#!/usr/bin/env python3
"""Upload ai-money-lab files to GitHub via gh Contents API.

Bypasses github.com TLS handshake failure on CN proxy nodes — gh CLI talks to
api.github.com which is reachable, git push talks to github.com which is not.
Auto-detects create vs update by fetching the existing sha.

Usage: python push_ideas.py <relative_path> [more paths ...]
"""
# ponytail: API-per-file instead of git push — github.com TLS is blocked on
# every CN node tested (jp/hk), api.github.com works. Switch to git push if a
# node with clean github.com TLS ever shows up.
import base64
import json
import logging
import os
import subprocess
import sys

REPO = "shkyyy18/ai-money-lab"
BRANCH = "main"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

logging.basicConfig(level=logging.INFO, format="%(message)s")
log = logging.getLogger("push_ideas")


def gh_api(*args):
    return subprocess.run(["gh", "api", *args], capture_output=True, text=True)


def upload(path):
    full = os.path.join(ROOT, path)
    if not os.path.exists(full):
        log.warning(f"[skip] not found: {path}")
        return False
    with open(full, "rb") as f:
        content = base64.b64encode(f.read()).decode()

    r = gh_api(f"repos/{REPO}/contents/{path}")
    sha = json.loads(r.stdout).get("sha") if r.returncode == 0 else None
    msg = f"docs: update {path}" if sha else f"feat: add {path}"
    args = [
        f"repos/{REPO}/contents/{path}", "-X", "PUT",
        "-f", f"message={msg}", "-f", f"branch={BRANCH}", "-f", f"content={content}",
    ]
    if sha:
        args += ["-f", f"sha={sha}"]

    r = gh_api(*args)
    if r.returncode == 0:
        log.info(f"[OK] {path} {'updated' if sha else 'created'}")
        return True
    log.error(f"[FAIL] {path}: {r.stderr[:200]}")
    return False


def main():
    paths = sys.argv[1:]
    if not paths:
        print("usage: python push_ideas.py <path> [more paths]", file=sys.stderr)
        sys.exit(2)
    ok = sum(1 for p in paths if upload(p))
    log.info(f"done {ok}/{len(paths)}")
    sys.exit(0 if ok == len(paths) else 1)


if __name__ == "__main__":
    main()
