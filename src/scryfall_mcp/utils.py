import logging
import os

import scrython
from scrython.cards import Object

logger = logging.getLogger(__name__)

# Construct card-tag map
CARD_TAG_MAP: dict[str, list[str]] = {}
if os.getenv("ENABLE_ORACLE_TAGS") == "true":
    print("Fetching oracle tags...")
    bulk_tags = scrython.bulk_data.ByType(type="oracle_tags")
    all_tags = [scrython.tags.Object(tag) for tag in bulk_tags.download()]
    for tag in all_tags:
        for tagging in tag.taggings:
            CARD_TAG_MAP[tagging.oracle_id].append(tag.label)


def get_card(name: str) -> Object:
    """Get a card by name."""
    card = scrython.cards.Named(fuzzy=name)
    return card


def card_to_dict(card: Object) -> dict:
    """Format a card as a minimal dictionary."""
    # Filter out fields that add distracting, useless, or redundant information
    fields = [
        "object",
        "id",
        "oracle_id",
        # "multiverse_ids",
        # "resource_id",
        # "mtgo_id",
        # "arena_id",
        # "tcgplayer_id",
        # "cardmarket_id",
        "name",
        # "lang",
        "released_at",
        # "uri",
        "scryfall_uri",
        # "layout",
        # "highres_image",
        # "image_status",
        # "image_updated_at",
        # "image_uris",
        "mana_cost",
        "cmc",
        "type_line",
        "oracle_text",
        "colors",
        "color_identity",
        "keywords",
        # "all_parts",
        "legalities",
        "games",
        # "reserved",
        "game_changer",
        # "foil",
        # "nonfoil",
        # "finishes",
        # "oversized",
        # "promo",
        # "reprint",
        # "variation",
        # "set_id",
        "set",
        "set_name",
        # "set_type",
        # "set_uri",
        # "set_search_uri",
        # "scryfall_set_uri",
        # "rulings_uri",
        # "prints_search_uri",
        # "collector_number",
        # "digital",
        "rarity",
        # "flavor_text",
        # "card_back_id",
        # "artist",
        # "artist_ids",
        # "illustration_id",
        # "border_color",
        # "frame",
        # "full_art",
        # "textless",
        # "booster",
        # "story_spotlight",
        # "promo_types",
        # "edhrec_rank",
        "prices",
        # "related_uris",
        # "purchase_uris",
    ]
    card_dict = {key: value for key, value in card.to_dict().items() if key in fields}

    # Condense legalities to save on tokens
    card_dict["legalities"] = [
        key
        for key, value in card_dict.get("legalities", {}).items()
        if value == "legal"
    ]

    # Get card oracle tags
    if CARD_TAG_MAP:
        card_dict["oracle_tags"] = CARD_TAG_MAP.get(card.oracle_id, [])

    return card_dict


def search_cards(q: str, offset: int = 0, limit: int = 60) -> list[Object]:
    """Search for cards matching a query string."""

    # Get the search result
    results = scrython.cards.Search(q=q, order="name")

    # Exit early if there are no results
    if results.total_cards == 0:
        return []

    # Paginate through results and fetch the cards in the requested window
    i = 0
    start = offset
    end = offset + limit
    cards: list[Object] = []
    for card in results.iter_all(cache=True, cache_ttl=3600):
        if i >= start and i <= end:
            cards.append(card)

        i += 1
        if i > end:
            break

    return cards
