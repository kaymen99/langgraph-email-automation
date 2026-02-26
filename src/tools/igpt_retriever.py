"""
iGPT Email Intelligence Retriever

An optional alternative to the ChromaDB RAG pipeline. Uses the official
langchain-igpt SDK to retrieve context from indexed emails and attachments
via natural language queries.

Requires:
  - IGPT_API_KEY: Bearer token for iGPT API authentication
  - IGPT_API_USER: User identifier for the iGPT API

SDK: pip install langchain-igpt
Docs: https://docs.igpt.ai
"""

from colorama import Fore, Style
from langchain_igpt import IgptAsk, IgptSearch


# Initialized lazily on first call (credentials read from env vars)
_ask_tool = None
_search_tool = None


def _get_ask_tool(quality="cef-1-normal"):
    """Returns a cached IgptAsk tool instance."""
    global _ask_tool
    if _ask_tool is None:
        _ask_tool = IgptAsk(quality=quality)
    return _ask_tool


def _get_search_tool(max_results=5):
    """Returns a cached IgptSearch tool instance."""
    global _search_tool
    if _search_tool is None:
        _search_tool = IgptSearch(max_results=max_results)
    return _search_tool


def igpt_retrieve(query, quality="cef-1-normal"):
    """
    Calls the iGPT Recall API to retrieve context for a natural language query.

    Args:
        query: Natural language question about email content.
        quality: Response quality level (default: "cef-1-normal").

    Returns:
        Context string from iGPT containing relevant email intelligence.
    """
    print(Fore.CYAN + f"[iGPT] Retrieving context for: {query[:80]}..." + Style.RESET_ALL)

    tool = _get_ask_tool(quality)
    result = tool.invoke({"input": query})

    # Handle error responses from the API
    if isinstance(result, dict) and "error" in result:
        print(Fore.RED + f"[iGPT] API error: {result['error']}" + Style.RESET_ALL)
        return "No relevant information found."

    # Extract the output text from the response
    output = result.get("output", "") if isinstance(result, dict) else str(result)

    if not output:
        print(Fore.YELLOW + "[iGPT] No relevant context found." + Style.RESET_ALL)
        return "No relevant information found."

    print(Fore.GREEN + "[iGPT] Context retrieved successfully." + Style.RESET_ALL)
    return output


def igpt_search(query, max_results=5):
    """
    Calls the iGPT Search API to find relevant email documents.

    Args:
        query: Natural language search query.
        max_results: Maximum number of results to return (default: 5).

    Returns:
        List of matching email document summaries.
    """
    print(Fore.CYAN + f"[iGPT] Searching for: {query[:80]}..." + Style.RESET_ALL)

    tool = _get_search_tool(max_results)
    result = tool.invoke({"query": query})

    if isinstance(result, dict) and "error" in result:
        print(Fore.RED + f"[iGPT] API error: {result['error']}" + Style.RESET_ALL)
        return []

    results = result.get("results", []) if isinstance(result, dict) else []

    print(Fore.GREEN + f"[iGPT] Found {len(results)} results." + Style.RESET_ALL)
    return results
