"""Check calcipy_template's pinned GitHub Action SHAs (in `package_template/**/*.jinja`) for drift.

Pin convention: `owner/repo@<40-char-sha> # <label>`, where `<label>` is either a release tag
(e.g. `v7.6.0`, compared against the repo's latest release) or a tracked branch name (e.g.
`master`, `release/v1`, compared by SHA against that branch's current HEAD). This mirrors GitHub's
own SHA-pinning recommendation: the trailing comment is a human-readable label, the SHA is what
actually gets executed.
"""

import argparse
import json
import logging
import re
import sys
from pathlib import Path

from freshness.checkers import CheckResult, fetch_github_commit, fetch_github_release, is_outdated, render_report

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

REPO_ROOT = Path(__file__).resolve().parent.parent
PACKAGE_TEMPLATE = REPO_ROOT / 'package_template'
BRANCH_NAME = 'chore/freshness-gha-pins'
TITLE = 'chore(ci): bump pinned GitHub Action versions'

PIN_PATTERN = re.compile(r'uses:\s*([\w.\-]+/[\w.\-]+)@([0-9a-f]{40})\s*#\s*([\w./\-]+)')
_RELEASE_LABEL_PATTERN = re.compile(r'^v\d')


def _iter_jinja_files() -> list[Path]:
    return sorted(PACKAGE_TEMPLATE.rglob('*.jinja'))


def _find_pins(files: list[Path]) -> dict[tuple[str, str, str], list[Path]]:
    """Map each distinct (owner/repo, sha, label) pin to the files it appears in."""
    pins: dict[tuple[str, str, str], list[Path]] = {}
    for file_path in files:
        content = file_path.read_text(encoding='utf-8')
        for owner_repo, sha, label in PIN_PATTERN.findall(content):
            pins.setdefault((owner_repo, sha, label), []).append(file_path)
    return pins


def _display(label: str, sha: str) -> str:
    """Label a pin for the report; branch refs need their SHA to say anything useful."""
    return label if _RELEASE_LABEL_PATTERN.match(label) else f'{label}@{sha[:7]}'


def _resolve_latest(owner_repo: str, sha: str, label: str) -> tuple[str, str] | None:
    """Return the (new_sha, new_label) a pin should move to, or None if already current.

    Returns:
        None when the pin is up to date, or the repo/network call failed.

    """
    owner, repo = owner_repo.split('/', 1)
    if _RELEASE_LABEL_PATTERN.match(label):
        latest = fetch_github_release(owner, repo)
        if not latest:
            logger.warning('Could not fetch latest release for %s', owner_repo)
            return None
        if not is_outdated(label.lstrip('v'), latest):
            return None
        new_label = f'v{latest}'
        new_sha = fetch_github_commit(owner, repo, branch=new_label)
        if not new_sha:
            logger.warning('Could not resolve %s@%s to a commit', owner_repo, new_label)
            return None
        return new_sha, new_label

    latest_sha = fetch_github_commit(owner, repo, branch=label)
    if not latest_sha or latest_sha == sha:
        return None
    return latest_sha, label


def check(*, apply: bool) -> tuple[list[CheckResult], list[str]]:
    """Check every pinned GitHub Action for drift, optionally patching files in place.

    Returns:
        The per-pin results, and a list of "owner/repo: old -> new" upgrade summary lines.

    """
    files = _iter_jinja_files()
    pins = _find_pins(files)

    results = []
    upgrades = []
    for (owner_repo, sha, label), pin_files in pins.items():
        resolved = _resolve_latest(owner_repo, sha, label)
        drifted = resolved is not None
        new_sha, new_label = resolved or (sha, label)
        current_display, latest_display = _display(label, sha), _display(new_label, new_sha)
        results.append(CheckResult(owner_repo, pin_files[0].name, current_display, latest_display, drifted))

        if not drifted:
            continue
        upgrades.append(f'{owner_repo}: {current_display} -> {latest_display}')
        if apply:
            old_pin = f'{owner_repo}@{sha} # {label}'
            new_pin = f'{owner_repo}@{new_sha} # {new_label}'
            for file_path in pin_files:
                file_path.write_text(file_path.read_text(encoding='utf-8').replace(old_pin, new_pin), encoding='utf-8')

    return results, upgrades


def main() -> int:
    """Run the freshness check and optionally write a JSON summary for CI to consume.

    Returns:
        0 always; drift is reported via the JSON `upgrades` list, not the exit code.

    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--apply', action='store_true', help='Patch drifted pins in place')
    parser.add_argument('--output', type=Path, help='Write a JSON summary to this path')
    args = parser.parse_args()

    results, upgrades = check(apply=args.apply)
    logger.info(render_report(results))

    if args.output:
        body_lines = ['Bumped the following pinned GitHub Actions to their latest version:', '']
        body_lines += [f'- `{line}`' for line in upgrades]
        body_lines += ['', 'Opened automatically by the freshness check workflow.']
        args.output.write_text(
            json.dumps({
                'branch': BRANCH_NAME,
                'title': TITLE,
                'body': '\n'.join(body_lines),
                'upgrades': upgrades,
            }),
            encoding='utf-8',
        )

    return 0


if __name__ == '__main__':
    sys.exit(main())
