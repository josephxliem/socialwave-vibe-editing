#!/bin/bash
# Social Wave — one-command Premiere Pro MCP bridge install (macOS)
# Installs the npm server, the CEP panel, enables CEP debug mode, registers with Claude Code.
set -e
VERSION="${1:-1.1.1}"   # pinned known-good; bump deliberately after testing
echo "== Premiere MCP bridge install (v$VERSION) =="

command -v npm >/dev/null || { echo "ERROR: npm not found — install Node.js first (brew install node)"; exit 1; }
npm install -g "premiere-pro-mcp@$VERSION"

ROOT="$(npm root -g)/premiere-pro-mcp"
echo "-- installing CEP panel (copy mode) --"
bash "$ROOT/scripts/install-cep.sh" --copy

echo "-- enabling CEP PlayerDebugMode (lets Premiere load unsigned panels) --"
for v in 11 12; do defaults write "com.adobe.CSXS.$v" PlayerDebugMode 1; done

echo "-- registering with Claude Code --"
claude mcp add premiere-pro --scope user \
  --env PREMIERE_TEMP_DIR=/tmp/premiere-mcp-bridge \
  -- premiere-pro-mcp || echo "(already registered — fine)"

echo ""
echo "DONE. Now: restart Premiere Pro, open Window > Extensions > MCP Bridge,"
echo "then verify in Claude Code with the premiere-pro 'ping' tool."
