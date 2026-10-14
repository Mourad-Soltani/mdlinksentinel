# MDLinkSentinel

Minimal CLI tool to scan Markdown files and directories for broken hyperlinks.

**Built by Mourad.Soltani**

## Features

- Extract `https://` links from Markdown
- Check status with HTTP HEAD/GET fallback
- Report OK / BROKEN
- Optional `--fail-on-broken` for CI
- Simple, zero-config, Python 3.10+

## Installation

```bash
pip install httpx pytest
python mdlinksentinel.py --help
```

## Usage

```bash
python mdlinksentinel.py .
python mdlinksentinel.py README.md --fail-on-broken
```

## Tests

```bash
pytest test_mdlinksentinel.py -v
```

## Requirements

- Python 3.10+
- httpx

Signature: Mourad.Soltani
