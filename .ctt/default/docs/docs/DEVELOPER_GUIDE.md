# Developer Notes

## Local Development

```sh
git clone https://github.com/user_ctt/test-template.git
cd test-template
uv sync --all-extras

# See the available tasks
uv run calcipy
# Or use a local 'run' file (so that 'calcipy' can be extended)
./run

# Run the default task list (lint, auto-format, test coverage, etc.)
./run main

# Make code changes and run specific tasks as needed:
./run lint.fix test
```

### Maintenance

Dependency upgrades can be accomplished with:

```sh
uv lock --upgrade
uv sync --all-extras
```

## Publishing

Publishing is automated via GitHub Actions using PyPI Trusted Publishing. Tag creation triggers automated publishing.

```sh
./run release              # Bumps version, creates tag, pushes → triggers publish
./run release --suffix=rc  # For pre-releases
```

### Initial Setup

One-time setup to enable PyPI Trusted Publishing:

**Configure GitHub Environments**

Repository Settings → Environments:
- Create `testpypi` environment (no protection rules)
- Create `pypi` environment with "Required reviewers" enabled

**Register Trusted Publishers**

TestPyPI: https://test.pypi.org/manage/account/publishing/
- PyPI Project Name: `test_template`
- Owner: `user_ctt`
- Repository: `test_template`
- Workflow: `publish.yml`
- Environment: `testpypi`

PyPI: https://pypi.org/manage/project/test_template/settings/publishing/
- Owner: `user_ctt`
- Repository: `test_template`
- Workflow: `publish.yml`
- Environment: `pypi`

### Manual Publishing

For emergency manual publish:

```sh
export UV_PUBLISH_TOKEN=pypi-...
uv build
uv publish
```

## Current Status

<!-- {cts} COVERAGE -->

<!-- {cte} -->
