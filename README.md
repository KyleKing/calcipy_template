# Copier Calcipy

Project scaffold for Python packages built on `calcipy` ([kyleking/calcipy](https://github.com/KyleKing/calcipy)). Built with `copier` so projects can be kept up-to-date

## Quick Start

```sh
# Install copier globally with pipx or use your preferred method
pipx install copier

# For end users, get the template with the below snippet. Replace dest_folder_name (can use ".")
copier copy --UNSAFE gh:KyleKing/calcipy_template dest_folder_name

# Updates can be retrieved with:
copier update . --UNSAFE
# I personally have aliases for:
alias copier-update='copier update --UNSAFE --conflict=rej'
alias copier-auto-update='copier-update --defaults'
```

## Alternatives

This project scaffold is primarily for my personal use, so you may find that there are other templates that better support your use case. I would recommend any of these:

- [pawamoy/copier-poetry](https://github.com/pawamoy/copier-poetry) or [pawamoy/copier-pdm](https://github.com/pawamoy/copier-pdm) (both have heavily inspired this version!)
- [cjolowicz/cookiecutter-hypermodern-python](https://github.com/cjolowicz/cookiecutter-hypermodern-python)
- This project is built with [copier](https://github.com/copier-org/copier), but there is also [cookiecutter](https://github.com/cookiecutter/cookiecutter)/[cruft](https://github.com/cruft/cruft) and the very cool [flexlate](https://github.com/nickderobertis/flexlate) to consider

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

If this repository is cloned, you will need to add a Personal Access Token to the repository under `Settings > Secrets > Add new secret` ([see guide](https://commitizen-tools.github.io/commitizen/tutorials/github_actions/))

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
