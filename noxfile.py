import webbrowser
from pathlib import Path

import nox

nox.options.sessions = []


def _get_base_path(session: nox.Session):
    BASE_PATH = session.run("git", "rev-parse", "--show-toplevel", silent=True)
    return BASE_PATH


def _build_html_doc(session: nox.Session):
    session.run("sphinx-apidoc", "-T", "-e", "-o", "api", "../exasol_bucketfs_utils_python")
    session.run("sphinx-build", "-b", "html", "-W", ".", ".build-docu")


def _open_docs_in_browser(session: nox.Session):
    index_file_path = Path(".build-docu/index.html").resolve()
    webbrowser.open_new_tab(index_file_path.as_uri())


@nox.session
def build_html_doc(session: nox.Session):
    BASE_PATH = _get_base_path(session)
    with session.chdir(BASE_PATH[:-1] + "/doc"):
        _build_html_doc(session)


@nox.session
def open_html_doc(session: nox.Session):
    BASE_PATH = _get_base_path(session)
    with session.chdir(BASE_PATH[:-1] + "/doc"):
        _open_docs_in_browser(session)


@nox.session
def build_and_open_html_doc(session: nox.Session):
    BASE_PATH = _get_base_path(session)
    with session.chdir(BASE_PATH[:-1] + "/doc"):
        _build_html_doc(session)
        _open_docs_in_browser(session)


@nox.session
def commit_pages_main(session: nox.Session):
    BASE_PATH = _get_base_path(session)
    with session.chdir(BASE_PATH[:-1]):
        session.run("sgpg",
                    "--target_branch", "github-pages/main",
                    "--push_origin", "origin",
                    "--push_enabled", "commit",
                    "--source_branch", "main",
                    "--module_path", "${StringArray[@]}",
                    env={"StringArray": ("../exasol-bucketfs-utils-python")})


@nox.session
def commit_pages_current(session: nox.Session):
    BASE_PATH = _get_base_path(session)
    branch = session.run("git", "branch", "--show-current", silent=True)
    with session.chdir(BASE_PATH[:-1]):
        session.run("sgpg",
                    "--target_branch", "github-pages/" + branch[:-1],
                    "--push_origin", "origin",
                    "--push_enabled", "commit",
                    "--module_path", "${StringArray[@]}",
                    env={"StringArray": ("../exasol-bucketfs-utils-python")})


@nox.session
def push_pages_main(session: nox.Session):
    BASE_PATH = _get_base_path(session)
    with session.chdir(BASE_PATH[:-1]):
        session.run("sgpg",
                    "--target_branch", "github-pages/main",
                    "--push_origin", "origin",
                    "--push_enabled", "push",
                    "--source_branch", "main",
                    "--module_path", "${StringArray[@]}",
                    env={"StringArray": ("../exasol-bucketfs-utils-python")})


@nox.session
def push_pages_current(session: nox.Session):
    BASE_PATH = _get_base_path(session)
    branch = session.run("git", "branch", "--show-current", silent=True)
    with session.chdir(BASE_PATH[:-1]):
        session.run("sgpg",
                    "--target_branch", "github-pages/" + branch[:-1],
                    "--push_origin", "origin",
                    "--push_enabled", "push",
                    "--module_path", "${StringArray[@]}",
                    env={"StringArray": ("../exasol-bucketfs-utils-python")})


@nox.session
def push_pages_release(session: nox.Session):
    BASE_PATH = _get_base_path(session)
    tags = session.run("git", "tag", "--sort=committerdate", silent=True)
    # get the latest tag. last element in list is empty string, so choose second to last
    tag = tags.split("\n")[-2]
    with session.chdir(BASE_PATH[:-1]):
        session.run("sgpg",
                    "--target_branch", "github-pages/main",
                    "--push_origin", "origin",
                    "--push_enabled", "push",
                    "--source_branch", tag,
                    "--source_origin", "tags",
                    "--module_path", "${StringArray[@]}",
                    env={"StringArray": ("../exasol-bucketfs-utils-python")})


@nox.session
def run_tests(session: nox.Session):
    BASE_PATH = _get_base_path(session)
    with session.chdir(BASE_PATH[:-1]):
        session.run("pytest", "tests")
