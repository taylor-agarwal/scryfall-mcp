from fastmcp.tools import tool
from scrython.cards import Object

from scryfall_mcp.utils import card_to_dict, get_card


@tool
def get_cards(names: list[str]) -> dict:
    """
    Fetch card details for one or more cards by name.

    Args:
        names (list[str]):
            Names of cards to fetch details for.

    Returns:
        dict[str, list[dict]]:
            Card details.
            Includes any errors that occurred during card lookup.

    """

    cards: list[Object] = []
    errors: dict[str, str] = {}
    for name in names:
        try:
            card = get_card(name=name)
            cards.append(card)
        except Exception as e:
            error = f"Failed to find card named {name}: {e!s}"
            errors[name] = error

    formatted_cards = [card_to_dict(card) for card in cards]
    response = {
        "message": "Fetched {len(cards)} cards successfully.", 
        "cards": formatted_cards,
    }
    if num_errors := len(errors) > 0:
        response["message"] += f" Failed to fetch {num_errors} cards."
        response["errors"] = errors

    return response
