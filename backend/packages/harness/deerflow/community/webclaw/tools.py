"""Webclaw community tools for DeerFlow.

Provides ``web_fetch`` tool using the self-hosted Webclaw binary.
Webclaw offers 95.1% extraction accuracy, 67% fewer tokens than raw HTML,
and sub-millisecond extraction speed — all without a headless browser.

For web_search, this module does NOT provide its own implementation because
webclaw's search requires a cloud API key. Use DuckDuckGo or Tavily for
search instead, and webclaw solely for superior content extraction.

Deployment options:
  1. Install webclaw binary in the Docker image (recommended for self-hosted)
  2. Point at webclaw.io cloud API via the Python SDK

Configuration in ``config.yaml``::

    tools:
      - name: web_fetch
        group: web
        use: deerflow.community.webclaw.tools:web_fetch_tool
        # Optional: path to webclaw binary (default: webclaw)
        webclaw_bin: /usr/local/bin/webclaw
        # Optional: request timeout in seconds
        timeout: 30
"""

import json
import subprocess

from langchain.tools import tool

from deerflow.config import get_app_config


def _get_webclaw_bin() -> str:
    """Return the path to the webclaw binary from config, or default."""
    config = get_app_config().get_tool_config("web_fetch")
    if config is not None:
        return config.model_extra.get("webclaw_bin", "webclaw")
    return "webclaw"


def _get_timeout() -> int:
    """Return request timeout in seconds from config, or default."""
    config = get_app_config().get_tool_config("web_fetch")
    if config is not None:
        return int(config.model_extra.get("timeout", 30))
    return 30


# ── web_fetch ────────────────────────────────────────────────────────────


@tool("web_fetch", parse_docstring=True)
def web_fetch_tool(url: str) -> str:
    """Fetch the contents of a web page at a given URL using Webclaw.

    Uses the LLM-optimized output format for 67% fewer tokens compared
    to raw HTML. Powered by Rust with TLS fingerprinting for reliable
    extraction without a headless browser.

    Only fetch EXACT URLs that have been provided directly by the user
    or have been returned in results from the web_search and web_fetch
    tools.
    This tool can NOT access content that requires authentication,
    such as private Google Docs or pages behind login walls.
    Do NOT add www. to URLs that do NOT have them.
    URLs must include the schema: https://example.com is a valid URL
    while example.com is an invalid URL.

    Args:
        url: The URL to fetch the contents of.
    """
    try:
        webclaw_bin = _get_webclaw_bin()
        timeout = _get_timeout()

        result = subprocess.run(
            [webclaw_bin, url, "-f", "json", "--only-main-content"],
            capture_output=True,
            text=True,
            timeout=timeout,
        )

        if result.returncode != 0:
            stderr = result.stderr.strip()
            return f"Error: webclaw failed: {stderr or 'unknown error'}"

        data = json.loads(result.stdout)

        metadata = data.get("metadata", {})
        content_obj = data.get("content", {})
        title = metadata.get("title", "Untitled")
        markdown = content_obj.get("markdown", "")

        if not markdown:
            return "Error: No content found"

        return f"# {title}\n\n{markdown[:4096]}"

    except subprocess.TimeoutExpired:
        return f"Error: Request timed out after {_get_timeout()}s"
    except json.JSONDecodeError:
        return "Error: Failed to parse webclaw output"
    except FileNotFoundError:
        return "Error: webclaw binary not found. Install it: cargo install --git https://github.com/0xMassi/webclaw.git webclaw-cli"
    except Exception as e:
        return f"Error: {str(e)}"
