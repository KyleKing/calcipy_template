# Testing Strategy for calcipy_template

This document outlines the testing strategy for the calcipy_template, including how to use copier-template-tester (CTT) for regression testing.

## Overview

The template uses [copier-template-tester](https://github.com/kyleking/copier-template-tester) to validate template generation and ensure changes don't break existing projects.

## Current Testing

### Pre-commit Hook

The `.pre-commit-config.yaml` includes a copier-template-tester hook:

```yaml
- repo: https://github.com/kyleking/copier-template-tester
  rev: 2.1.3
  hooks:
    - id: copier-template-tester
```

This runs automatically on commits and validates:
- Template syntax correctness
- Generated project structure
- Post-generation scripts execute successfully

### Manual Testing

Run CTT manually:

```sh
# Run all CTT checks
uv run pre-commit run --all-files copier-template-tester

# Or run CTT directly (if you have it installed)
ctt test
```

## Regression Testing Strategy

### Test Scenarios

To ensure the uv migration doesn't break existing functionality, test these scenarios:

#### 1. Fresh Project Generation

```sh
# Generate a new project from the template
copier copy --UNSAFE . ../test-fresh-project

cd ../test-fresh-project

# Verify uv.lock was generated
test -f uv.lock || echo "ERROR: uv.lock not found"

# Install dependencies
uv sync

# Run basic commands
./run --help
uv run calcipy --version

# Run tests
uv run calcipy-test test.pytest
```

#### 2. Existing Project Update (Poetry → uv)

```sh
# Create a test project with the OLD template version
git clone https://github.com/KyleKing/calcipy_template.git old-template
cd old-template
git checkout <last-poetry-commit>
copier copy --UNSAFE . ../test-update-project

cd ../test-update-project

# Set up the old Poetry environment
poetry install

# Create a commit
git add .
git commit -m "Initial commit with Poetry"

# Update to the NEW template with uv
copier update . --UNSAFE --conflict=rej

# Verify migration
test ! -f poetry.lock || echo "ERROR: poetry.lock still exists"
test -f uv.lock || echo "ERROR: uv.lock not created"

# Test functionality
uv sync
./run main --keep-going
```

#### 3. CI/CD Validation

After pushing changes:

1. Check GitHub Actions pass on the template repo itself
2. Check Actions pass on a generated project
3. Verify all matrix combinations (OS: ubuntu/macos/windows, Python versions)

### CTT Configuration

The `.ctt/default/` directory contains:
- Example project configuration
- Test files
- Expected outputs

When modifying the template, update `.ctt/default/` to match:

```sh
# After changing template files
cp package_template/pyproject.toml.jinja .ctt/default/pyproject.toml
# ... copy other changed files ...

# Process jinja templates manually or use test project
# Then test with CTT
uv run pre-commit run --all-files copier-template-tester
```

## Regression Test Checklist

Before releasing template changes:

- [ ] Fresh project generation works
  - [ ] `uv sync` succeeds
  - [ ] `./run --help` works
  - [ ] All calcipy tasks run
  - [ ] Pre-commit hooks install and run
  - [ ] Tests pass

- [ ] Existing project update works (simulate Poetry → uv)
  - [ ] Migration script removes Poetry files
  - [ ] `uv.lock` is generated
  - [ ] All workflows updated correctly
  - [ ] Pre-commit config updated

- [ ] GitHub Actions
  - [ ] Template repo Actions pass
  - [ ] Generated project Actions pass
  - [ ] All OS/Python matrix combinations work

- [ ] CTT validation passes
  - [ ] `copier-template-tester` pre-commit hook passes
  - [ ] No unexpected changes in `.ctt/default/`

- [ ] Documentation
  - [ ] README.md reflects uv usage
  - [ ] MIGRATION.md is comprehensive
  - [ ] Post-copy message is helpful

## Automated Regression Testing

### Option 1: CTT with Multiple Scenarios

Create multiple test scenarios in CTT:

```sh
# In .ctt/ directory, create subdirectories for different scenarios
.ctt/
  ├── default/          # Standard configuration
  ├── extends-calcipy/  # With extends_calcipy=true
  └── minimal-python/   # With minimum_python=3.9.13
```

### Option 2: Integration Tests in CI

Add a workflow to test template generation:

```yaml
name: Template Integration Tests

on: [push, pull_request]

jobs:
  test-generation:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup uv
        uses: astral-sh/setup-uv@v7

      - name: Install copier
        run: pipx install copier

      - name: Generate fresh project
        run: |
          copier copy --UNSAFE --defaults . ../test-project
          cd ../test-project
          uv sync
          uv run calcipy --version

      - name: Run generated project tests
        run: |
          cd ../test-project
          ./run main --keep-going
```

### Option 3: Snapshot Testing

Use CTT's snapshot feature to detect unexpected changes:

```sh
# Create baseline snapshots
ctt test --update-snapshots

# Future tests compare against snapshots
ctt test  # Fails if generated files differ from snapshots
```

## Continuous Improvement

- Review CTT output on every commit
- Update `.ctt/default/` when intentionally changing output
- Add new test scenarios as edge cases are discovered
- Document known issues or limitations
- Consider adding more comprehensive integration tests in CI

## Resources

- [copier-template-tester Documentation](https://github.com/kyleking/copier-template-tester)
- [Copier Documentation](https://copier.readthedocs.io/)
- [uv Documentation](https://docs.astral.sh/uv/)
