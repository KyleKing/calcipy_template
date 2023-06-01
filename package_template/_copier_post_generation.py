"""Post-Generation Script to be run from Copier."""

import json
import re
import shutil
from pathlib import Path
from dataclasses import dataclass

# Don't print any output if matching directories like:
# /private/var/folders/1f/gd24l7210d3d8crp0clcm4440000gn/T/copier.main.update_diff.7eb725cw/.git/
# /private/var/folders/1f/gd24l7210d3d8crp0clcm4440000gn/T/copier.main.recopy_diff.gnos2law/.git/
_re_copier_dir = re.compile(rf'copier\.[^\.]+\.\w+_diff\.')
_IS_PROJ = not _re_copier_dir.search(Path(__file__).absolute().as_posix())


@dataclass
class Config:
    package_name_py: str
    doc_dir: str


_CONFIG_PATH = Path(__file__).with_suffix('.json')
_CONFIG = Config(**json.loads(_CONFIG_PATH.read_text()))
_CONFIG_PATH.unlink()


def log(message: str) -> None:
    if _IS_PROJ:
        print(message)


def cleanup() -> None:
    """Remove files and folders that are no longer used."""
    paths = [
        Path('.deepsource.toml'),
        Path('.doit-db.sqlite'),
        Path('.doit.tmp-py'),
        Path('.doit.tmp-toml'),
        Path('.github/workflows/codeql-config.yml'),
        Path('.github/workflows/upgrade-dependencies.yml'),
        Path('.pyup.yml'),
        Path('.sourcery.yaml'),
        Path('.sourcery.yaml'),
        Path('.yamllint.yaml'),
        Path('appveyor.yml'),
        Path('dodo.py'),
        Path('flake8-full.log'),
        Path('mypy.ini'),
        Path('requirements.txt'),
        Path('ruff.toml'),
        Path(f'{_CONFIG.doc_dir}/docs/_docs.md'),
        Path(f'{_CONFIG.doc_dir}/docs/CODE_OF_CONDUCT.md'),
        Path(f'{_CONFIG.doc_dir}/docs/CONTRIBUTING.md'),
        Path(f'{_CONFIG.doc_dir}/docs/SECURITY.md'),
    ]
    directories = [
        Path('.logs'),
        Path('_adr'),
        Path(f'{_CONFIG.doc_dir}/css'),
    ]

    for pth in paths:
        if pth.is_file():
            log(f'Removing: {pth}')
            pth.unlink()  # FYI: "missing_ok" was added in 3.8, but this script is ^3.7
    for dir_pth in directories:
        if dir_pth.is_dir():
            log(f'Deleting: {dir_pth}')
            shutil.rmtree(dir_pth)


def validate_configuration():
    copier_text = Path('.copier-answers.yml').read_text()
    copier_dict = {
        line.split(':')[0]: line.split(':')[-1].strip()
        for line in copier_text.split('\n')
        if ':' in line
    }

    errors = []
    extras_value = copier_dict['install_extras']
    if extras_value == 'None':
        errors.append(f'install_extras should be an empty string or list of extras, not {extras_value}')
    python_value = copier_dict['minimum_python'].replace('"', '').replace("'", '').split('.')[:2]
    python_short_value = copier_dict['minimum_python_short'].replace('"', '').replace("'", '').split('.')
    if python_value != python_short_value:
        errors.append(f'Error in Python versions ({python_value} != {python_short_value})')
    if errors:
        print('\n\n')
        print('Please review the errors below and edit the copier answers accordingly')
        print(errors)
        print('\n\n')
        exit(1)


def delete_myself() -> None:
    """Delete this file after completing the main script."""
    Path(__file__).unlink()


if __name__ == '__main__':
    log(
        f"""
The '{_CONFIG.package_name_py}' package has been updated!

1. Review the changes and commit. Merge conflicts will be logged by copier in '*.rej' files
2. Install dependencies with 'poetry install --sync'
3. Run `poetry run doit list` to show the available actions
4. Run `poetry run doit --continue` to try running all default tasks
"""
    )
    cleanup()
    validate_configuration()
    delete_myself()
