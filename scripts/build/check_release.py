import os
import re
from pathlib import Path

from git import Repo
import toml


def get_git_version():
    repo = Repo()
    assert not repo.bare
    tag_strings = [t.name for t in repo.tags]
    tag_strings.sort(reverse=True)
    
    if len(tag_strings) > 0:
        latest_tag = tag_strings[0].strip()
        return latest_tag
    else:
        return None


def get_poetry_version():
    parsed_toml = toml.load('pyproject.toml')
    return parsed_toml["tool"]["poetry"]["version"].strip()


def get_change_log_version():
    # Path overloads __truediv__
    path_to_changelog = Path(__file__).parent / ".." / ".." / "doc" / "changes" / "changelog.md"
    with open(path_to_changelog) as changelog:
        changelog_str = changelog.read()
        # Search for the FIRST pattern like: "* [0.5.0](changes_0.5.0.md)" in the changelog file.
        # Note that we encapsulate the [(0.5.0)] with parenthesis, which tells re to return the matching string as group
        version_match = re.search(r"\* \[([0-9]+.[0-9]+.[0-9]+)]\(\S+\)", changelog_str)
        return version_match.groups()[0]


if __name__ == '__main__':
    poetry_version = get_poetry_version()
    latest_tag = get_git_version()
    changelog_version = get_change_log_version()
    print(f'Changelog version: "{changelog_version}"')
    print(f'Current version: "{poetry_version}"')
    print(f'Latest git tag: "{latest_tag}"')


    if latest_tag is None and poetry_version != "0.1.0":
        raise ValueError("You don't have yet a release. Your Poetry version needs to be 0.1.0!")

    # We expect that the current version in pyproject.toml is always greater than the latest tag.
    # Thus we avoid creating a release without having the version number updated.
    if poetry_version == latest_tag:
        raise ValueError("Poetry version needs to be updated!")

    if changelog_version != poetry_version:
        raise ValueError("Poetry version differs from Changelog version!")

    print("Everything looks good")
