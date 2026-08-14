#!/usr/bin/env bash
# Bulk-install all Skills from this repo into ~/.claude/skills/
# Usage: ./scripts/install-all.sh [--exclude skill1,skill2]

set -euo pipefail

TARGET="${HOME}/.claude/skills"
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

EXCLUDE=""
if [[ "${1:-}" == "--exclude" ]]; then
  EXCLUDE="${2:-}"
fi

mkdir -p "$TARGET"

# Find every directory containing SKILL.md or skill.md (POSIX-portable)
SKILL_DIRS=()
while IFS= read -r dir; do
  SKILL_DIRS+=("$dir")
done < <(find "$REPO_ROOT" -mindepth 2 -maxdepth 3 \
  \( -name "SKILL.md" -o -name "skill.md" \) -print | while read -r f; do dirname "$f"; done | sort -u)

INSTALLED=0
SKIPPED=0

for dir in "${SKILL_DIRS[@]}"; do
  name="$(basename "$dir")"
  if [[ ",$EXCLUDE," == *",$name,"* ]]; then
    echo "[skip] $name (excluded)"
    SKIPPED=$((SKIPPED+1))
    continue
  fi
  echo "[install] $name -> $TARGET/$name"
  rm -rf "$TARGET/$name"
  cp -r "$dir" "$TARGET/$name"
  INSTALLED=$((INSTALLED+1))
done

echo ""
echo "Installed: $INSTALLED  Skipped: $SKIPPED  Total: ${#SKILL_DIRS[@]}"
echo "Restart Claude Code to load the new skills."