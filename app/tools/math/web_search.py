"""
tools/math/web_search.py
Web search tool using OpenAI's built-in web search.

This is a real tool — the LLM cannot access the internet on its own.
Useful for: looking up specific theorems, finding current educational
resources, verifying formulas the LLM isn't sure about, or finding
worked examples of specific problem types.
"""

import json
import logging

from openai import OpenAI
from langchain_core.tools import tool
from app.config import OPENAI_API_KEY, OPENAI_MODEL

logger = logging.getLogger(__name__)

_client = OpenAI(api_key=OPENAI_API_KEY)


def search_web(query: str) -> dict:
    """
    Search the web for math-related information using OpenAI's
    web search tool calling feature.

    Args:
        query: The search query (e.g. "proof of Pythagorean theorem",
               "integration by parts examples", "double angle formula derivation")

    Returns:
        {
            "query": str,
            "result": str,          # The answer with citations
            "annotations": list,    # Source URLs if available
            "error": str | None
        }
    """
    try:
        response = _client.responses.create(
            model=OPENAI_MODEL,
            tools=[{"type": "web_search_preview"}],
            input=f"Search for math educational content: {query}",
        )

        # Extract text and annotations from the response
        result_text = ""
        annotations = []

        for item in response.output:
            if item.type == "message":
                for block in item.content:
                    if block.type == "output_text":
                        result_text = block.text
                        # Collect citation URLs
                        if hasattr(block, "annotations"):
                            for ann in block.annotations:
                                if hasattr(ann, "url"):
                                    annotations.append({
                                        "title": getattr(ann, "title", ""),
                                        "url": ann.url,
                                    })

        return {
            "query": query,
            "result": result_text,
            "annotations": annotations,
            "error": None,
        }

    except Exception as e:
        logger.error(f"Web search failed: {e}")
        return {
            "query": query,
            "result": None,
            "annotations": [],
            "error": str(e),
        }


@tool
def math_web_search(query: str) -> str:
    """Search the web for math concepts, theorems, proofs, or worked examples. Use when you need to verify a formula, find a specific theorem, or look up a concept you're not confident about.

    Args:
        query: What to search for (e.g. 'proof of law of cosines', 'integration by parts worked examples')
    """
    result = search_web(query)
    return json.dumps(result)
