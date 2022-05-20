import exasol_sphinx_github_pages_generator.deploy_github_pages as deploy_github_pages
import sys

if __name__ == "__main__":
    deploy_github_pages.deploy_github_pages(sys.argv[1:])
