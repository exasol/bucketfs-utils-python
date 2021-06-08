#!/bin/bash
set -x
PUSH_ORIGIN="$2"
PUSH_ENABLED="$3"

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
	rm -rf "$TMP"
}

TMP="$(mktemp -d)"
WORKTREE="$TMP/worktree"
BUILD_DIR="$TMP/build"
trap 'cleanup' EXIT;
TARGET_BRANCH_EXISTS="$(git show-ref "refs/heads/$TARGET_BRANCH" || echo)"
if [ -n "$TARGET_BRANCH_EXISTS" ]
then
  echo "Checkout existing branch $TARGET_BRANCH"
  git worktree add "$WORKTREE" "$TARGET_BRANCH"
else
  echo "Checkout new branch $TARGET_BRANCH"
  git worktree add -b "$TARGET_BRANCH" "$WORKTREE" "github-pages/main"
fi
sphinx-build -M html "$SCRIPT_DIR" "$BUILD_DIR" -W
rm -rf  "${WORKTREE:?}/"*
mv "$BUILD_DIR/html/"*  "$WORKTREE/"
SOURCE_COMMIT_ID="$(git rev-parse HEAD)"
SOURCE_BRANCH_NAME="$(git rev-parse --abbrev-ref HEAD)"
pushd "$WORKTREE"
echo "BRANCH=$SOURCE_BRANCH_NAME" > .source
echo "COMMIT_ID=$SOURCE_COMMIT_ID" >> .source
echo "Git commit"
git add .
git diff-index --quiet HEAD || git commit --no-verify -m "Update documentation from source branch '$SOURCE_BRANCH_NAME' with commit id '$SOURCE_COMMIT_ID'"
if [ -n "$PUSH_ORIGIN" ] && [ "$PUSH_ENABLED" == "push" ]
then
  echo "Git push $PUSH_ORIGIN $TARGET_BRANCH"
  git push "$PUSH_ORIGIN" "$TARGET_BRANCH"
fi
popd
touch  "$WORKTREE/.nojekyll"
