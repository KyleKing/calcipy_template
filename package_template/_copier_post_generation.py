"""Post-Generation Script to be run from Copier."""

import re
import shutil
import sys
from pathlib import Path


def _log(message: str | list[str]) -> None:
    print(message)  # noqa: T201


def cleanup() -> None:
    """Remove files and folders that are no longer used."""
    remove_list = Path('remove-if-found.txt')
    if not remove_list.is_file():
        return
    for line in remove_list.read_text(encoding='utf-8').split('\n'):
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
    cleanup()
    validate_configuration()
    delete_myself()
