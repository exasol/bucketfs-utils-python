#!/bin/bash
set -x
PUSH_ORIGIN="$2"
PUSH_ENABLED="$3"
SOURCE_BRANCH="$4"

set -euo pipefail

detect_source_branch() {
  CURRENT_BRANCH="$(git rev-parse --abbrev-ref HEAD)"
  if [ -z "$SOURCE_BRANCH" ]; then
    if [ -z "$CURRENT_BRANCH" ]; then
      echo "Abort. Could detect current branch and no source branch given."
      exit 1
    fi
    SOURCE_BRANCH="$CURRENT_BRANCH"
  fi
  if [ "$SOURCE_BRANCH" != "$CURRENT_BRANCH" ]; then
    echo "Abort. Specified Source Branch doesn't correspond to the currently checked out branch $CURRENT_BRANCH."
    exit 1
  fi
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
  TARGET_BRANCH_EXISTS="$(git show-ref "refs/heads/$TARGET_BRANCH" || echo)"
  if [ -n "$TARGET_BRANCH_EXISTS" ]; then
    echo "Checkout existing branch $TARGET_BRANCH"
    git worktree add "$WORKTREE" "$TARGET_BRANCH"
  else
    echo "Checkout new branch $TARGET_BRANCH"
    git branch "$TARGET_BRANCH"
    git worktree add "$WORKTREE" "$TARGET_BRANCH"
    pushd "$WORKTREE"
    git reset --hard "$SOURCE_BRANCH"
    popd
  fi
}

build_and_copy_documentation() {
  echo "Build with sphinx"
  sphinx-build -M html "$SCRIPT_DIR" "$BUILD_DIR" -W

  echo "Generated HTML Output"
  HTML_OUTPUT_DIR="$BUILD_DIR/html/"
  ls -la "$HTML_OUTPUT_DIR"

  OUTPUT_DIR="${WORKTREE:?}/${SOURCE_BRANCH:?}"
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
  echo "Git commit"
  echo "BRANCH=$SOURCE_BRANCH" >.source
  echo "COMMIT_ID=$CURRENT_COMMIT_ID" >>.source
  git add .
  git diff-index --quiet HEAD || git commit --no-verify -m "Update documentation from source branch '$SOURCE_BRANCH' with commit id '$CURRENT_COMMIT_ID'"
  if [ -n "$PUSH_ORIGIN" ] && [ "$PUSH_ENABLED" == "push" ]; then
    git config --local user.email "opensource@exasol.com"
    git config --local user.name "GitHub Action"
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

detect_source_branch
checkout_target_branch_as_worktree
build_and_copy_documentation
git_commit_and_push
