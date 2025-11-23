"""Post-Generation Script to be run from Copier."""

import re
import shutil
import sys
from pathlib import Path


def _log(message: str | list[str]) -> None:
    print(message)  # noqa: T201


def migrate_from_poetry_to_uv() -> None:
    """Migrate from Poetry to uv by removing Poetry-specific files."""
    _log('Checking for Poetry migration...')

    # Remove Poetry-specific files
    poetry_files = ['poetry.lock', 'poetry.toml']
    for file_name in poetry_files:
        pth = Path(file_name)
        if pth.is_file():
            _log(f'Removing Poetry file: {pth}')
            pth.unlink()

    # Remove .venv to allow recreation with uv
    venv_path = Path('.venv')
    if venv_path.is_dir():
        _log('Removing .venv directory (will be recreated with uv sync)')
        shutil.rmtree(venv_path)

    # Update .pre-commit-config.yaml if it exists and has poetry references
    precommit_path = Path('.pre-commit-config.yaml')
    if precommit_path.is_file():
        content = precommit_path.read_text(encoding='utf-8')
        if 'poetry.lock' in content or 'poetry run' in content:
            _log('Updating .pre-commit-config.yaml references from poetry to uv')
            content = content.replace('poetry\\.lock', 'uv\\.lock')
            content = content.replace('poetry run', 'uv run')
            precommit_path.write_text(content, encoding='utf-8')

    _log('Poetry to uv migration complete.')


def cleanup() -> None:
    """Remove files and folders that are no longer used."""
    remove_list = Path('remove-if-found.txt')
    if not remove_list.is_file():
        return
    for line in remove_list.read_text().split('\n'):
        if not line:
            continue
        pth = Path(line)
        if pth.is_file():
            _log(f'Removing: {pth}')
            pth.unlink()
        elif pth.is_dir():
            _log(f'Deleting: {pth}')
            shutil.rmtree(pth)
    remove_list.unlink()


def validate_configuration() -> None:
    copier_text = Path('.copier-answers.yml').read_text(encoding='utf-8')
    copier_dict = {line.split(':')[0]: line.split(':')[-1].strip() for line in copier_text.split('\n') if ':' in line}

    errors = []
    py_tuples = {
        key: re.compile(r'["\']+').sub('', copier_dict[key]).split('.')
        for key in ('minimum_python', 'minimum_python_short')
    }
    python_value = py_tuples['minimum_python'][:2]
    python_short_value = py_tuples['minimum_python_short']
    if python_value != python_short_value:
        errors.append(f'Error in Python versions ({python_value} != {python_short_value})')
    if errors:
        _log('\n\n')
        _log('Please review the errors below and edit the copier answers accordingly')
        _log(errors)
        _log('\n\n')
        sys.exit(1)


def delete_myself() -> None:
    """Delete this file after completing the main script."""
    Path(__file__).unlink()


if __name__ == '__main__':
    _log('Running self-deleting post-setup script.')
    migrate_from_poetry_to_uv()
    cleanup()
    validate_configuration()
    delete_myself()
