"""Post-Generation Script to be run from Copier."""

import shutil
from pathlib import Path


def cleanup() -> None:
    """Remove files and folders that are no longer used."""
    paths = [
        Path('.pyup.yml'),
        Path('appveyor.yml'),
    ]
    directories = [
        Path('_adr'),
    ]

    for pth in paths:
        if pth.is_file():
            print(f'Removing: {pth}')
            pth.unlink()  # FYI: "missing_ok" was added in 3.8, but this script is ^3.7
    for dir_pth in directories:
        if dir_pth.is_dir():
            print(f'Deleting: {dir_pth}')
            shutil.rmtree(dir_pth)


def delete_myself() -> None:
    """Delete this file after completing the main script."""
    Path(__file__).unlink()


if __name__ == '__main__':
    print("""
Project successfully generated!

1. Install dependencies 'poetry install'
2. Run `poetry run doit list` to show the available actions

""")
    cleanup()
    delete_myself()
