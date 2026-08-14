#!/bin/bash

# Render simplified version (no LaTeX required)
export PATH="/Users/andy/Library/Python/3.9/bin:$PATH"

SCRIPT="attention_mechanism_simple.py"
QUALITY="${1:-low}"

case $QUALITY in
    low) FLAG="-pql" ;;
    medium) FLAG="-pqm" ;;
    high) FLAG="-pqh" ;;
    production) FLAG="-pqk" ;;
    *)
        echo "Usage: ./render_simple.sh [low|medium|high|production]"
        exit 1
        ;;
esac

echo "🎬 Rendering simplified Attention Mechanism video ($QUALITY quality)"
echo ""

SCENES=(
    "AttentionIntro"
    "AttentionBasics"
    "AttentionMathSetup"
    "AttentionConclusion"
)

for SCENE in "${SCENES[@]}"; do
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "🎥 Rendering: $SCENE"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    manim $FLAG $SCRIPT $SCENE
    
    if [ $? -ne 0 ]; then
        echo "❌ Failed to render $SCENE"
        exit 1
    fi
    
    echo "✅ $SCENE completed"
    echo ""
done

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🎉 All 4 scenes rendered successfully!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
