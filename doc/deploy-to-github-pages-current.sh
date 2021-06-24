#!/bin/bash

set -euo pipefail

PUSH_ENABLED="$1"

SCRIPT_DIR="$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")"

SCRIPT_DIR="$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")"
SOURCE_BRANCH="$(git rev-parse --abbrev-ref HEAD)"
if [ "$SOURCE_BRANCH" != "main" ]; then
  if [ -n "$SOURCE_BRANCH" ]; then
    TARGET_BRANCH="$("$SCRIPT_DIR/get_target_branch_name.sh" "$SOURCE_BRANCH")"
    bash "$SCRIPT_DIR/deploy-to-github-pages.sh" "$TARGET_BRANCH" origin "$PUSH_ENABLED" "$SOURCE_BRANCH"
  else
    echo "ERROR: Could not acquire your current checked out branch. Please check the state of your "
  fi
else
  echo "ERROR: Source branch is 'main'."
fi
