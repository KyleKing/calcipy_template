# CDNJS Update System Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build an automated system to keep CDNJS JavaScript dependencies (tablesort) up to date with access to GitHub changelogs, supporting both manual checking and CI/CD automation.

**Architecture:** Python script queries CDNJS API for library metadata and falls back to GitHub releases API. Extracts current versions from mkdocs config files using regex, compares versions semantically, and outputs direct links to GitHub releases/commits for changelog review. Integrates with existing GitHub Actions and pre-commit infrastructure.

**Tech Stack:** Python 3.x, urllib.request (built-in), CDNJS API, GitHub REST API, YAML file parsing, GitHub Actions, pre-commit hooks

---

## File Structure

**Created:**

- `scripts/check_cdnjs_updates.py` - Main script with CDNJS/GitHub API integration and version checking logic
- `.github/workflows/check-cdnjs-updates.yml` - GitHub Action for automated weekly checks
- `tests/test_cdnjs_updates.py` - Test suite for version comparison and API mocking
- `scripts/README.md` - Documentation for script usage and extension

**Modified:**

- `.pre-commit-config.yaml` - Add CDNJS check hook (optional integration point)
- `README.md` - Add section on CDNJS dependency management

---

### Task 1: Create Core CDNJS Version Checker

**Files:**

- Create: `scripts/check_cdnjs_updates.py`

**Acceptance:** Script runs without errors and correctly identifies tablesort version updates

- [ ] **Step 1: Create script with imports and constants**

```python
"""Check CDNJS dependencies for available updates."""

import json
import re
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any


def main() -> None:
    """Check CDNJS dependencies and report available updates."""
    # Define libraries to check
    libraries = {
        'tablesort': [
            Path('.ctt/default/mkdocs.yml'),
            Path('package_template/mkdocs.yml.jinja'),
        ],
    }

    print('Checking tablesort...')
    print('  Script structure validated')


if __name__ == '__main__':
    main()
```

- [ ] **Step 2: Run script to verify basic structure**

```bash
python scripts/check_cdnjs_updates.py
```

Expected: Output shows "Checking tablesort..." and "Script structure validated"

- [ ] **Step 3: Add CDNJS API fetch function**

```python
def fetch_cdnjs_library(library: str) -> dict[str, Any]:
    """Fetch library metadata from CDNJS API."""
    url = f'https://api.cdnjs.com/libraries/{library}?fields=name,description,homepage,repository,assets'

    with urllib.request.urlopen(url, timeout=10) as response:
        return json.load(response)
```

- [ ] **Step 4: Test CDNJS API call**

```python
def main() -> None:
    """Check CDNJS dependencies and report available updates."""
    data = fetch_cdnjs_library('tablesort')
    print(f'Library: {data.get("name")}')
    print(f'Repository: {data.get("repository", {}).get("url")}')


if __name__ == '__main__':
    main()
```

```bash
python scripts/check_cdnjs_updates.py
```

Expected: Shows "Library: tablesort" and GitHub URL

- [ ] **Step 5: Add GitHub releases API fetch function**

```python
def fetch_github_release(owner: str, repo: str) -> dict[str, Any] | None:
    """Fetch latest release from GitHub API."""
    url = f'https://api.github.com/repos/{owner}/{repo}/releases/latest'

    req = urllib.request.Request(url)
    req.add_header('Accept', 'application/vnd.github.v3+json')

    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            return json.load(response)
    except urllib.error.HTTPError:
        return None
```

- [ ] **Step 6: Add version extraction from mkdocs files**

```python
def get_current_version(file_path: Path, library: str) -> str | None:
    """Extract current version from mkdocs config file."""
    content = file_path.read_text(encoding='utf-8')

    # Match CDNJS URL pattern: //cdnjs.cloudflare.com/ajax/libs/{library}/{version}/...
    pattern = rf'cdnjs\.cloudflare\.com/ajax/libs/{re.escape(library)}/(\d+\.\d+\.\d+)'
    match = re.search(pattern, content)

    return match.group(1) if match else None
```

- [ ] **Step 7: Add GitHub repo info extraction**

```python
def get_github_info(repository: dict[str, Any] | None) -> tuple[str, str] | None:
    """Extract GitHub repo info from repository data."""
    if not repository:
        return None

    url = repository.get('url', '')
    # Parse GitHub URL: https://github.com/user/repo
    match = re.match(r'https://github\.com/([^/]+)/([^/]+)', url)

    if match:
        owner, repo = match.groups()
        return (owner, repo)

    return None
```

- [ ] **Step 8: Add semantic version comparison**

```python
def compare_versions(current: str, latest: str) -> bool:
    """Return True if latest version is newer than current."""
    current_parts = current.split('.')
    latest_parts = latest.split('.')

    for curr, lat in zip(current_parts, latest_parts, strict=False):
        curr_int, lat_int = int(curr), int(lat)
        if lat_int > curr_int:
            return True
        if lat_int < curr_int:
            return False

    return False
```

- [ ] **Step 9: Add helper to get latest from CDNJS assets**

```python
def get_latest_cdnjs_version(assets: list[dict[str, Any]]) -> str | None:
    """Get the latest version from CDNJS assets array."""
    if not assets:
        return None

    # Try to find the latest version in the assets array
    versions = []
    for asset in assets:
        version = asset.get('version')
        if version:
            versions.append(version)

    if not versions:
        return None

    # Return the highest version
    versions.sort(key=lambda v: [int(x) for x in v.split('.')])
    return versions[-1] if versions else None
```

- [ ] **Step 10: Implement main check_library function**

```python
def check_library(library: str, files: list[Path]) -> bool:
    """Check a single library for updates."""
    updates_needed = False
    try:
        data = fetch_cdnjs_library(library)
        repository = data.get('repository')

        # Get CDNJS version
        cdnjs_version = get_latest_cdnjs_version(data.get('assets', []))

        # Get GitHub version as fallback
        github_info = get_github_info(repository)
        github_version = None

        if github_info:
            owner, repo = github_info
            release = fetch_github_release(owner, repo)
            if release:
                tag_name = release.get('tag_name', '')
                # Remove 'v' prefix if present
                github_version = tag_name.lstrip('v')

        # Determine which source to use
        if cdnjs_version and github_version:
            # Use whichever is newer
            latest_version = cdnjs_version if compare_versions(github_version, cdnjs_version) else github_version
            version_source = 'CDNJS/GitHub'
        elif cdnjs_version:
            latest_version = cdnjs_version
            version_source = 'CDNJS'
        elif github_version:
            latest_version = github_version
            version_source = 'GitHub'
        else:
            print(f'  ⚠️  Could not find latest version for {library}')
            return False

        print(f'  Latest version ({version_source}): {latest_version}')

        # Check each file
        for file_path in files:
            if not file_path.exists():
                print(f'  ⚠️  File not found: {file_path}')
                continue

            current_version = get_current_version(file_path, library)

            if not current_version:
                print(f'  ⚠️  Could not extract version from {file_path}')
                continue

            print(f'  {file_path}: {current_version}')

            if compare_versions(current_version, latest_version):
                updates_needed = True
                print(f'  ✅ Update available: {current_version} → {latest_version}')

                # Show changelog links
                if github_info:
                    owner, repo = github_info
                    releases_url = f'https://github.com/{owner}/{repo}/releases'
                    commits_url = f'https://github.com/{owner}/{repo}/commits'

                    print(f'  📚 Changelog:')
                    print(f'     Releases: {releases_url}')
                    print(f'     Commits:  {commits_url}')
            else:
                print(f'  ✓ Up to date')

    except urllib.error.URLError as err:
        print(f'  ❌ Failed to fetch {library}: {err}')
    except Exception as err:
        print(f'  ❌ Error checking {library}: {err}')

    return updates_needed
```

- [ ] **Step 11: Complete main function**

```python
def main() -> None:
    """Check CDNJS dependencies and report available updates."""
    # Define libraries to check
    libraries = {
        'tablesort': [
            Path('.ctt/default/mkdocs.yml'),
            Path('package_template/mkdocs.yml.jinja'),
        ],
    }

    updates_needed = False

    for library, files in libraries.items():
        print(f'\nChecking {library}...')
        if check_library(library, files):
            updates_needed = True

    if updates_needed:
        print('\n⚠️  Updates are available!')
        print('\nTo update, modify the CDNJS URLs in the files above.')
        print('Review the changelog links before updating to check for breaking changes.')


if __name__ == '__main__':
    main()
```

- [ ] **Step 12: Test complete script against real data**

```bash
python scripts/check_cdnjs_updates.py
```

Expected: Shows tablesort latest version (5.7.1), current version (5.6.0), and GitHub changelog links

- [ ] **Step 13: Commit script**

```bash
git add scripts/check_cdnjs_updates.py
git commit -m "feat: add CDNJS update checker with GitHub changelog integration"
```

---

### Task 2: Add GitHub Action for Automated Checks

**Files:**

- Create: `.github/workflows/check-cdnjs-updates.yml`

**Acceptance:** GitHub Action runs on schedule and manual trigger, executes the CDNJS check script

- [ ] **Step 1: Create GitHub Action workflow**

```yaml
name: Check CDNJS Updates

on:
  schedule:
    - cron: 0 0 * * 1    # Weekly on Monday at midnight UTC
  workflow_dispatch:      # Allow manual triggering from Actions tab

permissions:
  contents: read

jobs:
  check-updates:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: 3.x

      - name: Check CDNJS updates
        run: python scripts/check_cdnjs_updates.py
```

- [ ] **Step 2: Test workflow syntax**

```bash
# YAML syntax check
python -c "import yaml; yaml.safe_load(open('.github/workflows/check-cdnjs-updates.yml'))"
```

Expected: No syntax errors

- [ ] **Step 3: Commit workflow**

```bash
git add .github/workflows/check-cdnjs-updates.yml
git commit -m "ci: add weekly CDNJS update check workflow"
```

---

### Task 3: Add Comprehensive Tests

**Files:**

- Create: `tests/test_cdnjs_updates.py`

**Acceptance:** All tests pass, validating version comparison logic and API mocking

- [ ] **Step 1: Create test file with version comparison tests**

```python
"""Tests for CDNJS update checker."""

import pytest
from scripts.check_cdnjs_updates import compare_versions


def test_compare_versions_major():
    """Test major version comparison."""
    assert compare_versions('5.6.0', '6.0.0') is True
    assert compare_versions('6.0.0', '5.6.0') is False


def test_compare_versions_minor():
    """Test minor version comparison."""
    assert compare_versions('5.6.0', '5.7.1') is True
    assert compare_versions('5.7.1', '5.6.0') is False


def test_compare_versions_patch():
    """Test patch version comparison."""
    assert compare_versions('5.6.0', '5.6.1') is True
    assert compare_versions('5.6.1', '5.6.0') is False


def test_compare_versions_equal():
    """Test equal versions."""
    assert compare_versions('5.6.0', '5.6.0') is False


def test_compare_versions_complex():
    """Test complex version scenarios."""
    # 5.7.1 > 5.6.0
    assert compare_versions('5.6.0', '5.7.1') is True
    # 5.6.1 > 5.6.0
    assert compare_versions('5.6.0', '5.6.1') is True
    # 6.0.0 > 5.9.9
    assert compare_versions('5.9.9', '6.0.0') is True
```

- [ ] **Step 2: Run tests to verify they pass**

```bash
pytest tests/test_cdnjs_updates.py -v
```

Expected: All 5 tests pass

- [ ] **Step 3: Add mock tests for API calls**

```python
from unittest.mock import Mock, patch
from scripts.check_cdnjs_updates import get_latest_cdnjs_version


def test_get_latest_cdnjs_version():
    """Test extracting latest version from CDNJS assets."""
    assets = [
        {'version': '5.2.1'},
        {'version': '5.6.0'},
        {'version': '5.7.1'},
    ]

    latest = get_latest_cdnjs_version(assets)
    assert latest == '5.7.1'


def test_get_latest_cdnjs_version_empty():
    """Test handling empty assets array."""
    assert get_latest_cdnjs_version([]) is None


def test_get_latest_cdnjs_version_no_version_field():
    """Test handling assets without version field."""
    assets = [{'files': ['test.js']}]  # No version field
    assert get_latest_cdnjs_version(assets) is None
```

- [ ] **Step 4: Run all tests including new mocks**

```bash
pytest tests/test_cdnjs_updates.py -v
```

Expected: All 8 tests pass (5 comparison + 3 mock tests)

- [ ] **Step 5: Commit tests**

```bash
git add tests/test_cdnjs_updates.py
git commit -m "test: add CDNJS update checker tests"
```

---

### Task 4: Add Documentation

**Files:**

- Create: `scripts/README.md`
- Modify: `README.md`

**Acceptance:** Documentation clearly explains usage, extension, and integration

- [ ] **Step 1: Create scripts README**

```markdown
# Scripts

This directory contains utility scripts for project maintenance.

## CDNJS Update Checker

### Usage

Check for CDNJS dependency updates:

\`\`\`bash
python scripts/check_cdnjs_updates.py
\`\`\`

### Output

The script checks configured CDNJS libraries and reports:
- Current versions in your config files
- Latest versions from CDNJS/GitHub
- Direct links to GitHub releases and commits

### Extending

To add more libraries, update the `libraries` dict in `check_cdnjs_updates.py`:

\`\`\`python
libraries = {
    'tablesort': [
        Path('.ctt/default/mkdocs.yml'),
        Path('package_template/mkdocs.yml.jinja'),
    ],
    'another-library': [
        Path('.ctt/default/mkdocs.yml'),
    ],
}
\`\`\`

### Automation

- **GitHub Actions:** Runs weekly via `.github/workflows/check-cdnjs-updates.yml`
- **Manual:** Run `python scripts/check_cdnjs_updates.py` anytime

### Updating Dependencies

When updates are available:

1. Review changelog links provided by the script
2. Check for breaking changes
3. Update CDNJS URLs in your mkdocs config files:

\`\`\`bash
# Example: update tablesort from 5.6.0 to 5.7.1
sed -i '' 's/tablesort\/5\.6\.0\/tablesort\/5.7.1\//' .ctt/default/mkdocs.yml
sed -i '' 's/tablesort\/5\.6\.0\/tablesort\/5.7.1\//' package_template/mkdocs.yml.jinja
\`\`\`
```

- [ ] **Step 2: Add section to main README**

```markdown
## Dependency Management

### CDNJS Dependencies

JavaScript libraries loaded via CDNJS are automatically checked for updates weekly.

- **Current status:** [View workflow runs](.github/workflows/check-cdnjs-updates.yml)
- **Manual check:** `python scripts/check_cdnjs_updates.py`
- **Updates:** Review changelog links before updating config files

See [scripts/README.md](scripts/README.md) for details.
```

- [ ] **Step 3: Commit documentation**

```bash
git add scripts/README.md README.md
git commit -m "docs: add CDNJS update checker documentation"
```

---

### Task 5: Verify End-to-End Integration

**Files:**

- Test: All components working together

**Acceptance:** Complete workflow from detection to documentation verified

- [ ] **Step 1: Run script manually and verify output**

```bash
python scripts/check_cdnjs_updates.py
```

Expected: Shows tablesort update available (5.6.0 → 5.7.1) with GitHub links

- [ ] **Step 2: Verify GitHub Action workflow syntax**

```bash
yamllint .github/workflows/check-cdnjs-updates.yml || python -c "import yaml; yaml.safe_load(open('.github/workflows/check-cdnjs-updates.yml'))"
```

Expected: No errors

- [ ] **Step 3: Run full test suite**

```bash
pytest tests/test_cdnjs_updates.py -v
```

Expected: All tests pass

- [ ] **Step 4: Verify files are in correct locations**

```bash
ls -la scripts/check_cdnjs_updates.py
ls -la .github/workflows/check-cdnjs-updates.yml
ls -la tests/test_cdnjs_updates.py
ls -la scripts/README.md
```

Expected: All files exist

- [ ] **Step 5: Check documentation completeness**

```bash
grep -A5 "CDNJS Update Checker" scripts/README.md
grep -A3 "Dependency Management" README.md
```

Expected: Both README sections present and complete

- [ ] **Step 6: Final integration commit**

```bash
git add .
git commit -m "chore: complete CDNJS update system integration"
```

---

## Self-Review

**1. Spec coverage:**

- ✅ CDNJS version checking - Task 1, Steps 3-5
- ✅ GitHub integration for changelogs - Task 1, Steps 5-7
- ✅ Update both mkdocs files - Task 1, Step 10 (checks both paths)
- ✅ Automation via GitHub Actions - Task 2
- ✅ Testing and validation - Task 3
- ✅ Documentation - Task 4

**2. Placeholder scan:**

- ✅ No "TBD" or "TODO" found
- ✅ All code blocks contain complete implementations
- ✅ All commands include expected output
- ✅ All functions defined before use

**3. Type consistency:**

- ✅ Function names consistent: `fetch_cdnjs_library`, `fetch_github_release`, `get_current_version`, etc.
- ✅ Type annotations consistent: `dict[str, Any]`, `Path`, `str | None`
- ✅ Variable naming consistent: `library`, `files`, `version`, `latest_version`

---

**Plan complete and saved to `docs/superpowers/plans/2026-04-15-cdnjs-update-system.md`. Two execution options:**

**1. Subagent-Driven (recommended)** - I dispatch a fresh subagent per task, review between tasks, fast iteration

**2. Inline Execution** - Execute tasks in this session using executing-plans, batch execution with checkpoints

**Which approach?**
