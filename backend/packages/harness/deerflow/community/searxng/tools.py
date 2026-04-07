"""SearXNG community tools for DeerFlow.

Provides ``web_search`` tool using a self-hosted SearXNG instance.
SearXNG is a free, open-source metasearch engine that aggregates results
from Google, Bing, DuckDuckGo, and 70+ other engines — with zero API
keys, zero rate limits, and full data sovereignty.

Configuration in ``config.yaml``::

    tools:
      - name: web_search
        group: web
        use: deerflow.community.searxng.tools:web_search_tool
        # URL of your self-hosted SearXNG instance
        base_url: http://searxng:8080
        # Optional: max results (default: 5)
        max_results: 5
        # Optional: language filter (default: auto)
        language: en
"""

import json
import logging

import httpx
from langchain.tools import tool

from deerflow.config import get_app_config

logger = logging.getLogger(__name__)


def _get_searxng_config() -> tuple[str, int, str | None]:
    """Return (base_url, max_results, language) from config."""
    config = get_app_config().get_tool_config("web_search")
    base_url = "http://searxng:8080"
    max_results = 5
    language = None
    if config is not None:
        base_url = config.model_extra.get("base_url", base_url)
        max_results = int(config.model_extra.get("max_results", max_results))
        language = config.model_extra.get("language", language)
    return base_url, max_results, language


@tool("web_search", parse_docstring=True)
def web_search_tool(query: str) -> str:
    """Search the web using SearXNG (self-hosted metasearch engine).

    Aggregates results from multiple search engines (Google, Bing,
    DuckDuckGo, and more) for comprehensive coverage. Fully self-hosted
    with no API keys or rate limits.

    Args:
        query: The query to search for.
    """
    try:
        base_url, max_results, language = _get_searxng_config()

        params: dict[str, str | int] = {
            "q": query,
            "format": "json",
            "categories": "general",
        }
        if language:
            params["language"] = language

        resp = httpx.get(
            f"{base_url}/search",
            params=params,
            headers={
                "X-Forwarded-For": "127.0.0.1",
                "X-Real-IP": "127.0.0.1",
            },
            timeout=30,
        )
        resp.raise_for_status()
        data = resp.json()

        results = data.get("results", [])[:max_results]

        if not results:
            return json.dumps(
                {"error": "No results found", "query": query},
                ensure_ascii=False,
            )

        normalized_results = [
            {
                "title": r.get("title", ""),
                "url": r.get("url", ""),
                "content": r.get("content", ""),
            }
            for r in results
        ]

        output = {
            "query": query,
            "total_results": len(normalized_results),
            "results": normalized_results,
        }

        return json.dumps(output, indent=2, ensure_ascii=False)

    except httpx.ConnectError:
        logger.error("Cannot connect to SearXNG at %s", base_url)
        return json.dumps(
            {"error": f"Cannot connect to SearXNG at {base_url}", "query": query},
            ensure_ascii=False,
        )
    except Exception as e:
        logger.error("SearXNG search failed: %s", e)
        return json.dumps(
            {"error": str(e), "query": query},
            ensure_ascii=False,
        )
