#!/usr/bin/env python3
import hashlib
import json
import pathlib


ROOT = pathlib.Path(__file__).resolve().parents[1]


def digest(relative):
    return hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()


manifest_path = ROOT / "integrations/openclaw/manifest.json"
manifest = json.loads(manifest_path.read_text())
manifest["files"] = {relative: digest(relative) for relative in manifest["files"]}
manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")

checksum_dir = ROOT / ".checksums"
for old in checksum_dir.glob("*.sha256"):
    old.unlink()

artifacts = sorted(ROOT.glob("ACIP_*.md"))
artifacts += [
    ROOT / "checker/ACIP_Checker_v_1.0.md",
    ROOT / "schemas/decision.schema.json",
    ROOT / "integrations/openclaw/AGENTS.fragment.md",
    ROOT / "integrations/openclaw/manifest.json",
    ROOT / "integrations/openclaw/verify.sh",
]
lines = []
for path in artifacts:
    relative = path.relative_to(ROOT).as_posix()
    value = digest(relative)
    checksum_name = relative.replace("/", "_").replace(".md", "").replace(".json", "").replace(".sh", "") + ".sha256"
    content = f"{value}  {relative}\n"
    (checksum_dir / checksum_name).write_text(content)
    lines.append(content)
(checksum_dir / "SHA256SUMS").write_text("".join(lines))
