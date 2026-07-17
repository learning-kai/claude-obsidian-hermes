#!/usr/bin/env python3
"""Best-effort retrieval refresh for the vault."""
from __future__ import annotations
import subprocess
from pathlib import Path

def reindex(vault: Path, timeout: int = 180) -> dict:
    vault = Path(vault)
    setup = vault / "bin" / "setup-retrieve.sh"
    if setup.exists():
        cp = subprocess.run(
            ["bash", str(setup), "--no-llm"],
            cwd=str(vault),
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        return {
            "method": "setup-retrieve",
            "rc": cp.returncode,
            "ok": cp.returncode == 0,
            "tail": (cp.stdout or cp.stderr or "")[-300:],
        }
    bm25 = vault / "scripts" / "bm25-index.py"
    if bm25.exists():
        cp = subprocess.run(
            ["python3", str(bm25), "build"],
            cwd=str(vault),
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        return {
            "method": "bm25-build",
            "rc": cp.returncode,
            "ok": cp.returncode == 0,
            "tail": (cp.stdout or cp.stderr or "")[-300:],
        }
    return {"method": "none", "ok": False, "rc": 1}
