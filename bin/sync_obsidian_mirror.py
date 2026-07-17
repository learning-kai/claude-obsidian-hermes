#!/usr/bin/env python3
"""One-way mirror server vault -> Windows Obsidian allowlisted folder only."""
from __future__ import annotations

import base64
import os
import subprocess
import tarfile
import tempfile
from pathlib import Path

SRC = Path(os.environ.get("CLAUDE_OBSIDIAN_VAULT", "/home/admin/claude-obsidian-vault"))
KEY = os.environ.get("CLAUDE_OBSIDIAN_MIRROR_KEY", "/home/admin/.ssh/windows-tailscale")
HOST = os.environ.get("CLAUDE_OBSIDIAN_MIRROR_HOST", "Lenovo@100.75.182.32")
DEST = r"D:\Documents\obsidian\claude-obsidian-vault"

EXCLUDE_PREFIXES = (
    ".vault-meta/locks/",
    ".vault-meta/chunks/",
    ".vault-meta/bm25/",
    "backup/",
    "Inbox/processed/",
    ".git/",
)


def excluded(rel: str) -> bool:
    rel = rel.replace("\\", "/").lstrip("./")
    if rel.endswith("__pycache__") or "/__pycache__/" in f"/{rel}/":
        return True
    for p in EXCLUDE_PREFIXES:
        if rel == p.rstrip("/") or rel.startswith(p):
            return True
    return False


def main() -> int:
    if not SRC.is_dir():
        print(f"ERR: missing source {SRC}")
        return 2
    if DEST != r"D:\Documents\obsidian\claude-obsidian-vault":
        print(f"ERR: refuse non-allowlisted dest: {DEST}")
        return 3

    tmp = Path(tempfile.mkstemp(prefix="co-mirror-", suffix=".tgz")[1])
    try:
        with tarfile.open(tmp, "w:gz") as tf:
            for p in SRC.rglob("*"):
                if not p.is_file():
                    continue
                rel = p.relative_to(SRC).as_posix()
                if excluded(rel):
                    continue
                tf.add(p, arcname=rel)

        scp = [
            "scp",
            "-i",
            KEY,
            "-o",
            "ConnectTimeout=20",
            str(tmp),
            f"{HOST}:C:/Users/Lenovo/AppData/Local/Temp/co-mirror.tgz",
        ]
        r = subprocess.run(scp, capture_output=True, text=True)
        if r.returncode != 0:
            print(r.stdout)
            print(r.stderr)
            return r.returncode

        ps = r"""
$ErrorActionPreference = 'Stop'
$dest = 'D:\Documents\obsidian\claude-obsidian-vault'
$tmp = 'C:\Users\Lenovo\AppData\Local\Temp\co-mirror.tgz'
$root = 'D:\Documents\obsidian'
if (-not (Test-Path -LiteralPath $root)) { throw 'obsidian root missing' }
if ([IO.Path]::GetFileName($dest) -ne 'claude-obsidian-vault') { throw 'refuse non-allowlisted dest' }
New-Item -ItemType Directory -Force -Path $dest | Out-Null
if (-not (Test-Path -LiteralPath $tmp)) { throw 'archive missing' }
Get-ChildItem -LiteralPath $dest -Force | Where-Object { $_.Name -notin @('README-镜像说明.md') } | ForEach-Object {
  Remove-Item -LiteralPath $_.FullName -Recurse -Force -ErrorAction SilentlyContinue
}
tar -xzf $tmp -C $dest
$stamp = @(
  '# Mirror sync status',
  '',
  '- Source: /home/admin/claude-obsidian-vault',
  '- Destination: D:\Documents\obsidian\claude-obsidian-vault',
  ('- Last sync: ' + (Get-Date).ToString('s')),
  '- Mode: one-way server -> this folder',
  '- Safety: siblings 考研/日记/大三下/.obsidian not modified'
) -join "`n"
Set-Content -LiteralPath (Join-Path $dest 'SYNC-STATUS.md') -Value $stamp -Encoding UTF8
$files = (Get-ChildItem -LiteralPath $dest -Recurse -File -Force | Measure-Object).Count
$siblings = (Get-ChildItem -LiteralPath $root -Force | Select-Object -ExpandProperty Name) -join ' | '
Write-Output ("EXTRACT_OK files=" + $files)
Write-Output ("SIBLINGS=" + $siblings)
"""
        b64 = base64.b64encode(ps.encode("utf-16le")).decode("ascii")
        cmd = [
            "sudo",
            "-iu",
            "admin",
            "ssh",
            "-i",
            KEY,
            "-o",
            "ConnectTimeout=30",
            HOST,
            f"powershell -NoProfile -EncodedCommand {b64}",
        ]
        r2 = subprocess.run(cmd, capture_output=True, text=True)
        print(r2.stdout.strip())
        if r2.returncode != 0:
            print(r2.stderr)
            return r2.returncode
        print("mirror sync complete")
        return 0
    finally:
        tmp.unlink(missing_ok=True)


if __name__ == "__main__":
    raise SystemExit(main())
