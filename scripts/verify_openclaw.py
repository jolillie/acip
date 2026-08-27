#!/usr/bin/env python3
import hashlib
import json
import pathlib
import sys


def sha256(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


root = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
manifest_path = root / "integrations/openclaw/manifest.json"
manifest = json.loads(manifest_path.read_text())
errors = []
for relative, expected in manifest["files"].items():
    target = root / relative
    if not target.is_file():
        errors.append(f"missing: {relative}")
        continue
    actual = sha256(target)
    if actual != expected:
        errors.append(f"checksum mismatch: {relative}")

if errors:
    print("\n".join(errors), file=sys.stderr)
    raise SystemExit(1)
print(f"verified {len(manifest['files'])} OpenClaw integration artifacts")
