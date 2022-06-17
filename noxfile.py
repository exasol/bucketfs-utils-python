import nox


@nox.session
def build_html_doc(session):
    BASE_PATH = session.run("git", "rev-parse", "--show-toplevel", silent=True)
    with session.chdir(BASE_PATH[:-1] + "/doc"):
        session.run("sphinx-apidoc", "-T", "-e", "-o", "api", "../exasol_bucketfs_utils_python")
        session.run("sphinx-build", "-b", "html", "-W", ".", ".build-docu")


@nox.session
def open_html_doc(session):
    BASE_PATH = session.run("git", "rev-parse", "--show-toplevel", silent=True)
    with session.chdir(BASE_PATH[:-1] + "/doc"):
        session.run("xdg-open", ".build-docu/index.html")


@nox.session
def build_and_open_html_doc(session):
    BASE_PATH = session.run("git", "rev-parse", "--show-toplevel", silent=True)
    with session.chdir(BASE_PATH[:-1] + "/doc"):
        session.run("sphinx-apidoc", "-T", "-e", "-o", "api", "../exasol_bucketfs_utils_python")
        session.run("sphinx-build", "-b", "html", "-W", ".", ".build-docu")
        session.run("xdg-open", ".build-docu/index.html")


@nox.session
def commit_pages_main(session):
    BASE_PATH = session.run("git", "rev-parse", "--show-toplevel", silent=True)
    with session.chdir(BASE_PATH[:-1]):
        session.run("sgpg",
                    "--target_branch", "github-pages/main",
                    "--push_origin", "origin",
                    "--push_enabled", "commit",
                    "--source_branch", "main",
                    "--module_path", "${StringArray[@]}",
                    env={"StringArray":("../exasol-bucketfs-utils-python")})


@nox.session
def commit_pages_current(session):
    BASE_PATH = session.run("git", "rev-parse", "--show-toplevel", silent=True)
    branch = session.run("git", "branch", "--show-current", silent=True)
    with session.chdir(BASE_PATH[:-1]):
        session.run("sgpg",
                    "--target_branch", "github-pages" + branch,
                    "--push_origin", "origin",
                    "--push_enabled", "commit",
                    "--module_path", "${StringArray[@]}",
                    env={"StringArray": ("../exasol-bucketfs-utils-python")})


@nox.session
def push_pages_main(session):
    BASE_PATH = session.run("git", "rev-parse", "--show-toplevel", silent=True)
    with session.chdir(BASE_PATH[:-1]):
        session.run("sgpg",
                    "--target_branch", "github-pages/main",
                    "--push_origin", "origin",
                    "--push_enabled", "push",
                    "--source_branch", "main",
                    "--module_path", "${StringArray[@]}",
                    env={"StringArray": ("../exasol-bucketfs-utils-python")})


@nox.session
def push_pages_current(session):
    BASE_PATH = session.run("git", "rev-parse", "--show-toplevel", silent=True)
    branch = session.run("git", "branch", "--show-current", silent=True)
    with session.chdir(BASE_PATH[:-1]):
        session.run("sgpg",
                    "--target_branch", "github-pages" + branch,
                    "--push_origin", "origin",
                    "--push_enabled", "push",
                    "--module_path", "${StringArray[@]}",
                    env={"StringArray": ("../exasol-bucketfs-utils-python")})


@nox.session
def push_pages_release(session):
    BASE_PATH = session.run("git", "rev-parse", "--show-toplevel", silent=True)
    tag = session.run("git", "tag", "--sort=committerdate", "|", "tail", "-1")
    with session.chdir(BASE_PATH[:-1]):
        session.run("sgpg",
                    "--target_branch", "github-pages/main",
                    "--push_origin", "origin",
                    "--push_enabled", "push",
                    "--source_branch",  tag,
                    "--source_origin", "tags",
                    "--module_path", "${StringArray[@]}",
                    env={"StringArray": ("../exasol-bucketfs-utils-python")})


@nox.session
def run_tests(session):
    session.run("pytest", "tests")
