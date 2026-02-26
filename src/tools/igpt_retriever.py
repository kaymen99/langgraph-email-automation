"""
iGPT Email Intelligence Retriever

An optional alternative to the ChromaDB RAG pipeline. Uses iGPT's Recall API
to retrieve context from indexed emails and attachments via natural language queries.

Requires:
  - IGPT_API_KEY: Bearer token for iGPT API authentication
  - IGPT_API_USER: User identifier for the iGPT API

Docs: https://docs.igpt.ai
"""

import os
import requests
from colorama import Fore, Style

IGPT_BASE_URL = "https://api.igpt.ai/v1/recall"


def _get_headers():
    """Returns authorization headers for iGPT API calls."""
    api_key = os.getenv("IGPT_API_KEY")
    if not api_key:
        raise ValueError(
            "IGPT_API_KEY environment variable is required when USE_IGPT=true. "
            "Get your API key at https://igpt.ai"
        )
    return {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }


def _get_user():
    """Returns the iGPT user identifier."""
    user = os.getenv("IGPT_API_USER")
    if not user:
        raise ValueError(
            "IGPT_API_USER environment variable is required when USE_IGPT=true. "
            "Set it to your iGPT user ID."
        )
    return user


def igpt_retrieve(query, quality="cef-1-normal"):
    """
    Calls the iGPT Recall API to retrieve context for a natural language query.

    Args:
        query: Natural language question about email content.
        quality: Response quality level (default: "cef-1-normal").

    Returns:
        Context string from iGPT containing relevant email intelligence.

    Raises:
        ValueError: If required environment variables are missing.
        requests.HTTPError: If the API request fails.
    """
    print(Fore.CYAN + f"[iGPT] Retrieving context for: {query[:80]}..." + Style.RESET_ALL)

    response = requests.post(
        f"{IGPT_BASE_URL}/ask/",
        headers=_get_headers(),
        json={
            "user": _get_user(),
            "input": query,
            "stream": False,
            "quality": quality,
            "output_format": "text",
        },
        timeout=30,
    )
    response.raise_for_status()

    data = response.json()
    result = data.get("output", data.get("result", ""))

    if not result:
        print(Fore.YELLOW + "[iGPT] No relevant context found." + Style.RESET_ALL)
        return "No relevant information found."

    print(Fore.GREEN + "[iGPT] Context retrieved successfully." + Style.RESET_ALL)
    return result


def igpt_search(query, max_results=5):
    """
    Calls the iGPT Search API to find relevant email documents.

    Args:
        query: Natural language search query.
        max_results: Maximum number of results to return (default: 5).

    Returns:
        List of matching email document summaries.

    Raises:
        ValueError: If required environment variables are missing.
        requests.HTTPError: If the API request fails.
    """
    print(Fore.CYAN + f"[iGPT] Searching for: {query[:80]}..." + Style.RESET_ALL)

    response = requests.post(
        f"{IGPT_BASE_URL}/search/",
        headers=_get_headers(),
        json={
            "user": _get_user(),
            "input": query,
            "max_results": max_results,
        },
        timeout=30,
    )
    response.raise_for_status()

    data = response.json()
    results = data.get("results", [])

    print(Fore.GREEN + f"[iGPT] Found {len(results)} results." + Style.RESET_ALL)
    return results
