"""Post-Generation Script to be run from Copier."""

from pathlib import Path


def delete_myself():
    """Delete this file after completing the main script."""
    Path(__file__).unlink()


if __name__ == '__main__':
    print("""
Project successfully generated!

1. Install dependencies 'poetry install'
2. Run `poetry run doit list` to show the available actions

""")

    delete_myself()
