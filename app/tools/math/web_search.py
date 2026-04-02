"""
tools/math/web_search.py
Web search tool using Google Custom Search API.

This is a real tool — the LLM cannot access the internet on its own.
Useful for: looking up specific theorems, finding current educational
resources, verifying formulas the LLM isn't sure about, or finding
worked examples of specific problem types.
"""

import json
import logging
from typing import Optional

from googleapiclient.discovery import build
from langchain_core.tools import tool
from app.config import GOOGLE_API_KEY, GOOGLE_SEARCH_ENGINE_ID

logger = logging.getLogger(__name__)


def search_web(query: str, num_results: int = 5) -> dict:
    """
    Search the web for math-related information using Google Custom Search API.

    Args:
        query: The search query (e.g. "proof of Pythagorean theorem",
               "integration by parts examples", "double angle formula derivation")
        num_results: Number of search results to return (max 10)

    Returns:
        {
            "query": str,
            "results": list[dict],   # List of search results with title, snippet, link
            "total_results": int,    # Estimated total results
            "error": str | None
        }
    """
    if not GOOGLE_API_KEY or not GOOGLE_SEARCH_ENGINE_ID:
        logger.error("Google API credentials not configured")
        return {
            "query": query,
            "results": [],
            "total_results": 0,
            "error": "Google Search not configured. Set GOOGLE_API_KEY and GOOGLE_SEARCH_ENGINE_ID in .env",
        }

    try:
        # Build the Google Custom Search service
        service = build("customsearch", "v1", developerKey=GOOGLE_API_KEY)

        # Execute the search
        result = service.cse().list(
            q=query,
            cx=GOOGLE_SEARCH_ENGINE_ID,
            num=min(num_results, 10),  # Google allows max 10 per request
        ).execute()

        # Parse results
        search_results = []
        if "items" in result:
            for item in result["items"]:
                search_results.append({
                    "title": item.get("title", ""),
                    "snippet": item.get("snippet", ""),
                    "link": item.get("link", ""),
                    "displayLink": item.get("displayLink", ""),
                })

        total_results = int(result.get("searchInformation", {}).get("totalResults", 0))

        return {
            "query": query,
            "results": search_results,
            "total_results": total_results,
            "error": None,
        }

    except Exception as e:
        logger.error(f"Google search failed: {e}")
        return {
            "query": query,
            "results": [],
            "total_results": 0,
            "error": str(e),
        }


@tool
def math_web_search(query: str) -> str:
    """Search the web for math concepts, theorems, proofs, or worked examples using Google Search.
    Use when you need to verify a formula, find a specific theorem, or look up a concept you're not confident about.

    Args:
        query: What to search for (e.g. 'proof of law of cosines', 'integration by parts worked examples')

    Returns:
        JSON string with search results including titles, snippets, and links
    """
    result = search_web(query, num_results=5)
    return json.dumps(result, indent=2)
