#!/bin/bash
set -x

PUSH_ORIGIN="$2"
PUSH_ENABLED="$3"
SOURCE_BRANCH="$4"

set -euo pipefail

detect_or_verify_source_branch() {
  CURRENT_BRANCH="$(git rev-parse --abbrev-ref HEAD)"
  if [ -z "$SOURCE_BRANCH" ]; then
    if [ -z "$CURRENT_BRANCH" ]; then
      echo "Abort. Could not detect current branch and no source branch given."
      exit 1
    fi
    SOURCE_BRANCH="$CURRENT_BRANCH"
  fi
  if [ "$SOURCE_BRANCH" != "$CURRENT_BRANCH" ]; then
    echo "Abort. Specified Source Branch doesn't correspond to the currently checked out branch $CURRENT_BRANCH."
    exit 1
  fi
  echo "Detected current branch $CURRENT_BRANCH"
}

cleanup_trap() {
  if [ -e "$WORKTREE" ]; then
    echo "Cleanup git worktree $WORKTREE"
    git worktree remove --force "$WORKTREE" || echo "Removing worktree $WORKTREE failed"
  fi
  echo "Cleanup temporary directory $TMP"
  rm -rf "$TMP"
}

checkout_target_branch_as_worktree() {
  TARGET_BRANCH_EXISTS="$(git show-branch "remotes/origin/$TARGET_BRANCH" || echo)"
  if [ -n "$TARGET_BRANCH_EXISTS" ]; then
    echo "Create worktree from existing branch $TARGET_BRANCH"
    git worktree add "$WORKTREE" "$TARGET_BRANCH"
  else
    echo "Create worktree from new branch $TARGET_BRANCH"
    # We need to create the worktree directly with the TARGET_BRANCH,
    # because every other branch could be already checked out
    git branch "$TARGET_BRANCH"
    git worktree add "$WORKTREE" "$TARGET_BRANCH"
    pushd "$WORKTREE"
    # We need to set the TARGET_BRANCH to the default branch
    # The default branch from github for pages is gh-pages, but you can change that.
    # Not using the default branch actually has benefits, because the branch gh-pages enforces some things.
    # We use github-pages/main with separate history for Github Pages,
    # because automated commits to the main branch can cause problems and
    # we don't want to mix the generated documentation with sources.
    # Furthermore, Github Pages expects a certain directory structure in the repository
    # which we only can provide with a separate history.
    GH_PAGES_ROOT_BRANCH=github-pages/root # is needed to temporarly create a new root commit
    GH_PAGES_MAIN_BRANCH=github-pages/main
    GH_PAGES_MAIN_BRANCH_EXISTS="$(git show-ref "refs/heads/$PUSH_ORIGIN/$GH_PAGES_MAIN_BRANCH" || echo)"
    if [ -n "$GH_PAGES_MAIN_BRANCH_EXISTS" ]
    then
      git reset --hard "$PUSH_ORIGIN/$GH_PAGES_MAIN_BRANCH"
    else
      echo "Creating a new empty root commit for the Github Pages in root branch $GH_PAGES_ROOT_BRANCH."
      git checkout --orphan "$GH_PAGES_ROOT_BRANCH"
      git reset --hard
      git commit --no-verify --allow-empty -m 'Initial empty commit for Github Pages'
      echo "Reset target branch $TARGET_BRANCH to root branch $GH_PAGES_ROOT_BRANCH"
      git checkout "$TARGET_BRANCH"
      git reset --hard "$GH_PAGES_ROOT_BRANCH"
      echo "Delete root branch $GH_PAGES_ROOT_BRANCH"
      git branch -D "$GH_PAGES_ROOT_BRANCH"
    fi
    popd
  fi
}

build_and_copy_documentation() {
  echo "Build api-doc"
  sphinx-apidoc -T -d 1 --separate -o "$SCRIPT_DIR/api" "$SCRIPT_DIR/../exasol_bucketfs_utils_python"

  echo "Build with sphinx"
  sphinx-build -M html "$SCRIPT_DIR" "$BUILD_DIR" -W

  echo "Generated HTML Output"
  HTML_OUTPUT_DIR="$BUILD_DIR/html/"
  echo "Using HTML_OUTPUT_DIR=$HTML_OUTPUT_DIR"
  ls -la "$HTML_OUTPUT_DIR"

  OUTPUT_DIR="${WORKTREE:?}/${SOURCE_BRANCH:?}"
  echo "Using OUTPUT_DIR=$OUTPUT_DIR"
  if [ -e "${OUTPUT_DIR}" ]; then
    echo "Removing existing output directory $OUTPUT_DIR"
    rm -rf "${OUTPUT_DIR}"
  fi
  echo "Creating output directory $OUTPUT_DIR"
  mkdir -p "$OUTPUT_DIR"
  echo "Copying HTML output $HTML_OUTPUT_DIR to the output directory $OUTPUT_DIR"
  find "$HTML_OUTPUT_DIR" -mindepth 1 -maxdepth 1 -exec mv -t "$OUTPUT_DIR" -- {} +
  echo "Content of output directory $OUTPUT_DIR"
  touch "$WORKTREE/.nojekyll"
  ls -la "$OUTPUT_DIR"
}

git_commit_and_push() {
  pushd "$WORKTREE"
  echo "Current directory before commit and push $PWD"
  echo "Git commit"
  echo "BRANCH=$SOURCE_BRANCH" >.source
  echo "COMMIT_ID=$CURRENT_COMMIT_ID" >>.source
  git add .
  git diff-index --quiet HEAD || git commit --no-verify -m "Update documentation from source branch '$SOURCE_BRANCH' with commit id '$CURRENT_COMMIT_ID'"
  if [ -n "$PUSH_ORIGIN" ] && [ "$PUSH_ENABLED" == "push" ]; then
    echo "Git push $PUSH_ORIGIN $TARGET_BRANCH"
    git push "$PUSH_ORIGIN" "$TARGET_BRANCH"
  fi
  popd
}

SCRIPT_DIR="$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")"

TMP="$(mktemp -d)"
WORKTREE="$TMP/worktree"
BUILD_DIR="$TMP/build"
trap 'cleanup_trap' EXIT

TARGET_BRANCH="$1"
CURRENT_COMMIT_ID="$(git rev-parse HEAD)"

echo "Commandline parameter"
echo "TARGET_BRANCH=$TARGET_BRANCH"
echo "PUSH_ORIGIN=$PUSH_ORIGIN"
echo "PUSH_ENABLED=$PUSH_ENABLED"
echo "SOURCE_BRANCH=$SOURCE_BRANCH"
echo
echo "Using following Directories:"
echo "TMP=$TMP"
echo "TMP=$TMP"
echo "WORKTREE=$WORKTREE"
echo "BUILD_DIR=$BUILD_DIR"
echo "CURRENT_COMMIT_ID=$CURRENT_COMMIT_ID"
echo
detect_or_verify_source_branch
checkout_target_branch_as_worktree
build_and_copy_documentation
git_commit_and_push
