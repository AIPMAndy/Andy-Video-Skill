#!/usr/bin/env bash
# Validate repository integrity
# Usage: ./scripts/verify.sh

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

ERRORS=0

echo "=== Repository Integrity Check ==="
echo ""

# Check root files
for f in README.md CATALOG.md INSTALLATION.md CONTRIBUTING.md CHANGELOG.md LICENSE .gitignore; do
  if [[ ! -f "$f" ]]; then
    echo "[MISSING] $f"
    ERRORS=$((ERRORS+1))
  else
    echo "[OK]      $f"
  fi
done

# Check each category README
echo ""
echo "--- Category READMEs ---"
for cat in 00-orchestration 01-programmatic-animation 02-recording-to-video 03-code-to-video 04-script-and-planning 05-stylized-effects; do
  if [[ -f "$cat/README.md" ]]; then
    echo "[OK]      $cat/README.md"
  else
    echo "[MISSING] $cat/README.md"
    ERRORS=$((ERRORS+1))
  fi
done

# Check each skill has SKILL.md or skill.md
echo ""
echo "--- Skill SKILL.md ---"
SKILL_DIRS=()
while IFS= read -r dir; do
  SKILL_DIRS+=("$dir")
done < <(find . -mindepth 2 -maxdepth 2 -type d \
  ! -path './.git*' \
  ! -path './showcase*' \
  ! -path './docs*' \
  ! -path './scripts*' \
  ! -path './.github*')

for dir in "${SKILL_DIRS[@]}"; do
  if [[ -f "$dir/SKILL.md" || -f "$dir/skill.md" ]]; then
    echo "[OK]      $dir"
  else
    echo "[MISSING] $dir (no SKILL.md or skill.md)"
    ERRORS=$((ERRORS+1))
  fi
done

# Check showcase
echo ""
echo "--- Showcase ---"
for f in showcase/index.html showcase/assets/css/styles.css showcase/assets/js/main.js; do
  if [[ -f "$f" ]]; then
    echo "[OK]      $f"
  else
    echo "[MISSING] $f"
    ERRORS=$((ERRORS+1))
  fi
done

DETAIL_COUNT=$(find showcase/skills -name "*.html" -type f 2>/dev/null | wc -l)
echo "[INFO]    showcase skill detail pages: $DETAIL_COUNT (expected: 13)"

echo ""
if [[ $DETAIL_COUNT -ne 13 ]]; then
  echo "[MISMATCH] expected 13 showcase detail pages; found $DETAIL_COUNT"
  ERRORS=$((ERRORS+1))
fi

if [[ $ERRORS -eq 0 ]]; then
  echo "✓ All checks passed"
  exit 0
else
  echo "✗ $ERRORS error(s) found"
  exit 1
fi