#!/usr/bin/env bash
# Scaffold a new skill directory under a category
# Usage: ./scripts/new-skill.sh <skill-name> --category <0X-category-dir>

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SKILL_NAME="${1:?Usage: new-skill.sh <skill-name> --category <0X-category-dir>}"
CATEGORY=""

if [[ "${2:-}" == "--category" ]]; then
  CATEGORY="${3:?missing category value}"
fi

if [[ -z "$CATEGORY" ]]; then
  echo "Error: --category is required" >&2
  exit 1
fi

TARGET="$REPO_ROOT/$CATEGORY/$SKILL_NAME"

if [[ -d "$TARGET" ]]; then
  echo "Error: $TARGET already exists" >&2
  exit 1
fi

mkdir -p "$TARGET"

cat > "$TARGET/SKILL.md" <<SKILL
---
name: $SKILL_NAME
description: TODO - one-sentence description
version: 0.1.0
---

# $SKILL_NAME

TODO: describe what this skill does.

## When to Use

- TODO: trigger conditions

## Quick Start

\`\`\`bash
# TODO: install/run steps
\`\`\`
SKILL

cat > "$TARGET/README.md" <<README
# $SKILL_NAME

Human-readable description. See [SKILL.md](./SKILL.md) for the agent prompt.
README

cat > "$TARGET/LICENSE" <<LICENSE
MIT License - $SKILL_NAME

Copyright (c) $(date +%Y) Andy

[Standard MIT text - replace this with full MIT license text]
LICENSE

echo "Created scaffold: $TARGET"
echo "Next steps:"
echo "  1. Edit SKILL.md and README.md"
echo "  2. Add the skill row to CATALOG.md"
echo "  3. Add entry to CHANGELOG.md"