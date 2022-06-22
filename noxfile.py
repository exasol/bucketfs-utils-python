import webbrowser
from pathlib import Path

import nox

nox.options.sessions = []


def _get_base_path(session: nox.Session):
    base_path = session.run("git", "rev-parse", "--show-toplevel", silent=True)
    return base_path


def _build_html_doc(session: nox.Session):
    session.run("sphinx-apidoc", "-T", "-e", "-o", "api", "../exasol_bucketfs_utils_python")
    session.run("sphinx-build", "-b", "html", "-W", ".", ".build-docu")


def _open_docs_in_browser(session: nox.Session):
    index_file_path = Path(".build-docu/index.html").resolve()
    webbrowser.open_new_tab(index_file_path.as_uri())


@nox.session(name="build-html-doc", python=None)
def build_html_doc(session: nox.Session):
    """Build the documentation for current checkout"""
    base_path = _get_base_path(session)
    with session.chdir(base_path[:-1] + "/doc"):
        _build_html_doc(session)


@nox.session(name="open-html-doc", python=None)
def open_html_doc(session: nox.Session):
    """Open the documentation for current checkout in the browser"""
    base_path = _get_base_path(session)
    with session.chdir(base_path[:-1] + "/doc"):
        _open_docs_in_browser(session)


@nox.session(name="build-and-open-html-doc", python=None)
def build_and_open_html_doc(session: nox.Session):
    """Build and open the documentation for current checkout in browser"""
    base_path = _get_base_path(session)
    with session.chdir(base_path[:-1] + "/doc"):
        _build_html_doc(session)
        _open_docs_in_browser(session)


@nox.session(name="commit-pages-main", python=None)
def commit_pages_main(session: nox.Session):
    """
    Generate the GitHub pages documentation for the main branch and
    commit it to the branch github-pages/main
    """
    base_path = _get_base_path(session)
    with session.chdir(base_path[:-1]):
        session.run("sgpg",
                    "--target_branch", "github-pages/main",
                    "--push_origin", "origin",
                    "--push_enabled", "commit",
                    "--source_branch", "main",
                    "--module_path", "${StringArray[@]}",
                    env={"StringArray": ("../exasol-bucketfs-utils-python")})


@nox.session(name="commit-pages-current", python=None)
def commit_pages_current(session: nox.Session):
    """
    Generate the GitHub pages documentation for the current branch and
    commit it to the branch github-pages/<current_branch>
    """
    base_path = _get_base_path(session)
    branch = session.run("git", "branch", "--show-current", silent=True)
    with session.chdir(base_path[:-1]):
        session.run("sgpg",
                    "--target_branch", "github-pages/" + branch[:-1],
                    "--push_origin", "origin",
                    "--push_enabled", "commit",
                    "--module_path", "${StringArray[@]}",
                    env={"StringArray": ("../exasol-bucketfs-utils-python")})


@nox.session(name="push-pages-main", python=None)
def push_pages_main(session: nox.Session):
    """
    Generate the GitHub pages documentation for the main branch and
    pushes it to the remote branch github-pages/main
    """
    base_path = _get_base_path(session)
    with session.chdir(base_path[:-1]):
        session.run("sgpg",
                    "--target_branch", "github-pages/main",
                    "--push_origin", "origin",
                    "--push_enabled", "push",
                    "--source_branch", "main",
                    "--module_path", "${StringArray[@]}",
                    env={"StringArray": ("../exasol-bucketfs-utils-python")})


@nox.session(name="push-pages-current", python=None)
def push_pages_current(session: nox.Session):
    """
    Generate the GitHub pages documentation for the current branch and
    pushes it to the remote branch github-pages/<current_branch>
    """
    base_path = _get_base_path(session)
    branch = session.run("git", "branch", "--show-current", silent=True)
    with session.chdir(base_path[:-1]):
        session.run("sgpg",
                    "--target_branch", "github-pages/" + branch[:-1],
                    "--push_origin", "origin",
                    "--push_enabled", "push",
                    "--module_path", "${StringArray[@]}",
                    env={"StringArray": ("../exasol-bucketfs-utils-python")})


@nox.session(name="push-pages-release", python=None)
def push_pages_release(session: nox.Session):
    """Generate the GitHub pages documentation for the release and pushes it to the remote branch github-pages/main"""
    base_path = _get_base_path(session)
    tags = session.run("git", "tag", "--sort=committerdate", silent=True)
    # get the latest tag. last element in list is empty string, so choose second to last
    tag = tags.split("\n")[-2]
    with session.chdir(base_path[:-1]):
        session.run("sgpg",
                    "--target_branch", "github-pages/main",
                    "--push_origin", "origin",
                    "--push_enabled", "push",
                    "--source_branch", tag,
                    "--source_origin", "tags",
                    "--module_path", "${StringArray[@]}",
                    env={"StringArray": ("../exasol-bucketfs-utils-python")})


@nox.session(name="run-tests", python=None)
def run_tests(session: nox.Session):
    """Run the tests in the poetry environment"""
    base_path = _get_base_path(session)
    with session.chdir(base_path[:-1]):
        session.run("pytest", "tests")
