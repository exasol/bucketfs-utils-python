#!/bin/bash

set -euo pipefail

PUSH_ENABLED="$1"

SCRIPT_DIR="$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")"

TAG="$(git describe --tags --exact-match)"
if [ -n "$TAG" ]; then
  TARGET_BRANCH="$("$SCRIPT_DIR/get_target_branch_name.sh" "main")"
  bash "$SCRIPT_DIR/deploy-to-github-pages.sh" "$TARGET_BRANCH" origin "$PUSH_ENABLED" "$TAG"
else
  echo "ERROR: Could not acquire your current checked out tag. Please check the state of your working copy"
fi