from emerald_shadows.config import INITIAL_GAME_STATE
from emerald_shadows.item_manager import ItemManager
from emerald_shadows.location_manager import LocationManager


def test_taking_badge_updates_inventory_and_location():
    location_manager = LocationManager()
    item_manager = ItemManager()
    game_state = INITIAL_GAME_STATE.copy()

    available = location_manager.get_available_items()
    assert "badge" in available

    assert item_manager.take_item("badge", available, game_state) is True
    location_manager.remove_item("badge")

    assert "badge" in item_manager.get_inventory()
    assert game_state["has_badge"] is True
    assert "badge" not in location_manager.get_available_items()


def test_combining_items_decodes_notes():
    item_manager = ItemManager()
    game_state = INITIAL_GAME_STATE.copy()

    item_manager.inventory.extend(["notebook", "cipher_wheel"])

    assert item_manager.combine_items("notebook", "cipher_wheel", game_state) is True
    assert game_state.get("decoded_notes") is True
