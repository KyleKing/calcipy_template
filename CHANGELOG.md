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
