#!/bin/bash -e

# Convenience script to sync latest .ctt configuration files with the top-level template

cp .ctt/default/.editorconfig .editorconfig
cp .ctt/default/.ruff.toml .ruff.toml
cp .ctt/default/.flake8 .flake8

echo 'FYI: Occasionally sync the pre-commit config, but requires manual review'
echo '  cp .ctt/default/.pre-commit-config.yaml .pre-commit-config.yaml'
