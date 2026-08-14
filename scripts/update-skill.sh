#!/usr/bin/env bash
# Overwrite one skill from its source path
# Usage: ./scripts/update-skill.sh <skill-name> [source-path]
# Default source path: ~/.claude/skills/<skill-name>

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SKILL_NAME="${1:?Usage: update-skill.sh <skill-name> [source-path]}"
SOURCE="${2:-$HOME/.claude/skills/$SKILL_NAME}"

if [[ ! -d "$SOURCE" ]]; then
  echo "Error: source directory not found: $SOURCE" >&2
  exit 1
fi

# Locate skill in repo (under any category)
TARGET="$(find "$REPO_ROOT" -mindepth 2 -maxdepth 3 -type d -name "$SKILL_NAME" | head -n 1)"

if [[ -z "$TARGET" ]]; then
  echo "Error: skill '$SKILL_NAME' not found in repo" >&2
  exit 1
fi

echo "Updating $SKILL_NAME:"
echo "  source: $SOURCE"
echo "  target: $TARGET"

rsync -a --delete --exclude='node_modules' --exclude='__pycache__' --exclude='.venv' --exclude='.DS_Store' \
  "$SOURCE/" "$TARGET/"

# Append CHANGELOG entry
TODAY="$(date +%Y-%m-%d)"
cat >> "$REPO_ROOT/CHANGELOG.md" <<ENTRY

## [$SKILL_NAME] - $TODAY

### Updated
- Synced from $SOURCE

ENTRY

echo "Done. Review CHANGELOG.md and commit."