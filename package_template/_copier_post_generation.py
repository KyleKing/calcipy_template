"""Post-Generation Script to be run from Copier."""

import json
import re
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path

# Don't print any output if matching directories like:
# /private/var/folders/1f/gd24l7210d3d8crp0clcm4440000gn/T/copier.main.update_diff.7eb725cw/.git/
# /private/var/folders/1f/gd24l7210d3d8crp0clcm4440000gn/T/copier.main.recopy_diff.gnos2law/.git/
_re_copier_dir = re.compile(r'copier\.[^\.]+\.\w+_diff\.')
_IS_PROJ = not _re_copier_dir.search(Path(__file__).absolute().as_posix())


@dataclass
class Config:
    cname: str
    doc_dir: str
    project_description: str
    package_name_py: str
    project_name: str


_CONFIG_PATH = Path(__file__).with_suffix('.json')
_CONFIG = Config(**json.loads(_CONFIG_PATH.read_text()))
_CONFIG_PATH.unlink()


def _log(message: str) -> None:
    if _IS_PROJ:
        print(message)  # noqa: T201


def cleanup() -> None:
    """Remove files and folders that are no longer used."""
    paths = [
        Path('.deepsource.toml'),
        Path('.doit-db.sqlite'),
        Path('.doit.tmp-py'),
        Path('.doit.tmp-toml'),
        Path('.github/codeql-config.yml'),
        Path('.github/workflows/codeql-analysis.yml'),
        Path('.github/workflows/codeql-config.yml'),
        Path('.github/workflows/upgrade-dependencies.yml'),
        Path('.pyup.yml'),
        Path('.sourcery.yaml'),
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
            _log(f'Removing: {pth}')
            pth.unlink()  # FYI: "missing_ok" was added in 3.8, but this script is ^3.7
    for dir_pth in directories:
        if dir_pth.is_dir():
            _log(f'Deleting: {dir_pth}')
            shutil.rmtree(dir_pth)


def validate_configuration() -> None:
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
    py_tuples = {
        key: re.compile(r'["\']+').sub('', copier_dict[key]).split('.')
        for key in ('minimum_python', 'minimum_python_short')
    }
    python_value = py_tuples['minimum_python'][:2]
    python_short_value = py_tuples['minimum_python_short']
    if python_value != python_short_value:
        errors.append(f'Error in Python versions ({python_value} != {python_short_value})')
    if errors:
        print('\n\n')  # noqa: T201
        print('Please review the errors below and edit the copier answers accordingly')  # noqa: T201
        print(errors)  # noqa: T201
        print('\n\n')  # noqa: T201
        sys.exit(1)


def delete_myself() -> None:
    """Delete this file after completing the main script."""
    Path(__file__).unlink()


if __name__ == '__main__':
    _log(
        f"""
The '{_CONFIG.package_name_py}' package has been updated (or created)!

1. Review the changes and commit. Merge conflicts may either be '*.rej' files or as inline git diffs
2. Install dependencies with 'poetry install --sync'
3. Run `./run --help` to show the available actions
4. Run `./run main --keep-going` to try running all default tasks after the changes
5. If this is a new project, you could create the GitHub repo with:

    ```sh
    gh repo create "{_CONFIG.project_name}" --source=. --remote=origin --push \
        --description="{_CONFIG.project_description}" --homepage="{_CONFIG.cname}" --public
    ```
""",
    )
    cleanup()
    validate_configuration()
    delete_myself()
