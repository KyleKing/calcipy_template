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
