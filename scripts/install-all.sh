#!/usr/bin/env bash
# Bulk-install all Skills from this repo into ~/.claude/skills/
# Usage: ./scripts/install-all.sh [--exclude skill1,skill2] [--with-upstreams]

set -euo pipefail

TARGET="${HOME}/.claude/skills"
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

EXCLUDE=""
WITH_UPSTREAMS=0
while [[ $# -gt 0 ]]; do
  case "$1" in
    --exclude) [[ $# -ge 2 ]] || { echo "Missing exclusion names" >&2; exit 2; }; EXCLUDE="$2"; shift 2 ;;
    --with-upstreams) WITH_UPSTREAMS=1; shift ;;
    --help|-h) echo "Usage: $0 [--exclude name1,name2] [--with-upstreams]"; exit 0 ;;
    *) echo "Unknown option: $1" >&2; exit 2 ;;
  esac
done

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
  if [[ -L "$TARGET/$name" ]]; then echo "Refusing to overwrite a symlink: $TARGET/$name" >&2; exit 1; fi
  rm -rf "$TARGET/$name"
  cp -r "$dir" "$TARGET/$name"
  INSTALLED=$((INSTALLED+1))
done

echo ""
echo "Installed: $INSTALLED  Skipped: $SKIPPED  Total: ${#SKILL_DIRS[@]}"
if [[ "$WITH_UPSTREAMS" -eq 1 ]]; then
  # Explicit network opt-in: stage reviewed upstream sources, NOT dependencies or videos.
  command -v python3 >/dev/null || { echo "python3 is required" >&2; exit 1; }
  DIRECTOR="$REPO_ROOT/00-orchestration/andy-video-director/director.py"
  for upstream in bb-video moneyprinterturbo-video remotion-skills; do
    if [[ ",$EXCLUDE," == *",$upstream,"* ]]; then echo "[skip-upstream] $upstream"; continue; fi
    if [[ -e "$TARGET/$upstream" ]]; then echo "[skip-existing] $upstream"; continue; fi
    python3 "$DIRECTOR" bootstrap "$upstream" --dest "$TARGET" --execute
  done
fi

echo "Restart Claude Code to load new Skills. Rendering dependencies are separate."