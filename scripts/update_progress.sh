#!/usr/bin/env bash
set -euo pipefail

PROGRESS_FILE="PROGRESS.md"

usage() {
  cat <<'USAGE'
Usage:
  scripts/update_progress.sh "<progress note>"

Example:
  scripts/update_progress.sh "Implemented live Fingertips ingestion retries"
USAGE
}

if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
  usage
  exit 0
fi

if [[ $# -lt 1 ]]; then
  usage
  exit 1
fi

if [[ ! -f "$PROGRESS_FILE" ]]; then
  echo "Error: $PROGRESS_FILE not found in current directory." >&2
  exit 1
fi

note="$*"
current_date="$(date -u +"%Y-%m-%d")"
current_timestamp="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"

tmp_file="$(mktemp)"

# Keep the status section fresh by updating the first Last updated line.
awk -v updated_date="$current_date" '
  BEGIN { replaced = 0 }
  /^- Last updated:/ && replaced == 0 {
    print "- Last updated: " updated_date
    replaced = 1
    next
  }
  { print }
' "$PROGRESS_FILE" > "$tmp_file"

mv "$tmp_file" "$PROGRESS_FILE"

if ! grep -q '^## Activity Log$' "$PROGRESS_FILE"; then
  {
    echo
    echo "## Activity Log"
  } >> "$PROGRESS_FILE"
fi

printf -- "- %s %s\n" "$current_timestamp" "$note" >> "$PROGRESS_FILE"

echo "Updated $PROGRESS_FILE"
