# /// script
# dependencies = ["tomlkit>=0.13"]
# requires-python = ">=3.9"
# ///
"""Migration Script for Poetry to uv conversion.

Reads Poetry dependencies from the last committed version of pyproject.toml
(via git history) and applies them to the current pyproject.toml after Copier.

Usage:
    uv run _poetry_to_uv_migration.py

The script will self-delete when no migration is needed.
"""

from __future__ import annotations

import shutil
import subprocess  # noqa: S404 # Required for git operations with controlled input
from itertools import starmap
from pathlib import Path


def _log(message: str) -> None:
    print(f'[migration] {message}')  # noqa: T201


def _get_git_file_content(file_path: str, ref: str = 'HEAD') -> str | None:
    """Get file content from git history.

    Args:
        file_path: Path to file relative to repo root
        ref: Git reference (default: HEAD)

    Returns:
        File content if found, None otherwise
    """
    git_path = shutil.which('git')
    if not git_path:
        return None

    try:
        result = subprocess.run(  # noqa: S603 # git path from shutil.which, ref/file_path controlled
            [git_path, 'show', f'{ref}:{file_path}'],
            capture_output=True,
            text=True,
            check=False,
        )
    except (subprocess.SubprocessError, FileNotFoundError):
        return None
    else:
        return result.stdout if result.returncode == 0 else None


def _check_if_migration_needed() -> bool:
    """Check if migration is needed by looking for Poetry config in git history."""
    content = _get_git_file_content('pyproject.toml')
    if not content:
        return False

    import tomlkit  # noqa: PLC0415

    try:
        doc = tomlkit.parse(content)
        return 'poetry' in doc.get('tool', {})
    except Exception:
        return False


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


def _extract_poetry_dependencies(git_doc: dict) -> tuple[list[str], list[str]]:
    """Extract main and dev dependencies from Poetry config.

    Args:
        git_doc: Parsed pyproject.toml from git history

    Returns:
        Tuple of (main_dependencies, dev_dependencies)
    """
    deps = []
    dev_deps = []

    try:
        poetry = git_doc['tool']['poetry']
        deps = _convert_dependencies(poetry['dependencies'])
        _log(f'Found {len(deps)} main dependencies in git history')
    except (KeyError, AttributeError) as err:
        _log(f'No main dependencies in git history: {err}')

    try:
        poetry = git_doc['tool']['poetry']
        dev_deps_dict = poetry['group']['dev']['dependencies']
        dev_deps = list(starmap(_format_dependency_spec, dev_deps_dict.items()))
        _log(f'Found {len(dev_deps)} dev dependencies in git history')
    except (KeyError, AttributeError) as err:
        _log(f'No dev dependencies in git history: {err}')

    return deps, dev_deps


def _apply_dependencies_to_pyproject(
    deps: list[str],
    dev_deps: list[str],
) -> bool:
    """Apply dependencies to current pyproject.toml.

    Args:
        deps: Main dependencies to apply
        dev_deps: Dev dependencies to apply

    Returns:
        True if modifications were made, False otherwise
    """
    import tomlkit  # noqa: PLC0415

    pyproject_path = Path('pyproject.toml')
    if not pyproject_path.is_file():
        _log('No pyproject.toml found in working directory')
        return False

    content = pyproject_path.read_text(encoding='utf-8')
    doc = tomlkit.parse(content)
    modified = False

    if deps:
        _log('Applying [project.dependencies]...')
        if 'project' not in doc:
            doc.add('project', tomlkit.table())

        existing_deps = doc['project'].get('dependencies', [])
        all_deps = list(existing_deps) + deps
        doc['project']['dependencies'] = tomlkit.array(all_deps)
        modified = True
        _log(f'Applied {len(deps)} dependencies to [project.dependencies]')

    if dev_deps:
        _log('Applying [dependency-groups.dev]...')
        if 'dependency-groups' not in doc:
            doc.add('dependency-groups', tomlkit.table())

        existing_dev_deps = doc['dependency-groups'].get('dev', [])
        all_dev_deps = list(existing_dev_deps) + dev_deps
        doc['dependency-groups']['dev'] = tomlkit.array(all_dev_deps)
        modified = True
        _log(f'Applied {len(dev_deps)} dependencies to [dependency-groups.dev]')

    if modified:
        pyproject_path.write_text(tomlkit.dumps(doc), encoding='utf-8')
        _log('Dependencies migrated successfully')

    return modified


def _migrate_dependencies_from_git() -> bool:
    """Read Poetry dependencies from git history and apply to current pyproject.toml.

    Returns:
        True if migration was performed, False otherwise.
    """
    import tomlkit  # noqa: PLC0415

    _log('Reading Poetry config from git history...')
    git_content = _get_git_file_content('pyproject.toml')
    if not git_content:
        _log('Could not read pyproject.toml from git history')
        return False

    git_doc = tomlkit.parse(git_content)
    if 'poetry' not in git_doc.get('tool', {}):
        _log('No Poetry config found in git history')
        return False

    deps, dev_deps = _extract_poetry_dependencies(git_doc)
    if not deps and not dev_deps:
        _log('No Poetry dependencies found in git history')
        return False

    return _apply_dependencies_to_pyproject(deps, dev_deps)


def _cleanup_poetry_files() -> bool:
    """Remove Poetry-specific files.

    Returns:
        True if any file was removed, False otherwise.
    """
    removed = False

    try:
        poetry_lock = Path('poetry.lock')
        if poetry_lock.is_file():
            _log('Removing poetry.lock')
            poetry_lock.unlink()
            removed = True
    except OSError as err:
        _log(f'Failed to remove poetry.lock: {err}')

    try:
        poetry_toml = Path('poetry.toml')
        if poetry_toml.is_file():
            _log('Removing poetry.toml')
            poetry_toml.unlink()
            removed = True
    except OSError as err:
        _log(f'Failed to remove poetry.toml: {err}')

    return removed


def main() -> None:
    """Run the migration."""
    if not _check_if_migration_needed():
        _log('No Poetry config found in git history - self-deleting')
        Path(__file__).unlink()
        return

    _log('Starting Poetry to uv dependency migration...')
    _log('')

    migration_performed = False

    # Migrate dependencies from git history
    try:
        migration_performed |= _migrate_dependencies_from_git()
    except Exception as err:
        _log(f'Error migrating dependencies: {err}')

    # Cleanup poetry files
    try:
        migration_performed |= _cleanup_poetry_files()
    except Exception as err:
        _log(f'Error cleaning up poetry files: {err}')

    if not migration_performed:
        _log('No changes were made')
        return

    _log('')
    _log('Migration complete!')
    _log('')
    _log('Next steps:')
    _log('  1. Review changes: git diff')
    _log('  2. Run: uv sync')
    _log('  3. Delete this script when satisfied')
    _log('')


if __name__ == '__main__':
    main()
