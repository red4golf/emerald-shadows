"""Tests for the conversation system."""

from copy import deepcopy

import pytest

from emerald_shadows.config import INITIAL_GAME_STATE
from emerald_shadows.config_dialogue import NPCS, TOPICS, resolve_npc, resolve_topic
from emerald_shadows.dialogue import DialogueManager


@pytest.fixture
def dialogue():
    return DialogueManager()


@pytest.fixture
def state():
    return deepcopy(INITIAL_GAME_STATE)


# --- resolving who and what ---

@pytest.mark.parametrize("word,expected", [
    ("ches", "ches"),
    ("Ches", "ches"),
    ("barman", "ches"),
    ("harold", "harold"),
    ("operator", "harold"),
    ("motorman", "roy"),
    ("night porter", "porter"),
])
def test_resolve_npc(word, expected):
    assert resolve_npc(word) == expected


def test_resolve_npc_rejects_strangers():
    assert resolve_npc("the mayor") == ""
    assert resolve_npc("") == ""


@pytest.mark.parametrize("word,expected", [
    ("harbormaster", "harbormaster"),
    ("the harbormaster", "harbormaster"),
    ("blue sedan", "sedan"),
    ("the car", "sedan"),
    ("medical supplies", "supplies"),
    ("415.6", "frequency"),
])
def test_resolve_topic(word, expected):
    assert resolve_topic(word) == expected


def test_resolve_topic_rejects_nonsense():
    assert resolve_topic("the weather") == ""


# --- knowledge ---

def test_starts_knowing_the_basics(dialogue):
    assert dialogue.knows("case")
    assert dialogue.knows("supplies")
    assert not dialogue.knows("harbormaster")


def test_learning_a_topic(dialogue):
    gained = dialogue.learn("harbormaster", announce=False)
    assert gained == ["harbormaster"]
    assert dialogue.knows("harbormaster")


def test_learning_is_idempotent(dialogue):
    dialogue.learn("harbormaster", announce=False)
    assert dialogue.learn("harbormaster", announce=False) == []


def test_learning_ignores_unknown_topics(dialogue):
    assert dialogue.learn("not_a_topic", announce=False) == []


# --- presence ---

def test_people_are_placed_in_their_locations(dialogue):
    assert dialogue.people_here("anchor_tavern", 1) == ["ches"]
    assert dialogue.people_here("smith_tower", 1) == ["harold"]
    assert dialogue.people_here("street", 1) == []


def test_mathers_only_appears_in_act_two(dialogue):
    assert dialogue.people_here("police_station", 1) == []
    assert dialogue.people_here("police_station", 2) == ["mathers"]


def test_describe_presence_names_who_is_here(dialogue):
    assert "Ches" in dialogue.describe_presence("anchor_tavern", 1)
    assert dialogue.describe_presence("street", 1) is None


# --- asking ---

def test_asking_a_known_topic_sets_its_flag(dialogue, state):
    dialogue.learn("harbormaster", announce=False)
    dialogue.ask("ches", "harbormaster", "anchor_tavern", 1, state)
    assert state["heard_harbormaster"] is True


def test_asking_awards_score_once(dialogue, state):
    dialogue.learn("harbormaster", announce=False)
    dialogue.ask("ches", "harbormaster", "anchor_tavern", 1, state)
    first = state["score"]
    dialogue.ask("ches", "harbormaster", "anchor_tavern", 1, state)
    assert state["score"] == first


def test_asking_unlocks_further_topics(dialogue, state):
    dialogue.ask("ches", "supplies", "anchor_tavern", 1, state)
    assert dialogue.knows("harbormaster")


def test_cannot_ask_about_what_you_do_not_know(dialogue, state, capsys):
    dialogue.ask("ches", "harbormaster", "anchor_tavern", 1, state)
    assert state["heard_harbormaster"] is False
    assert "don't know enough" in capsys.readouterr().out


def test_asking_someone_who_is_absent(dialogue, state, capsys):
    dialogue.learn("harbormaster", announce=False)
    dialogue.ask("ches", "harbormaster", "smith_tower", 1, state)
    assert state["heard_harbormaster"] is False
    assert "isn't here" in capsys.readouterr().out


def test_asking_in_an_empty_room(dialogue, state, capsys):
    dialogue.ask("ches", "case", "street", 1, state)
    assert "nobody here" in capsys.readouterr().out.lower()


def test_deflection_for_a_topic_they_have_nothing_on(dialogue, state, capsys):
    dialogue.learn("frequency", announce=False)
    dialogue.ask("ches", "frequency", "anchor_tavern", 1, state)
    assert "not my end of the bar" in capsys.readouterr().out.lower()


# --- plate fragments ---

def test_asking_about_the_sedan_yields_a_plate_fragment(dialogue, state):
    dialogue.learn("sedan", announce=False)
    dialogue.ask("ches", "sedan", "anchor_tavern", 1, state)
    assert "ches" in state["plate_fragments"]


def test_fragments_are_not_duplicated(dialogue, state):
    dialogue.learn("sedan", announce=False)
    dialogue.ask("ches", "sedan", "anchor_tavern", 1, state)
    dialogue.ask("ches", "sedan", "anchor_tavern", 1, state)
    assert state["plate_fragments"].count("ches") == 1


# --- items handed over ---

def test_the_motorman_hands_over_the_informant_note(dialogue, state):
    dialogue.learn("frequency", announce=False)
    granted = dialogue.ask("roy", "frequency", "trolley", 1, state)
    assert granted == "informant_note"
    assert state["roy_gave_note"] is True


def test_the_motorman_will_not_hand_it_over_twice(dialogue, state):
    dialogue.learn("frequency", announce=False)
    dialogue.ask("roy", "frequency", "trolley", 1, state)
    assert dialogue.ask("roy", "frequency", "trolley", 1, state) is None


# --- gated people ---

def test_porter_refuses_without_a_badge(dialogue, state, capsys):
    dialogue.learn("eagles", announce=False)
    dialogue.ask("porter", "eagles", "eagles_hall", 1, state)
    assert state["porter_relented"] is False
    assert "members only" in capsys.readouterr().out.lower()


def test_porter_talks_once_you_have_the_badge(dialogue, state):
    state["has_badge"] = True
    dialogue.learn("voss", announce=False)
    dialogue.ask("porter", "voss", "eagles_hall", 1, state)
    assert state["porter_relented"] is True


# --- persistence ---

def test_state_round_trips(dialogue, state):
    dialogue.learn("harbormaster", announce=False)
    dialogue.ask("ches", "harbormaster", "anchor_tavern", 1, state)

    restored = DialogueManager()
    restored.restore_state(dialogue.get_state())
    assert restored.known_topics == dialogue.known_topics
    assert restored.met == dialogue.met
    assert restored.spoken == dialogue.spoken


def test_restore_from_a_save_predating_dialogue(dialogue):
    dialogue.restore_state(None)
    assert dialogue.knows("case")
    assert not dialogue.knows("harbormaster")


# --- content integrity ---

def test_every_npc_topic_is_a_real_topic():
    for key, npc in NPCS.items():
        for topic in npc["topics"]:
            assert topic in TOPICS, f"{key} answers unknown topic {topic}"


def test_every_unlocked_topic_is_a_real_topic():
    for key, npc in NPCS.items():
        for topic, entry in npc["topics"].items():
            for unlocked in entry.get("unlocks", []):
                assert unlocked in TOPICS, f"{key}:{topic} unlocks unknown {unlocked}"


def test_every_npc_location_exists():
    from emerald_shadows.config_locations import LOCATIONS

    for key, npc in NPCS.items():
        assert npc["location"] in LOCATIONS, f"{key} stands in a room that doesn't exist"
