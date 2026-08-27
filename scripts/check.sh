#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd -P)"
cd "$repo_root"

python3 -m unittest discover -s tests -p 'test_*.py'
python3 scripts/replay_fixtures.py
./integrations/openclaw/verify.sh

while IFS= read -r checksum_file; do
  if command -v sha256sum >/dev/null 2>&1; then
    sha256sum -c "$checksum_file"
  else
    expected="$(awk '{print $1}' "$checksum_file")"
    target="$(awk '{print $2}' "$checksum_file")"
    actual="$(shasum -a 256 "$target" | awk '{print $1}')"
    test "$expected" = "$actual"
  fi
done < <(find .checksums -name '*.sha256' -type f | LC_ALL=C sort)
