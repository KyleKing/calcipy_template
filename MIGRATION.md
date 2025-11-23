# Migration Guide: Poetry to uv

This template has migrated from Poetry to [uv](https://docs.astral.sh/uv/) for faster dependency management and better performance.

## For Existing Projects

If you're updating an existing project that uses this template, the migration process is automated through the `_copier_post_generation.py` script:

### What Happens Automatically

When you run `copier update`:

1. **Files Removed:**
   - `poetry.lock` - Will be replaced by `uv.lock`
   - `poetry.toml` - No longer needed
   - `.venv/` - Will be recreated by uv

2. **Files Updated:**
   - `.pre-commit-config.yaml` - References to `poetry.lock` → `uv.lock` and `poetry run` → `uv run`
   - `pyproject.toml` - Migrated from Poetry format to PEP 621 standard format
   - GitHub Actions workflows - Updated to use uv instead of Poetry
   - `run` script - Changed from `poetry run` to `uv run`

### Manual Steps Required

1. **Install uv:**
   ```sh
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. **After copier update completes:**
   ```sh
   # Sync dependencies (creates .venv and uv.lock)
   uv sync

   # Verify everything works
   ./run --help
   ./run main --keep-going
   ```

3. **Commit the changes:**
   ```sh
   git add .
   git commit -m "chore: migrate from Poetry to uv"
   git add uv.lock
   git commit -m "chore: add uv.lock"
   ```

## Key Differences

### Command Mapping

| Poetry Command | uv Equivalent |
|---|---|
| `poetry install` | `uv sync` |
| `poetry add <package>` | `uv add <package>` |
| `poetry add --group dev <package>` | `uv add --dev <package>` |
| `poetry remove <package>` | `uv remove <package>` |
| `poetry run <command>` | `uv run <command>` |
| `poetry shell` | No direct equivalent, use `uv run` |
| `poetry show` | `uv pip list` |
| `poetry lock` | `uv lock` |
| `poetry update` | `uv lock --upgrade` |

### Configuration Changes

**pyproject.toml format:**

```toml
# Before (Poetry)
[tool.poetry]
name = "my-package"
version = "1.0.0"
description = "My package"

[tool.poetry.dependencies]
python = "^3.10"
requests = "^2.28"

[tool.poetry.group.dev.dependencies]
pytest = "^7.0"

# After (uv/PEP 621)
[project]
name = "my-package"
version = "1.0.0"
description = "My package"
requires-python = ">=3.10"
dependencies = ["requests>=2.28"]

[dependency-groups]
dev = ["pytest>=7.0"]

[build-system]
build-backend = "uv_build"
requires = ["uv_build>=0.9.10"]
```

### Lock Files

- **Poetry:** `poetry.lock` (TOML format)
- **uv:** `uv.lock` (TOML format, but different structure)

Both lock files should be committed to version control.

## Troubleshooting

### Issue: "uv: command not found"

Solution: Install uv following the instructions above, then restart your terminal.

### Issue: Missing dependencies after migration

Solution: Run `uv sync` to install all dependencies from the lock file.

### Issue: Pre-commit hooks failing

Solution: Update pre-commit hooks:
```sh
uv run pre-commit autoupdate
uv run pre-commit run --all-files
```

### Issue: GitHub Actions failing

Solution: The migration should have updated all workflows automatically. If you have custom workflows, update them to use:
```yaml
- uses: astral-sh/setup-uv@v7
  with:
    python-version: ${{ matrix.python-version }}
```

## Benefits of uv

1. **Speed:** 10-100x faster than Poetry for dependency resolution
2. **Standard:** Uses PEP 621 format (future-proof)
3. **Compatibility:** Works with existing pip/PyPI ecosystem
4. **Size:** Smaller tool footprint
5. **Development:** Actively maintained by Astral (creators of Ruff)

## Reference

- [uv Documentation](https://docs.astral.sh/uv/)
- [PEP 621](https://peps.python.org/pep-0621/) - Storing project metadata in pyproject.toml
- [calcipy PR #139](https://github.com/KyleKing/calcipy/pull/139) - Original migration
