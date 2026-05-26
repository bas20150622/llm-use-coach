#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="$(cd "$(dirname "$0")" && pwd)"
DATA_DIR="${XDG_DATA_HOME:-$HOME/.local/share}/llm-use-coach"
COMMANDS_DIR="$HOME/.claude/commands"

echo "Installing LLM Use Coach..."

# Create data directory structure
mkdir -p "$DATA_DIR/debriefs" "$DATA_DIR/lessons" "$DATA_DIR/scores"

# Copy README to data directory (the coach reads it from there)
cp "$REPO_DIR/README.md" "$DATA_DIR/README.md"

# Initialize state and profile if they don't exist
if [ ! -f "$DATA_DIR/state.yaml" ]; then
    cat > "$DATA_DIR/state.yaml" <<'EOF'
analyzed: {}
focus_next: null
EOF
    echo "  Created state.yaml"
fi

if [ ! -f "$DATA_DIR/profile.md" ]; then
    cat > "$DATA_DIR/profile.md" <<'EOF'
# Prompting Profile

## Current strengths
(No sessions analyzed yet)

## Active growth areas
(No sessions analyzed yet)

## Resolved
(None)

## Trajectory
| Date | Project | Prec | Ctx | Scope | Mode | Quest |
|------|---------|------|-----|-------|------|-------|

## Focus log
| Date | Focus given | Practiced? | Result |
|------|-------------|------------|--------|
EOF
    echo "  Created profile.md"
fi

# Install global slash command
mkdir -p "$COMMANDS_DIR"
cp "$REPO_DIR/commands/coach.md" "$COMMANDS_DIR/coach.md"

echo ""
echo "Installed:"
echo "  Data directory: $DATA_DIR"
echo "  Slash command:  $COMMANDS_DIR/coach.md"
echo ""
echo "Usage: run /coach from any Claude Code session."
