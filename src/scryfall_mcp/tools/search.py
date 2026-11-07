from fastmcp.tools import tool

from scryfall_mcp.utils import search_cards, card_to_dict


@tool
def search(q: str, offset: int = 0, limit: int = 60) -> dict:
    """
    Search for cards using Scryfall syntax.

    Args:
        q (str):
            The search query.
            
            The query must be in Scryfall syntax.

            Common filters include

            - `c` - Color (uses WUBRG notation, e.g. `w` for white and `u` for blue)
            - `ci` - Color identity
            - `t` - Card types (e.g. `instant` or `fish`)
            - `o` - Oracle text
            - `kw` - Keyword abilities (e.g. `flying`)
            - `pow`/`tou` - Power / Toughness
            - `s` - Set code
            - `f` - Format legality (e.g. `commander`)
            - `otag` - Oracle tag (e.g. `draw` or `combat-trick`)

            Examples

            - `fire s:alpha` - Cards with "fire" in their name from the Alpha set
            - `o:draw t:creature` - Creature cards with "draw" in their text
            - `otag:removal ci<=bw` - Cards that cause removal and have a color identity of blue and/or white and/or colorless
            - `f:standard pow>=3 -c:r` - Cards with power 3 or greater that are legal in standard and are not red (negate conditions with `-`)
            - `t:creature o:/^{T}:/` - Creatures that tap with no other payment (regex is supported)
            - `t:legendary (kw:first-strike or kw:double-strike)` - Cards that are legendary and have first strike or double strike (nested conditions are supported)

        offset (int, optional):
            Results offset. Defaults to 0.

        limit (int, optional):
            Results limit. Defaults to 60.

    Returns:
        dict[str, list[dict]]:
            Search results.
            Includes any errors that occurred during card search.
    """
    
    results = []
    error = None
    try:
        results = search_cards(q=q, offset=offset, limit=limit)
        formatted_results = [card_to_dict(card) for card in results]
        return {
            "message": f"Found {len(formatted_results)} results.",
            "cards": formatted_results,
        }
    except Exception as e:
        error = f"Error fetching search results: {str(e)}"
        return {
            "message": error,
        }
