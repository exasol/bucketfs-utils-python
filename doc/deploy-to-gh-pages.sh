#!/bin/bash

set -euo pipefail

TARGET_BRANCH="$1"

SCRIPT_DIR="$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")"

cleanup(){
  if [ -e "$WORKTREE" ]
  then
    echo "Cleanup git worktree $WORKTREE"
	  git worktree remove --force "$WORKTREE" || echo "Removing worktree $WORKTREE failed"
  fi
  echo "Cleanup temporary directory $TMP"
	rm -rf $TMP
}

TMP="$(mktemp -d)"
WORKTREE="$TMP/worktree"
BUILD_DIR="$TMP/build"
trap 'cleanup' EXIT;
git worktree add "$WORKTREE" "$TARGET_BRANCH"
sphinx-build -M html "$SCRIPT_DIR" "$BUILD_DIR"
rm -rf  "$WORKTREE/"*
mv "$BUILD_DIR/html/"*  "$WORKTREE/"
SOURCE_COMMIT_ID="$(git rev-parse HEAD)"
SOURCE_BRANCH_NAME="$(git rev-parse --abbrev-ref HEAD)"
pushd "$WORKTREE"
echo "BRANCH=$SOURCE_BRANCH_NAME" > .source
echo "COMMIT_ID=$SOURCE_COMMIT_ID" >> .source
git add .
git commit --no-verify -m "Update documentation from source branch '$SOURCE_BRANCH_NAME' with commit id '$SOURCE_COMMIT_ID'"
popd
touch  "$WORKTREE/.nojekyll"
