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

import sys
from itertools import starmap
from pathlib import Path


def _log(message: str) -> None:
    print(f'[migration] {message}')  # noqa: T201


def _check_if_migration_needed() -> bool:
    """Check if migration is needed by checking for poetry.lock."""
    return Path('poetry.lock').is_file()


def _should_skip_migration(doc: dict) -> str | None:
    """Check if migration should be skipped, return reason if so."""
    if 'tool' not in doc or 'poetry' not in doc.get('tool', {}):
        return 'No [tool.poetry] section found, skipping pyproject.toml migration'

    build_system = doc.get('build-system', {})
    is_poetry_backend = 'poetry' in build_system.get('build-backend', '')
    if not is_poetry_backend:
        return 'Not using poetry backend, skipping pyproject.toml migration'

    return None


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


def _convert_dependencies(deps: dict) -> list[str]:
    """Convert Poetry dependencies to project format, excluding python version."""
    dep_list = []
    for name, spec in deps.items():
        if name == 'python':
            continue
        dep_list.append(_format_dependency_spec(name, spec))
    return dep_list


def _migrate_dependencies() -> bool:
    """Convert dependencies from Poetry to uv format in pyproject.toml.

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

    _log('Migrating dependencies from Poetry to uv format...')

    poetry = doc['tool']['poetry']
    modified = False

    # Migrate main dependencies to [project.dependencies]
    if 'dependencies' in poetry:
        deps = _convert_dependencies(poetry['dependencies'])
        if deps:
            if 'project' not in doc:
                doc.add('project', tomlkit.table())
            doc['project']['dependencies'] = tomlkit.array(deps)
            modified = True
            _log('Migrated [project.dependencies]')

    # Migrate dev dependencies to [dependency-groups.dev]
    if 'group' in poetry and 'dev' in poetry['group']:
        dev_deps_dict = poetry['group']['dev'].get('dependencies', {})
        if dev_deps_dict:
            dev_deps = list(starmap(_format_dependency_spec, dev_deps_dict.items()))
            if 'dependency-groups' not in doc:
                doc.add('dependency-groups', tomlkit.table())
            doc['dependency-groups']['dev'] = tomlkit.array(dev_deps)
            modified = True
            _log('Migrated [dependency-groups.dev]')

    if modified:
        pyproject_path.write_text(tomlkit.dumps(doc), encoding='utf-8')
        _log('Dependencies migrated successfully')
        return True

    _log('No dependency migration needed')
    return False


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

    _log('Starting Poetry to uv dependency migration...')
    _log('')

    migration_performed = False

    try:
        # Only migrate dependencies - template handles everything else
        migration_performed |= _migrate_dependencies()
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
        _log('  2. Update other project metadata manually if needed')
        _log('  3. Run: uv lock')
        _log('  4. Run: uv sync --all-extras')
        _log('  5. Test: ./run main')
        _log('  6. Commit changes and delete this script')
        _log('')

    except Exception as err:
        _log(f'Migration error: {err}')
        _log('Migration may be incomplete. Please review manually.')
        _log('This script has been kept for potential re-run.')
        sys.exit(1)


if __name__ == '__main__':
    main()
