"""Sync top-level pyproject.toml."""

from pathlib import Path

import tomlkit


def merge() -> None:
    """Merge ctt output into top-level pyproject.toml."""
    ctt_pyproject = Path('.ctt/default/pyproject.toml')
    ctt_doc = tomlkit.parse(ctt_pyproject.read_text())

    tl_pyproject = Path('pyproject.toml')
    tl_doc = tomlkit.parse(tl_pyproject.read_text())

    for tool in ('commitizen', 'poetry'):
        ctt_doc['tool'][tool] = tl_doc['tool'][tool]
    tl_pyproject.write_text(tomlkit.dumps(ctt_doc))


if __name__ == '__main__':
    merge()
