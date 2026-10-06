"""Regression cover for the defects two cold playtesters found.

Both testers were stopped by the same root cause from opposite directions: one
read the tram as broken, the other as a missing item. Each test here names the
player-visible symptom, because that's what a future change would reintroduce.
"""

from copy import deepcopy

import pytest

from emerald_shadows import acts, casebook
from emerald_shadows.config import INITIAL_GAME_STATE
from emerald_shadows.config_dialogue import NPCS, TOPICS, resolve_topic
from emerald_shadows.location_manager import LocationManager


@pytest.fixture
def state():
    return deepcopy(INITIAL_GAME_STATE)


# ---------------------------------------------------------------------------
# The unwinnable bug: `topics` printed phrasings that `ask` refused
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("key", list(TOPICS))
def test_every_printed_topic_label_is_accepted(key):
    """`topics` prints the label; `ask` parses it. If those disagree the game
    rejects its own wording — and four labels did, including both steps of the
    only route to the informant's note, which made the case impossible."""
    assert resolve_topic(TOPICS[key]["label"]) == key


@pytest.mark.parametrize("key", list(TOPICS))
def test_topic_keys_and_aliases_resolve(key):
    for probe in [key, *TOPICS[key].get("aliases", ())]:
        assert resolve_topic(probe) == key, f"{probe!r} should resolve to {key!r}"


@pytest.mark.parametrize("junk", ["the weather", "pizza", "", "   ", "xyzzy"])
def test_nonsense_topics_still_rejected(junk):
    assert resolve_topic(junk) == ""


def test_the_route_to_the_informants_note_is_askable():
    """Walk the actual chain: supplies unlocks frequency, frequency hands over
    the note. Both labels have to survive a round trip or Act 3 never opens."""
    giver = [
        (npc, topic)
        for npc, data in NPCS.items()
        for topic, entry in data["topics"].items()
        if entry.get("gives") == "informant_note"
    ]
    assert giver, "nobody gives the informant_note any more"
    npc, gift_topic = giver[0]

    unlockers = [
        topic
        for topic, entry in NPCS[npc]["topics"].items()
        if gift_topic in entry.get("unlocks", [])
    ]
    assert unlockers, f"no topic unlocks {gift_topic!r}"

    for topic in [gift_topic, *unlockers]:
        label = TOPICS[topic]["label"]
        assert resolve_topic(label) == topic, (
            f"the game prints {label!r} but will not accept it — "
            "this is the bug that made the case unwinnable"
        )


# ---------------------------------------------------------------------------
# Re-entering a room shouldn't reprint the whole paragraph
# ---------------------------------------------------------------------------

def test_second_visit_is_shorter_than_the_first():
    lm = LocationManager()
    first = lm.get_location_description()
    second = lm.get_location_description()
    assert len(second) < len(first)


def test_brief_form_keeps_what_the_player_navigates_by():
    lm = LocationManager()
    lm.get_location_description()
    brief = lm.get_location_description()
    assert "Exits:" in brief
    assert "You can see:" in brief


def test_look_always_gives_the_full_text():
    """Abbreviating is for the automatic on-entry display. Asking to look is a
    deliberate act and should always be answered in full."""
    lm = LocationManager()
    lm.get_location_description()
    assert lm.get_location_description(brief=False) == lm.get_location_description(brief=False)
    assert len(lm.get_location_description(brief=False)) > len(
        lm.get_location_description(brief=True)
    )


# ---------------------------------------------------------------------------
# The Pier 7 gate must describe itself truthfully
# ---------------------------------------------------------------------------

def test_pier_gate_names_only_what_is_actually_missing(state):
    state["found_warehouse"] = True
    state["identified_suspect"] = True
    message = acts.pier_gate_message(state)

    assert acts.ACT_THREE_GAPS["identified_vehicle"] in message
    assert acts.ACT_THREE_GAPS["observed_activity"] in message
    # Things the player has established must not be listed against them.
    assert acts.ACT_THREE_GAPS["found_warehouse"] not in message
    assert acts.ACT_THREE_GAPS["identified_suspect"] not in message


def test_pier_gate_covers_every_act_three_requirement():
    """A requirement with no phrasing would vanish from the refusal and leave
    the player hunting for something the game never mentions."""
    assert set(acts.ACT_THREE_GAPS) == set(acts.ACT_REQUIREMENTS[3])


def test_pier_gate_opens_once_everything_is_in_hand(state):
    for flag in acts.ACT_REQUIREMENTS[3]:
        state[flag] = True
    assert "finish it" in acts.pier_gate_message(state).lower()


# ---------------------------------------------------------------------------
# Opening the map must not strand the one tram-only witness
# ---------------------------------------------------------------------------

def test_casebook_points_at_the_waterfront_line_while_the_radio_is_open(state):
    """Roy rides the tram and is the sole source of the informant's note. With
    everywhere else now walkable, the casebook is what keeps him findable."""
    rendered = casebook.render(state, [], {})
    assert "waterfront" in rendered.lower()
