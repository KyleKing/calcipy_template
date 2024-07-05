"""Sync top-level pyproject.toml."""

from pathlib import Path

import tomlkit

# PLANNED: use this logic for Configapult when merging dependencies and versions!


def merge() -> None:
    """Merge ctt output into top-level pyproject.toml."""
    ctt_subdir = '.ctt/default'
    ctt_pyproject = Path(ctt_subdir) / 'pyproject.toml'
    ctt_doc = tomlkit.parse(ctt_pyproject.read_text())

    tl_pyproject = Path('pyproject.toml')
    tl_doc = tomlkit.parse(tl_pyproject.read_text())

    for key in ('ruff',):
        tl_doc['tool'][key] = ctt_doc['tool'][key]

    per_file_ignores = tl_doc['tool']['ruff']['lint']['per-file-ignores']
    for key in ('tests/*.py',):
        per_file_ignores[f'package_template/{key}'] = per_file_ignores[key]
        per_file_ignores[f'{ctt_subdir}/{key}'] = per_file_ignores[key]

    tl_pyproject.write_text(tomlkit.dumps(tl_doc))


if __name__ == '__main__':
    merge()
