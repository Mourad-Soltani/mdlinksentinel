# Tests for mdlinksentinel
# Built by Mourad.Soltani

from pathlib import Path
import pytest
from mdlinksentinel import extract_links, scan_path

def test_extract_links():
    content = "See [example](https://example.com) and [bad](https://httpbin.org/status/404)"
    links = extract_links(content)
    assert "https://example.com" in links
    assert "https://httpbin.org/status/404" in links

def test_scan_temp_md(tmp_path: Path):
    md = tmp_path / "test.md"
    md.write_text("# Test\n[good](https://example.com)\n[missing](https://httpbin.org/status/404)\n")
    results = scan_path(tmp_path)
    assert len(results) >= 2
    statuses = [r[3] for r in results]
    assert any(s == "ok" for s in statuses)
    assert any(s == "broken" for s in statuses)
