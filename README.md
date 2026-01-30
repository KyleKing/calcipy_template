# Copier Calcipy

Project scaffold for Python packages built on `calcipy` ([kyleking/calcipy](https://github.com/KyleKing/calcipy)). Built with `copier` so projects can be kept up-to-date

**Now using `uv` instead of Poetry!** See the [Migration section](#migration-from-poetry-to-uv) below for details.

## Quick Start

```sh
# Install uv if you haven't already
# Option 1: Using the official installer (recommended)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Option 2: Using Homebrew (macOS/Linux)
brew install uv

# Install copier globally with pipx or use your preferred method
pipx install copier

# For end users, get the template with the below snippet. Replace dest_folder_name (can use ".")
copier copy --UNSAFE gh:KyleKing/calcipy_template dest_folder_name

# After generation, install dependencies
cd dest_folder_name
uv sync

# Updates can be retrieved with:
copier update . --UNSAFE
# I personally have aliases for:
alias copier-update='copier update --UNSAFE --conflict=rej'
alias copier-auto-update='copier-update --defaults'
```

## Migration from Poetry to uv

If you're updating an existing project using this template, the migration from Poetry to uv is automated:

### What Happens Automatically

When you run `copier update`, the `_copier_post_generation.py` script will:

1. **Remove Poetry files:** `poetry.lock`, `poetry.toml`, and `.venv/`
2. **Update configurations:** `.pre-commit-config.yaml` references are updated from `poetry.lock` → `uv.lock` and `poetry run` → `uv run`

### Manual Steps After Update

```sh
# 1. Sync dependencies (creates .venv and uv.lock)
uv sync

# 2. Verify everything works
./run --help
./run main --keep-going

# 3. Commit the changes
git add .
git commit -m "chore: migrate from Poetry to uv"
```

### Command Mapping

| Poetry Command | uv Equivalent |
|---|---|
| `poetry install` | `uv sync` |
| `poetry add <package>` | `uv add <package>` |
| `poetry add --group dev <package>` | `uv add --dev <package>` |
| `poetry remove <package>` | `uv remove <package>` |
| `poetry run <command>` | `uv run <command>` |
| `poetry show` | `uv pip list` |
| `poetry lock` | `uv lock` |
| `poetry update` | `uv lock --upgrade` |

### Why uv?

- **Speed:** 10-100x faster dependency resolution
- **Standard:** Uses PEP 621 format (future-proof)
- **Compatibility:** Full pip/PyPI ecosystem support
- **Active:** Maintained by Astral (creators of Ruff)

For detailed troubleshooting, see [uv documentation](https://docs.astral.sh/uv/).

## Alternatives

This project scaffold is primarily for my personal use, so you may find that there are other templates that better support your use case. I would recommend any of these:

- [pawamoy/copier-poetry](https://github.com/pawamoy/copier-poetry) or [pawamoy/copier-pdm](https://github.com/pawamoy/copier-pdm) (both have heavily inspired this version!)
- [cjolowicz/cookiecutter-hypermodern-python](https://github.com/cjolowicz/cookiecutter-hypermodern-python)

## Local Development

```sh
# Local changes need to be committed to take effect (at a later point squash all "tmp" commits)
git add . && git commit -m "tmp" && copier . ../test_template  --UNSAFE --conflict=rej --vcs-ref=HEAD

# For testing update from within the target directory
#   Note: make sure to commit changes in test directory before running copier
#   If not, after answering all of the questions, you may see this error and need to restart:
#     "Destination repository is dirty; cannot continue. Please commit or stash your local changes and retry."
cd test_template
copier copy --UNSAFE ../calcipy_template .
copier update . --UNSAFE --conflict=rej --defaults
```

## Releases

Any push to the repository `main` branch will trigger a version bump based on [`commitizen` rules (`fix`, `feat`, etc.)](https://commitizen-tools.github.io/commitizen/)

## Support

Below are a couple of useful snippets related to maintaining a package that utilizes this template

### Bulk Removing a Specific GitHub Action's History

After renaming or removing a workflow, run this script to tidy up the list of Actions and avoid folding under "See More." This script will delete all runs for a specific workflow and could be extended as needed.

```sh
#!/bin/zsh -e

# GitHub API docs: https://docs.github.com/en/rest/actions/workflow-runs?apiVersion=2022-11-28
#   GH CLI Docs: https://cli.github.com/manual/gh_api
# Inspiration: https://qmacro.org/blog/posts/2021/03/26/mass-deletion-of-github-actions-workflow-runs/

OWNER=kyleking
REPO=tail-jsonl
WORKFLOW_ID=upgrade-dependencies.yml

run_ids=$( \
        gh api \
        --header "Accept: application/vnd.github+json" \
        --header "X-GitHub-Api-Version: 2022-11-28" \
        "/repos/$OWNER/$REPO/actions/workflows/$WORKFLOW_ID/runs" \
        --method=GET \
        --raw-field='per_page=100' \
        --jq '.workflow_runs[].id' \
    )
echo $run_ids | xargs -I_ echo _
echo $run_ids | xargs -I_ gh api -X DELETE "/repos/$OWNER/$REPO/actions/runs/_"
```
