"""Post-Generation Script to be run from Copier."""

import re
import shutil
from pathlib import Path

# Don't print any output if matching directories like:
# /private/var/folders/1f/gd24l7210d3d8crp0clcm4440000gn/T/copier.main.update_diff.7eb725cw/.git/
# /private/var/folders/1f/gd24l7210d3d8crp0clcm4440000gn/T/copier.main.recopy_diff.gnos2law/.git/

_re_copier_dir = re.compile(f'copier\.[^\.]+\.\w+_diff\.')
_IS_PROJ = not _re_copier_dir.search(Path(__file__).absolute().as_posix())


def log(message: str) -> None:
    if _IS_PROJ:
        print(message)


def cleanup() -> None:
    """Remove files and folders that are no longer used."""
    paths = [
        Path('.deepsource.toml'),
        Path('.pyup.yml'),
        Path('appveyor.yml'),
        Path('mypy.ini'),
        Path('requirements.txt'),
        Path('docs/docs/CODE_OF_CONDUCT.md'),
        Path('docs/docs/CONTRIBUTING.md'),
        Path('docs/docs/SECURITY.md'),
        
        Path('.calcipy_packaging.lock'),
        Path('.pre-commit-config.yaml'),
        Path('.sourcery.yaml'),
        Path('mkdocs.yml'),
        
    ]
    directories = [
        Path('_adr'),
    ]

    for pth in paths:
        if pth.is_file():
            log(f'Removing: {pth}')
            pth.unlink()  # FYI: "missing_ok" was added in 3.8, but this script is ^3.7
    for dir_pth in directories:
        if dir_pth.is_dir():
            log(f'Deleting: {dir_pth}')
            shutil.rmtree(dir_pth)


def delete_myself() -> None:
    """Delete this file after completing the main script."""
    Path(__file__).unlink()


if __name__ == '__main__':
    log("""
The 'test_template' package has been updated!

1. Review the changes and commit. Merge conflicts will be logged by copier in '*.rej' files
2. Install dependencies with 'poetry install --sync'
3. Run `poetry run doit list` to show the available actions
4. Run `poetry run doit --continue` to try running all default tasks
""")
    cleanup()
    delete_myself()
