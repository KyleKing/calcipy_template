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
