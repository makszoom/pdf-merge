#!/bin/bash
# generate-agents.sh — Collects factual data for AGENTS.md update
# Run: bash scripts/generate-agents.sh

cd "$(dirname "$0")/.."

echo "=== Factual data for AGENTS.md ==="
echo "HTML files: $(find . -name '*.html' -not -path '*/node_modules/*' | wc -l)"
echo "JS files: $(find . -name '*.js' -not -path '*/node_modules/*' | wc -l)"
echo "CSS files: $(find . -name '*.css' -not -path '*/node_modules/*' | wc -l)"
echo ""
echo "Last commits:"
git log --oneline -5 2>/dev/null || echo "No git repository"
echo ""
echo "Files changed last 24h:"
git diff --name-only HEAD~1 2>/dev/null || echo "N/A"
