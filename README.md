# Copier Calcipy

Project scaffold for Python packages built on `calcipy` ([kyleking/calcipy](https://github.com/KyleKing/calcipy)). Built with `copier` so projects can be kept up-to-date

## Quick Start

```sh
# Install copier globally with pipx or use your preferred method
pipx install copier

# For end users, get the template with the below snippet. Replace dest_folder_name (can use ".")
copier copy gh:KyleKing/calcipy_template dest_folder_name

# Updates can be retrieved with:
copier update .
```

## Alternatives

This project scaffold is primarily for my personal use, so you may find that there are other templates that better support your use case. I would recommend any of these:

- [pawamoy/copier-poetry](https://github.com/pawamoy/copier-poetry) or [pawamoy/copier-pdm](https://github.com/pawamoy/copier-pdm) (both have heavily inspired this version!)
- [cjolowicz/cookiecutter-hypermodern-python](https://github.com/cjolowicz/cookiecutter-hypermodern-python)
- This project is built with [copier](https://github.com/copier-org/copier), but there is also [cookiecutter](https://github.com/cookiecutter/cookiecutter)/[cruft](https://github.com/cruft/cruft) and the very cool [flexlate](https://github.com/nickderobertis/flexlate) to consider

## Local Development

```sh
# Local changes need to be committed to take effect (at a later point squash all "tmp" commits)
git add . && git commit -m "tmp" && copier . ../test_template --force --vcs-ref=HEAD
# Note: "--force" skips all questions and overwrites files without asking

# For testing update from within the target directory
#   Note: make sure to commit changes in test directory before running copier
#   If not, after answering all of the questions, you may see this error and need to restart:
#   > Destination repository is dirty; cannot continue. Please commit or stash your local changes and retry.
cd test_template
copier copy ../calcipy_template .
copier --force update .
```

## Releases

Any push to the repository `main` branch will trigger a version bump based on [`commitizen` rules (`fix`, `feat`, etc.)](https://commitizen-tools.github.io/commitizen/)

If this repository is cloned, you will need to add a Personal Access Token to the repository under `Settings > Secrets > Add new secret` ([see guide](https://commitizen-tools.github.io/commitizen/tutorials/github_actions/))
