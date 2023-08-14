## 1.7.12 (2023-08-14)

### Fix

- support Python <3.11

## 1.7.11 (2023-08-14)

### Fix

- filter all PEP-585 warnings
- ignore unimportant failures because of Python 3.8 beartype warnings

## 1.7.10 (2023-08-13)

### Fix

- allow Runtime Typechecking Mode for tests to be configurable
- update pre-commit

## 1.7.9 (2023-08-13)

### Fix

- drop CALCIPY prefix

## 1.7.8 (2023-08-12)

### Fix

- update ruff import rules
- correct the error message for invoke.task

## 1.7.7 (2023-08-05)

### Fix

- switch to a generic prefix

## 1.7.6 (2023-08-02)

### Fix

- use public export for default beartype warnings

## 1.7.5 (2023-07-31)

### Fix

- remove duplicate comments

## 1.7.4 (2023-07-30)

### Fix

- use options key for mkdocstrings

## 1.7.3 (2023-07-22)

### Fix

- import Self from typing extensions instead of beartype

## 1.7.2 (2023-07-22)

### Fix

- refactor to resolve pyright and mypy errors

## 1.7.1 (2023-07-22)

### Fix

- refactor configuration into function to encapsulate variables

## 1.7.0 (2023-07-22)

### Feat

- use beartype_this_package

## 1.6.28 (2023-07-22)

### Refactor

- activate pylint valid naming rules

## 1.6.27 (2023-07-17)

### Fix

- keep leading whitespace on install_extras

## 1.6.26 (2023-07-17)

### Fix

- resolve truthy warning from yamllint
- correct non-determinism in .ctt output
- correct error in variable name
- exclude cassette files from yamllint

## 1.6.25 (2023-07-17)

### Fix

- update pre-commit
- skip RUF013 until supported by pyright

## 1.6.24 (2023-06-24)

### Fix

- don't delete yamllint

### Refactor

- suppress pre-commit errors on Python code
- sync .ctt configuration with top-level pre-commit

## 1.6.23 (2023-06-23)

### Fix

- import Any from typing rather than beartype
- run pre-commit
- update editorconfig for lua and shell
- sync pre-commit config with .ctt
- resolve yamllint error for empty-values
- add yamllint config

### Refactor

- run pre-commit on .ctt output

## 1.6.22 (2023-06-23)

### Fix

- typo in if extends_calcipy for the script.py file
- add companion yamllint to prettier in pre-commit

## 1.6.21 (2023-06-21)

### Fix

- filter TD001 for FIXME

## 1.6.20 (2023-06-17)

### Fix

- use the _CONFIG rather than template for the post-generation script help text
- bump calcipy in pre-commit for latest ruff

## 1.6.19 (2023-06-17)

### Fix

- format with toml-sort

## 1.6.18 (2023-06-17)

### Fix

- ignore new ruff 'FIX00#' rules

## 1.6.17 (2023-06-16)

### Fix

- update the instructions post-update
- remove unnecessary copier question defaults

## 1.6.16 (2023-06-06)

### Fix

- upgrade to copier 8

## 1.6.15 (2023-06-06)

### Refactor

- update Action removal script to loop

## 1.6.14 (2023-06-01)

### Fix

- actively remove the upgrade-dependencies workflow

## 1.6.13 (2023-06-01)

### Fix

- correct formatting for pre-commit config

## 1.6.12 (2023-06-01)

### Fix

- properly configure the prettier hook
- remove Upgrade Dependencies workflow

## 1.6.11 (2023-05-24)

### Fix

- simplify issue templates

## 1.6.10 (2023-05-24)

### Fix

- escalate warnings to errors in pytest
- remove extra whitespace in ruff configuration

## 1.6.9 (2023-05-23)

### Fix

- actually ignore the new TD002 & TD003

## 1.6.8 (2023-05-23)

### Fix

- ignore the new TD002 & TD003

## 1.6.7 (2023-05-22)

### Fix

- remove TODO comments that were appearing in the downstream Code Tag Summaries

## 1.6.6 (2023-05-22)

### Fix

- remove pyupgrade runtime typing configuration

## 1.6.5 (2023-05-17)

### Fix

- expand ADR section in docs

### Refactor

- recreate .ctt/

## 1.6.4 (2023-05-13)

### Fix

- make pylint more strict

## 1.6.3 (2023-04-22)

### Fix

- remove unused ADR directory and logic

## 1.6.2 (2023-04-09)

### Fix

- make post-validation script more robust

## 1.6.1 (2023-04-09)

### Fix

- actually call the validation logic

## 1.6.0 (2023-04-09)

### Feat

- validate the copier config post-install

### Fix

- set extends Calcipy to False by default
- use new sort-keys from toml-sort

## 1.5.0 (2023-04-08)

### Feat

- add pre-commit autoupdate

### Fix

- bump calcipy version

## 1.4.3 (2023-04-06)

### Fix

- bump default poetry version

## 1.4.2 (2023-04-06)

### Fix

- remove mdx-truly-sane-lists

## 1.4.1 (2023-04-03)

### Fix

- run CI on changes to dependencies

## 1.4.0 (2023-03-11)

### Feat

- turn on pyright for CI

## 1.3.0 (2023-03-03)

### Feat

- use new 'strict: false' from https://github.com/timvink/mkdocs-git-revision-date-localized-plugin/issues/108

## 1.2.10 (2023-03-02)

### Fix

- bump minimum calcipy in pre-commit
- correct typo in doc_dir

## 1.2.9 (2023-03-02)

### Fix

- **#4**: additional minor link corrections

## 1.2.8 (2023-03-02)

### Fix

- specify the default source url

## 1.2.7 (2023-03-02)

### Fix

- minor cleanup
- **#4**: resolve links from PyPi to documentation site
- remove legacy calcipy output files

### Refactor

- update gitignore and use the new .ruff.toml

## 1.2.6 (2023-02-25)

### Fix

- make scripts.py optional and extend ruff.toml

## 1.2.5 (2023-02-23)

### Fix

- minor logging and pre-commit updates

## 1.2.4 (2023-02-23)

### Fix

- correct typo in mdformat-mkdocs extra & remove duplicate copier-ff

## 1.2.3 (2023-02-23)

### Fix

- make extending calcipy optional

## 1.2.2 (2023-02-23)

### Fix

- update version of calcipy pre-commit

## 1.2.1 (2023-02-23)

### Fix

- use calcipy pre-commit instead of local
- remove trailing comma from template

## 1.2.0 (2023-02-23)

### Feat

- remove include_all

### Fix

- replace shoal references with calcipy and corallium
- set known_first_party to the package name

## 1.1.0 (2023-02-22)

### Feat

- use regex rules for commitizen

### Fix

- don't specify venvPath for pyright

## 1.0.3 (2023-02-21)

### Fix

- update ruff.toml
- assign the right permissions for workflows

## 1.0.2 (2023-02-21)

### Fix

- add missing ruff.toml and minor patches

## 1.0.1 (2023-02-21)

### Fix

- correct the logic in the post-generation script

## 1.0.0 (2023-02-20)

### Feat

- migrate to calcipy v1!

### Fix

- add cz back to pyproject.toml
- correct copier post generation JSON

## 0.18.2 (2023-02-08)

### Fix

- switch to mdformat-mkdocs, prettier, and drop taplo

## 0.18.1 (2023-02-07)

### Fix

- bump poetry minimum version

### Refactor

- use encoding in tests

## 0.18.0 (2023-01-10)

### Feat

- use MkDocs new watch feature

### Fix

- resolve issues flagged by actionlint
- use only the major and minor version for CI

## 0.17.7 (2022-12-05)

### Fix

- bump default Python to 3.8.12

## 0.17.6 (2022-12-04)

### Fix

- make the PR template less bad

## 0.17.5 (2022-11-29)

### Fix

- CodeQL configuration can't be in the workflows dir
- mypy uses "type: ignore" not the other order

## 0.17.4 (2022-11-27)

### Fix

- make the noxfile only part of include_all
- add watch directory to mkdocstrings

## 0.17.3 (2022-11-27)

### Fix

- move CodeQL to configuration file
- use title case A for mkdocs section-index

## 0.17.2 (2022-11-21)

### Fix

- switch css to _styles for consistency

## 0.17.1 (2022-11-20)

### Fix

- ignore end of file new line in answer file
- correct URLs for documentation site

## 0.17.0 (2022-11-20)

### Feat

- add ctt!
- support Python 3.11 (tomllib and calcipy.pythons)

### Fix

- remove tab navigation in doc site

## 0.16.3 (2022-11-13)

### Fix

- correct indent error on CodeQL Pipeline

## 0.16.2 (2022-11-13)

### Fix

- use the project_name where appropriate

## 0.16.1 (2022-11-13)

### Fix

- the repository URL must use the package_name instead of python

### Refactor

- introduce a single variable for the repo_url

## 0.16.0 (2022-11-12)

### Feat

- bump minimum copier version to resolve warning

### Fix

- suppress TC003
- begin excluding false positives from CodeQL

## 0.15.11 (2022-11-06)

### Fix

- switch the actual package_template to use pyproject-fmt

## 0.15.10 (2022-11-06)

### Fix

- switch to latest repo for pyproject-fmt

## 0.15.9 (2022-10-28)

### Fix

- source documentation was only being built for calcipy

## 0.15.8 (2022-10-28)

### Fix

- merge flake8 config from pft
- convert pylintrc to jinja for min_py
- simpify pylintrc

## 0.15.7 (2022-10-19)

### Fix

- bump default poetry to 1.2.2

## 0.15.6 (2022-10-19)

### Fix

- further minor improvements to the post-generate script help text

## 0.15.5 (2022-10-19)

### Fix

- typo in generation script

## 0.15.4 (2022-10-19)

### Fix

- make the printed generation message conditional

## 0.15.3 (2022-10-18)

### Fix

- move auto_format from pre-commit to doit when not include_all
- reflect auto-fixes into template files

## 0.15.2 (2022-10-18)

### Fix

- the in-file-name if doesn't work with .jinja

## 0.15.1 (2022-10-18)

### Fix

- reduce default task list

## 0.15.0 (2022-10-18)

### Feat

- add include_all to support skipping excess files

### Refactor

- drop hard-coded Jinja syntax

## 0.14.0 (2022-10-16)

### Feat

- add puml diagram builder

### Fix

- re-add mkdocs site-url

## 0.13.3 (2022-10-12)

### Fix

- set minimum Python version for flake8
- remove redundant required arguments

## 0.13.2 (2022-10-05)

### Fix

- make ADR optional

## 0.13.1 (2022-10-02)

### Fix

- remove redundant sourcery rules to flake8 plugins

## 0.13.0 (2022-09-27)

### Feat

- add custom styles for mkdocstrings
- add mkdocs-based docstrings

### Fix

- format jinja doc_dir name

## 0.12.2 (2022-09-26)

### Fix

- run labeler GHA less frequently

## 0.12.1 (2022-09-26)

### Fix

- doit task is check_types

## 0.12.0 (2022-09-26)

### Feat

- merge mypy.ini from pytest-cache-assert

## 0.11.0 (2022-09-25)

### Feat

- add type_check to CI

### Fix

- correct for extra whitespace in jinja sourcery template

## 0.10.3 (2022-09-25)

### Fix

- remove duplicate PR Template

## 0.10.2 (2022-09-20)

### Fix

- drop nox check_security and run in doit instead

## 0.10.1 (2022-09-18)

### Fix

- set Python version as major.minor for Sourcery

## 0.10.0 (2022-09-17)

### Feat

- add CodeQL workflow

### Fix

- remove check_safety from nox

## 0.9.5 (2022-09-17)

### Fix

- update pre-commit files

### Refactor

- convert sourcery to jinja template to use min_py version
- remove relative-import rule from sourcery

## 0.9.4 (2022-09-17)

### Fix

- suppress unimportant yamllint length errors

## 0.9.3 (2022-09-17)

### Fix

- skip Ubuntu for test matrix

## 0.9.2 (2022-09-17)

### Fix

- bump poetry version to match lock file
- configurable development_branch target for dep upgrades
- remove trailing space and cleanup comments

## 0.9.1 (2022-09-17)

### Fix

- don't remove sourcery file post-update

## 0.9.0 (2022-09-17)

### Feat

- init sourcery file with Google rules

## 0.8.4 (2022-09-13)

### Fix

- last set of escaped brackets

## 0.8.3 (2022-09-13)

### Fix

- last one?

## 0.8.2 (2022-09-12)

### Fix

- escape matrix.python-version

## 0.8.1 (2022-09-12)

### Fix

- escape matrix.os

## 0.8.0 (2022-09-12)

### Feat

- support minimum_python setting

## 0.7.6 (2022-08-07)

### Fix

- also remove bump version default shell

## 0.7.5 (2022-08-07)

### Refactor

- remove most suggested Github issue tags

## 0.7.4 (2022-08-07)

### Refactor

- set default for CNAME

## 0.7.3 (2022-08-06)

### Fix

- bump minimum calcipy

## 0.7.2 (2022-08-06)

### Refactor

- use conventional commit for PR title

## 0.7.1 (2022-08-05)

### Fix

- use copyright year

## 0.7.0 (2022-08-05)

### Feat

- sync with latest calcipy

## 0.6.4 (2022-08-02)

### Refactor

- update onboarding script

## 0.6.3 (2022-02-27)

### Fix

- remove requirements file if found

## 0.6.2 (2022-02-27)

### Fix

- try moving .doit.db outside of git for pre-commit runners

## 0.6.1 (2022-02-27)

### Fix

- run poetry install regardless of cache hit
- add dispatch for manual re-runs

## 0.6.0 (2022-02-27)

### Fix

- apply patches from Calcipy for Github Actions
- remove AppVeyor completely

### Feat

- remove Sourcery and DeepSource

## 0.5.3 (2022-02-23)

### Fix

- correct issues with templates

## 0.5.2 (2022-02-23)

### Fix

- escape curly brackets on two lines

## 0.5.1 (2022-02-23)

### Fix

- correctly escape brackets

## 0.5.0 (2022-02-23)

### Feat

- add shellcheck as a pre-commit task!
- add fix to pre-commit for cassettes
- drop Appveyor
- add Github Actions developer for Calcipy

### Fix

- merge action fixes from calcipy

## 0.4.2 (2022-02-20)

### Feat

- add beautysh

## 0.4.1 (2022-02-20)

### Refactor

- apply mdformat

### Fix

- use author name in Github templates

## 0.4.0 (2022-02-20)

### Feat

- add mdformat pre-commit
- remove pyup

## 0.3.6 (2022-02-18)

## 0.3.5 (2022-02-18)

### Feat

- **#3**: add Changelog link for PyPi to toml

## 0.3.4 (2022-02-18)

### Fix

- replace git url with published cz_legacy package on PyPi

## 0.3.3 (2022-02-18)

## 0.3.2 (2022-02-18)

### Refactor

- more yaml corrections

## 0.3.1 (2022-02-18)

## 0.3.0 (2022-02-17)

### Refactor

- resolve yaml inconsistencies
- apply yamlfix
- remove workarounds of beartype type warning

### Fix

- tables.js should be in doc_dir

## 0.2.3 (2021-12-08)

### Fix

- update gitignore for doc files

## 0.2.2 (2021-12-08)

### Feat

- add placeholder check_imports
- add CNAME

### Fix

- make migration more reliable
- repair copier tasks and merge with calcipy improvements

## 0.2.1 (2021-06-06)

### Fix

- 0.2.0 was failing with [[ -f ... ]]  check

## 0.2.0 (2021-06-05)

## 0.0.11 (2021-06-05)

### Fix

- errors found in troubleshooting the calcipy test_project

## 0.0.10 (2021-06-05)

### Fix

- remove rstrip - leave up to user to fix
- try to rstrip trailing slashes from doc_dir

## 0.0.9 (2021-06-05)

### Feat

- move isort into toml
- move docs into subdirectory for calcipy 0.2.0

## 0.0.8 (2021-06-04)

### Feat

- apply improvements from calcipy

### Refactor

- apply yaml lint fixes

### Fix

- accidentally dropped .jinja from bug report

## 0.0.7 (2021-05-26)

### Fix

- correct errors in 0.0.6. Fix doc_dir path

## 0.0.6 (2021-05-26)

### Feat

- apply updates for calcipy  ad148bc

### Fix

- use an empty string if extras are None

## 0.0.5 (2021-05-23)

### Feat

- add AppVeyor and new questions

### Fix

- add note to set to push for labeler

## 0.0.4 (2021-04-25)

### Fix

- isort file should have isort (not settings)

## 0.0.3 (2021-04-25)

### Fix

- correct last error in package_name_py

## 0.0.2 (2021-04-25)

### Fix

- minor errors in 0.0.1

## 0.0.1 (2021-04-25)

### Feat

- add default pytest files from calcipy
- initialize copier project

### Fix

- move isort to separate file
