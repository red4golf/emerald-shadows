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


# ---------------------------------------------------------------------------
# Round two: what the retest on the fixed build turned up
# ---------------------------------------------------------------------------

def test_the_business_card_names_the_front(state):
    """A tester read note_5 — a card printed NORTHWEST MARITIME IMPORTS — and
    the casebook still listed "you don't have a name for the company" forty
    turns later, stalling them in Act 1 with three puzzles solved."""
    from emerald_shadows.item_manager import EXAMINE_DISCOVERIES, ITEM_DESCRIPTIONS

    assert "Northwest Maritime Imports" in ITEM_DESCRIPTIONS["note_5"]["detailed"]
    assert EXAMINE_DISCOVERIES["note_5"]["sets"] == "identified_organization"


def test_act_two_is_reachable_from_the_card_alone(state):
    """note_5 plus the cipher should be enough to turn the act, without
    requiring the one specific notice at Pioneer Square."""
    state["decoded_notes"] = True
    state["identified_organization"] = True
    assert acts.current_act(state) == 2


def test_casebook_does_not_give_away_the_frequency(state):
    """The informant's note hides the last digit on purpose. The casebook used
    to print 415.6 one command later, cancelling the puzzle."""
    state["found_emergency_frequency"] = True
    rendered = casebook.render(state, [], {})
    assert "415.6" not in rendered
    assert "415" in rendered, "it should still say which band"


def test_the_manifest_does_not_assume_evidence_you_may_not_have():
    """It told players the Eagles minutes were in their other pocket. One who
    had never been to the hall went looking through their inventory for it."""
    from emerald_shadows.item_manager import ITEM_DESCRIPTIONS

    text = ITEM_DESCRIPTIONS["manifest"]["detailed"]
    assert "other pocket" not in text


def test_no_art_env_var_suppresses_the_title_art(monkeypatch, capsys):
    """Both testers were told to set EMERALD_NO_ART=1 and still got a screen of
    banner. It only ever suppressed colour."""
    import emerald_shadows.game_art as art

    monkeypatch.setenv("EMERALD_NO_ART", "1")
    monkeypatch.setattr(art, "clear_screen", lambda: None)
    monkeypatch.setattr("builtins.input", lambda *a: "")
    art.display_title_screen()
    out = capsys.readouterr().out
    assert art.TITLE_ART not in out
    assert art.SEATTLE_SKYLINE not in out
    assert "EMERALD SHADOWS" in out


def test_the_man_in_the_grey_coat_is_a_real_person():
    """Pike Place described him in detail and he could not be spoken to. A
    tester called it the moment the game told him its prose was lying."""
    from emerald_shadows.config_dialogue import NPCS, npc_at, resolve_npc
    from emerald_shadows.config_locations import LOCATIONS

    assert "grey coat" in LOCATIONS["pike_place"]["description"]
    assert npc_at("pike_place", 1), "he must be there from Act 1"

    for probe in ("man", "grey coat", "man in the grey coat", "nilsen"):
        assert resolve_npc(probe) == "watcher", f"{probe!r} should reach him"

    assert NPCS["watcher"]["topics"], "he needs something to say"


def test_pike_place_is_no_longer_an_empty_room():
    """It had no items, no people and no puzzle — a pure waypoint."""
    from emerald_shadows.config_dialogue import npc_at

    assert npc_at("pike_place", 1)


def test_warehouse_22_can_be_learned_in_act_one():
    """Its topic was unlocked only by Mathers, who doesn't appear until Act 2,
    so an Act 1 player could never ask anybody about the hub."""
    from emerald_shadows.config_dialogue import NPCS

    act_one_sources = [
        npc for npc, data in NPCS.items()
        if data.get("requires_act", 1) == 1
        and any("warehouse" in e.get("unlocks", []) for e in data["topics"].values())
    ]
    assert act_one_sources, "nobody in Act 1 opens the Warehouse 22 thread"


def test_every_new_dialogue_flag_is_registered():
    """A flag missing from the initial state never saves and never renders."""
    from emerald_shadows.config_dialogue import NPCS

    known = set(INITIAL_GAME_STATE)
    for npc, data in NPCS.items():
        for topic, entry in data["topics"].items():
            flag = entry.get("sets")
            if flag:
                assert flag in known, f"{npc}:{topic} sets unregistered flag {flag!r}"


def test_second_avenue_describes_where_its_exits_go():
    """Seven exits with no signposting had both testers brute-forcing a hub."""
    from emerald_shadows.config_locations import LOCATIONS

    description = LOCATIONS["street"]["description"].lower()
    for landmark in ("smith tower", "warehouse", "docks", "eagles", "pioneer square", "market"):
        assert landmark in description, f"the street never mentions {landmark}"
