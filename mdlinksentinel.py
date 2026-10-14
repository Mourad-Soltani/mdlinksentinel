# mdlinksentinel
# Built by Mourad.Soltani
# Minimal CLI to scan Markdown files for broken hyperlinks.

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import List, Tuple
from urllib.parse import urlparse

import httpx

LINK_RE = re.compile(r'\[([^\]]+)\]\((https?://[^\s)]+)\)')

def extract_links(content: str) -> List[str]:
    return [m.group(2) for m in LINK_RE.finditer(content)]

def check_link(url: str, timeout: float = 5.0) -> Tuple[str, int | None, str]:
    try:
        with httpx.Client(timeout=timeout, follow_redirects=True) as client:
            resp = client.head(url)
            if resp.status_code >= 400:
                # fallback to GET for some servers
                resp = client.get(url)
            return url, resp.status_code, "ok" if resp.status_code < 400 else "broken"
    except Exception as e:
        return url, None, str(e)

def scan_path(path: Path) -> List[Tuple[str, str, int | None, str]]:
    results = []
    if path.is_file() and path.suffix.lower() in {".md", ".markdown"}:
        files = [path]
    elif path.is_dir():
        files = list(path.rglob("*.md")) + list(path.rglob("*.markdown"))
    else:
        return results
    for f in files:
        try:
            content = f.read_text(encoding="utf-8", errors="ignore")
            for url in extract_links(content):
                status_url, code, note = check_link(url)
                results.append((str(f), status_url, code, note))
        except Exception:
            continue
    return results

def main() -> int:
    parser = argparse.ArgumentParser(description="Scan Markdown for broken links. Built by Mourad.Soltani")
    parser.add_argument("path", nargs="?", default=".", help="File or directory to scan")
    parser.add_argument("--fail-on-broken", action="store_true", help="Exit non-zero if any broken links")
    args = parser.parse_args()
    results = scan_path(Path(args.path))
    broken = 0
    for src, url, code, note in results:
        status = "OK" if note == "ok" else "BROKEN"
        print(f"{status}\t{code or 'ERR'}\t{url}\t({src})")
        if note != "ok":
            broken += 1
    print(f"\nScanned {len(results)} links, {broken} broken.")
    if args.fail_on_broken and broken > 0:
        return 1
    return 0

if __name__ == "__main__":
    sys.exit(main())
