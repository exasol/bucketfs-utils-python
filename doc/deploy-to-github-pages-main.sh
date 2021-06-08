#!/bin/bash

PUSH_ENABLED="$1"

set -euo pipefail

SCRIPT_DIR="$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")"
SOURCE_BRANCH="$(git rev-parse --abbrev-ref HEAD)"
if [ "$SOURCE_BRANCH" == "main" ]
then
  BRANCH="github-pages/main"
  bash "$SCRIPT_DIR/deploy-to-github-pages.sh" "$BRANCH" origin "$PUSH_ENABLED"
else
  echo "Abort. Source branch is not 'main', you are at branch '$SOURCE_BRANCH'"
fi
