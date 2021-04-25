# Copier Calcipy

Project scaffold for Python packages built on `calcipy` ([kyleking/calcipy](https://github.com/KyleKing/calcipy)). Utilizes `copier` to keep projects up to date (vs. cookie cutter which can only be used once)

## Quick Start

```sh
# Install copier globally with pipx or use your preferred method
pipx install copier

# For end users, get the template with the below snippet. Replace dest_folder_name
copier copy copier copy gh:KyleKing/copier_template dest_folder_name

# Updates can be retrieved with:
copier update .
```

## Alternatives

This project scaffold is primarily for my personal use, so you may find that there are other templates that better support your use case. I would recommend any of these:

- [pawamoy/copier-poetry](https://github.com/pawamoy/copier-poetry) or [pawamoy/copier-pdm](https://github.com/pawamoy/copier-pdm)
- [cjolowicz/cookiecutter-hypermodern-python](https://github.com/cjolowicz/cookiecutter-hypermodern-python)

## Development

```sh
# Local changes need to be committed to take effect (at a later point squash all "tmp" commits)
git add . && git commit -m "tmp" && copier . ../test_template --force
# Note: ^ force skips all questions and overwrites files without asking. Uses copier question default
# Note: ^ --force can't be used with copy or force sub-commands

# For testing update from within the target directory
# Note: make sure to commit changes in test directory before running copier
#   If not, after answering all of the questions, you may see this error and need to restart:
#   > Destination repository is dirty; cannot continue. Please commit or stash your local changes and retry.
cd test_template
copier copy ../calcipy_template .
copier update .
```
