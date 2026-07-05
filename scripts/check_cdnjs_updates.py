"""Check CDNJS dependencies for available updates."""

import json
import logging
import re
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


def fetch_cdnjs_library(library: str) -> dict[str, Any]:
    """Fetch library metadata from CDNJS API."""
    url = f'https://api.cdnjs.com/libraries/{library}?fields=name,description,homepage,repository,assets'

    with urllib.request.urlopen(url, timeout=10) as response:
        return json.load(response)


def fetch_github_release(owner: str, repo: str) -> dict[str, Any] | None:
    """Fetch latest release from GitHub API."""
    url = f'https://api.github.com/repos/{owner}/{repo}/releases/latest'

    req = urllib.request.Request(url)
    req.add_header('Accept', 'application/vnd.github.v3+json')

    try:
        with urllib.request.urlopen(req, timeout=10) as response:  # noqa: S310 (hardcoded https URL)
            return json.load(response)
    except urllib.error.HTTPError:
        return None


def get_current_version(file_path: Path, library: str) -> str | None:
    """Extract current version from mkdocs config file."""
    content = file_path.read_text(encoding='utf-8')

    # Match CDNJS URL pattern: //cdnjs.cloudflare.com/ajax/libs/{library}/{version}/...
    pattern = rf'cdnjs\.cloudflare\.com/ajax/libs/{re.escape(library)}/(\d+\.\d+\.\d+)'
    match = re.search(pattern, content)

    return match.group(1) if match else None


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


def get_latest_cdnjs_version(assets: list[dict[str, Any]]) -> str | None:
    """Get the latest version from CDNJS assets array."""
    versions = [version for asset in assets if (version := asset.get('version'))]

    if not versions:
        return None

    versions.sort(key=lambda v: [int(x) for x in v.split('.')])
    return versions[-1]


def resolve_latest_version(
    cdnjs_version: str | None,
    github_version: str | None,
) -> tuple[str, str] | None:
    """Pick the newer of the CDNJS and GitHub versions, if any are available."""
    if cdnjs_version and github_version:
        latest_version = cdnjs_version if compare_versions(github_version, cdnjs_version) else github_version
        return latest_version, 'CDNJS/GitHub'
    if cdnjs_version:
        return cdnjs_version, 'CDNJS'
    if github_version:
        return github_version, 'GitHub'
    return None


def report_file_status(file_path: Path, library: str, latest_version: str, github_info: tuple[str, str] | None) -> bool:
    """Log the update status for a single file and return whether an update is needed."""
    if not file_path.exists():
        logger.warning('  ⚠️  File not found: %s', file_path)
        return False

    current_version = get_current_version(file_path, library)
    if not current_version:
        logger.warning('  ⚠️  Could not extract version from %s', file_path)
        return False

    logger.info('  %s: %s', file_path, current_version)

    if not compare_versions(current_version, latest_version):
        logger.info('  ✓ Up to date')
        return False

    logger.info('  ✅ Update available: %s → %s', current_version, latest_version)
    if github_info:
        owner, repo = github_info
        logger.info('  📚 Changelog:')
        logger.info('     Releases: https://github.com/%s/%s/releases', owner, repo)
        logger.info('     Commits:  https://github.com/%s/%s/commits', owner, repo)

    return True


def check_library(library: str, files: list[Path]) -> bool:
    """Check a single library for updates."""
    try:
        data = fetch_cdnjs_library(library)
    except urllib.error.URLError:
        logger.exception('  ❌ Failed to fetch %s', library)
        return False

    github_info = get_github_info(data.get('repository'))
    github_release = fetch_github_release(*github_info) if github_info else None
    github_version = github_release.get('tag_name', '').lstrip('v') if github_release else None

    resolved = resolve_latest_version(get_latest_cdnjs_version(data.get('assets', [])), github_version)
    if not resolved:
        logger.warning('  ⚠️  Could not find latest version for %s', library)
        return False

    latest_version, version_source = resolved
    logger.info('  Latest version (%s): %s', version_source, latest_version)

    results = [report_file_status(file_path, library, latest_version, github_info) for file_path in files]
    return any(results)


def main() -> None:
    """Check CDNJS dependencies and report available updates."""
    logging.basicConfig(level=logging.INFO, format='%(message)s')

    libraries = {
        'tablesort': [
            Path('.ctt/default/mkdocs.yml'),
            Path('package_template/mkdocs.yml.jinja'),
        ],
    }

    updates_needed = False

    for library, files in libraries.items():
        logger.info('\nChecking %s...', library)
        if check_library(library, files):
            updates_needed = True

    if updates_needed:
        logger.info('\n⚠️  Updates are available!')
        logger.info('\nTo update, modify the CDNJS URLs in the files above.')
        logger.info('Review the changelog links before updating to check for breaking changes.')


if __name__ == '__main__':
    main()
