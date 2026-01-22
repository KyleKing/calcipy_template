# /// script
# dependencies = ["tomlkit>=0.13"]
# requires-python = ">=3.9"
# ///
"""Migration Script for Poetry to uv conversion.

Run this script to migrate an existing poetry-based project to uv.
The script will self-delete only if no migration is needed.

Usage:
    uv run _poetry_to_uv_migration.py

If migration is performed, review changes carefully before running:
    uv lock
    uv sync --all-extras
"""

from __future__ import annotations

import re
import sys
from itertools import starmap
from pathlib import Path


def _log(message: str) -> None:
    print(f'[migration] {message}')  # noqa: T201


def _check_if_migration_needed() -> bool:
    """Check if migration is needed without importing tomlkit."""
    pyproject_path = Path('pyproject.toml')
    if not pyproject_path.is_file():
        return False

    content = pyproject_path.read_text(encoding='utf-8')

    # Simple check: does it have [tool.poetry] and poetry backend?
    has_poetry_section = '[tool.poetry]' in content
    has_poetry_backend = 'poetry' in content and 'build-backend' in content

    return has_poetry_section and has_poetry_backend


def _should_skip_migration(doc: dict) -> str | None:
    """Check if migration should be skipped, return reason if so."""
    if 'tool' not in doc or 'poetry' not in doc.get('tool', {}):
        return 'No [tool.poetry] section found, skipping pyproject.toml migration'

    build_system = doc.get('build-system', {})
    is_poetry_backend = 'poetry' in build_system.get('build-backend', '')
    if not is_poetry_backend:
        return 'Not using poetry backend, skipping pyproject.toml migration'

    return None


def _create_build_system() -> dict:
    """Create build-system table for uv."""
    import tomlkit  # noqa: PLC0415

    build_system = tomlkit.table()
    build_system['build-backend'] = 'uv_build'
    build_system['requires'] = ['uv_build>=0.9.7']
    return build_system


def _format_dependency_spec(name: str, spec: str | dict) -> str:
    """Format a dependency specification string."""
    if isinstance(spec, str):
        return f'{name}{spec}'

    version = spec.get('version', '>=0')
    extras = spec.get('extras', [])
    markers = spec.get('markers', '')

    old_calcipy_extras = {'doc', 'lint', 'nox', 'tags', 'test', 'types'}
    if name == 'calcipy' and set(extras) == old_calcipy_extras:
        return 'calcipy[dev]>=5.0.0'

    base = name
    if extras:
        base = f"{name}[{','.join(extras)}]"

    result = f'{base}{version}'
    if markers:
        result = f'{result}; {markers}'
    return result


def _convert_dev_dependencies(poetry: dict) -> list[str] | None:
    """Convert Poetry dev dependencies to uv dependency-groups format."""
    if 'group' not in poetry or 'dev' not in poetry['group']:
        return None

    dev_deps = poetry['group']['dev'].get('dependencies', {})
    if not dev_deps:
        return None

    return list(starmap(_format_dependency_spec, dev_deps.items()))


def _parse_author(author: str) -> dict:
    """Parse author string into name/email dict."""
    if '<' not in author or '>' not in author:
        return {'name': author}

    if match := re.match(r'(.+?)\s*<(.+?)>', author):
        return {'email': match.group(2), 'name': match.group(1)}

    return {'name': author}


def _convert_authors(poetry: dict) -> list[dict] | None:
    """Convert Poetry authors to project format."""
    if 'authors' not in poetry:
        return None

    return [_parse_author(author) for author in poetry['authors']]


def _convert_dependencies(deps: dict) -> tuple[list[str], str | None]:
    """Convert Poetry dependencies to project format, extracting python version."""
    dep_list = []
    python_version = None

    for name, spec in deps.items():
        if name == 'python':
            python_version = spec
            continue
        dep_list.append(_format_dependency_spec(name, spec))

    return dep_list, python_version


def _format_python_version(version_spec: str) -> str:
    """Format python version spec for requires-python."""
    version_clean = version_spec.lstrip('^~>=<!')
    return f'>={version_clean}'


def _build_urls_table(poetry: dict) -> dict | None:
    """Build URLs table from poetry configuration."""
    import tomlkit  # noqa: PLC0415

    if 'urls' in poetry:
        return poetry['urls']

    urls = tomlkit.table()
    if 'repository' in poetry:
        urls['Repository'] = poetry['repository']
    if 'documentation' in poetry:
        urls['Documentation'] = poetry['documentation']

    return urls or None


def _copy_tool_sections(source_doc: dict, target_doc: dict) -> None:
    """Copy non-poetry tool sections from source to target document."""
    import tomlkit  # noqa: PLC0415

    if 'tool' not in source_doc:
        return

    for key, value in source_doc['tool'].items():
        if key == 'poetry':
            continue
        if 'tool' not in target_doc:
            target_doc.add('tool', tomlkit.table())
        target_doc['tool'][key] = value


def _add_uv_config(doc: dict) -> None:
    """Add uv configuration to document."""
    import tomlkit  # noqa: PLC0415

    if 'tool' not in doc:
        doc.add('tool', tomlkit.table())
    doc['tool']['uv'] = tomlkit.table()
    doc['tool']['uv']['default-groups'] = ['dev']
    doc['tool']['uv']['required-version'] = '>=0.9.0'


def _build_project_section(poetry: dict) -> dict:
    """Build the project section from poetry configuration."""
    import tomlkit  # noqa: PLC0415

    project = tomlkit.table()

    if authors := _convert_authors(poetry):
        project['authors'] = tomlkit.array(authors)

    if 'classifiers' in poetry:
        project['classifiers'] = poetry['classifiers']

    deps = poetry.get('dependencies', {})
    dep_list, python_version = _convert_dependencies(deps)
    if dep_list:
        project['dependencies'] = tomlkit.array(dep_list)

    simple_fields = ['description', 'keywords', 'license', 'maintainers', 'name', 'readme', 'version']
    for key in simple_fields:
        if key in poetry:
            project[key] = poetry[key]

    if python_version:
        project['requires-python'] = _format_python_version(python_version)

    if 'scripts' in poetry:
        project['scripts'] = poetry['scripts']

    if urls := _build_urls_table(poetry):
        project['urls'] = urls

    return project


def _migrate_pyproject_toml() -> bool:
    """Convert pyproject.toml from Poetry to uv format.

    Returns:
        True if migration was performed, False otherwise.
    """
    import tomlkit  # noqa: PLC0415

    pyproject_path = Path('pyproject.toml')
    if not pyproject_path.is_file():
        _log('pyproject.toml not found, skipping')
        return False

    content = pyproject_path.read_text(encoding='utf-8')
    doc = tomlkit.parse(content)

    if skip_reason := _should_skip_migration(doc):
        _log(skip_reason)
        return False

    _log('Migrating pyproject.toml from Poetry to uv...')

    poetry = doc['tool']['poetry']
    new_doc = tomlkit.document()

    new_doc.add('build-system', _create_build_system())

    if dev_deps := _convert_dev_dependencies(poetry):
        new_doc.add('dependency-groups', tomlkit.table())
        new_doc['dependency-groups']['dev'] = tomlkit.array(dev_deps)

    new_doc.add('project', _build_project_section(poetry))

    _copy_tool_sections(doc, new_doc)
    _add_uv_config(new_doc)

    pyproject_path.write_text(tomlkit.dumps(new_doc), encoding='utf-8')
    _log('pyproject.toml migrated successfully')
    return True


def _update_file_content(path: Path, replacements: list[tuple[str, str]]) -> bool:
    """Update file content with the given replacements."""
    if not path.is_file():
        return False

    content = path.read_text(encoding='utf-8')
    original = content

    for old, new in replacements:
        content = content.replace(old, new)

    if content != original:
        path.write_text(content, encoding='utf-8')
        return True
    return False


def _migrate_workflow_files() -> bool:
    """Update GitHub workflow files.

    Returns:
        True if any file was updated, False otherwise.
    """
    workflows_dir = Path('.github/workflows')
    if not workflows_dir.is_dir():
        return False

    replacements = [
        ('poetry run ', 'uv run '),
        ('poetry.lock', 'uv.lock'),
        ('poetry install', 'uv sync'),
        ('cache: poetry', 'enable-cache: true'),
    ]

    updated = False
    for workflow in workflows_dir.glob('*.yml'):
        if _update_file_content(workflow, replacements):
            _log(f'Updated {workflow}')
            updated = True

    setup_action = Path('.github/actions/setup/action.yml')
    if setup_action.is_file():
        content = setup_action.read_text(encoding='utf-8')
        if 'poetry' in content.lower() or 'pipx' in content.lower():
            _log(f'Action {setup_action} needs manual review for uv migration')

    return updated


def _migrate_pre_commit() -> bool:
    """Update .pre-commit-config.yaml.

    Returns:
        True if file was updated, False otherwise.
    """
    pre_commit_path = Path('.pre-commit-config.yaml')
    replacements = [
        ('poetry run ', 'uv run '),
        ('poetry.lock', 'uv.lock'),
        ('poetry\\.lock', 'uv\\.lock'),
        ('lint.pre-commit', 'lint.prek'),
        ('pre-commit install', 'prek install -f'),
        ('pre-commit autoupdate', 'prek autoupdate'),
        ('pre-commit run', 'prek run'),
    ]

    if _update_file_content(pre_commit_path, replacements):
        _log('Updated .pre-commit-config.yaml')
        return True
    return False


def _migrate_run_script() -> bool:
    """Update run script.

    Returns:
        True if file was updated, False otherwise.
    """
    run_path = Path('run')
    replacements = [
        ('poetry run ', 'uv run '),
    ]

    if _update_file_content(run_path, replacements):
        _log('Updated run script')
        return True
    return False


def _migrate_docs() -> bool:
    """Update documentation files.

    Returns:
        True if any file was updated, False otherwise.
    """
    doc_dirs = [Path('docs'), Path('doc')]
    replacements = [
        ('poetry install --sync', 'uv sync --all-extras'),
        ('poetry install', 'uv sync'),
        ('poetry run ', 'uv run '),
        ('poetry config ', '# (uv uses UV_PUBLISH_TOKEN env var) '),
    ]

    updated = False
    for doc_dir in doc_dirs:
        if not doc_dir.is_dir():
            continue
        for md_file in doc_dir.rglob('*.md'):
            if _update_file_content(md_file, replacements):
                _log(f'Updated {md_file}')
                updated = True
    return updated


def _cleanup_poetry_files() -> bool:
    """Remove Poetry-specific files.

    Returns:
        True if any file was removed, False otherwise.
    """
    removed = False
    poetry_lock = Path('poetry.lock')
    if poetry_lock.is_file():
        _log('Removing poetry.lock')
        poetry_lock.unlink()
        removed = True

    poetry_toml = Path('poetry.toml')
    if poetry_toml.is_file():
        _log('Removing poetry.toml')
        poetry_toml.unlink()
        removed = True

    return removed


def _delete_myself() -> None:
    """Delete this script after completion."""
    script_path = Path(__file__).resolve()
    if script_path.is_file():
        try:
            script_path.unlink()
            _log(f'Deleted migration script: {script_path.name}')
        except OSError as err:
            _log(f'Warning: Could not delete migration script: {err}')


def main() -> None:
    """Run the migration."""
    # Check if migration is needed before importing tomlkit
    if not _check_if_migration_needed():
        _log('No Poetry migration needed - auto-deleting script')
        _delete_myself()
        return

    _log('Starting Poetry to uv migration...')
    _log('')

    migration_performed = False

    try:
        # Track if any migration was performed
        migration_performed |= _migrate_pyproject_toml()
        migration_performed |= _migrate_workflow_files()
        migration_performed |= _migrate_pre_commit()
        migration_performed |= _migrate_run_script()
        migration_performed |= _migrate_docs()
        migration_performed |= _cleanup_poetry_files()

        if not migration_performed:
            _log('No changes were necessary - auto-deleting script')
            _delete_myself()
            return

        _log('')
        _log('Migration complete!')
        _log('')
        _log('IMPORTANT: Review all changes carefully before proceeding.')
        _log('This script has been kept so you can re-run if needed.')
        _log('')
        _log('Next steps:')
        _log('  1. Review changes: git diff')
        _log('  2. Run: uv lock')
        _log('  3. Run: uv sync --all-extras')
        _log('  4. Test: ./run main')
        _log('  5. Commit changes and delete this script')
        _log('')

    except Exception as err:
        _log(f'Migration error: {err}')
        _log('Migration may be incomplete. Please review manually.')
        _log('This script has been kept for potential re-run.')
        sys.exit(1)


if __name__ == '__main__':
    main()
