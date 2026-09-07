"""An end-to-end walkthrough.

This is the test that matters most: it drives the real parser and the real
command loop from the bullpen to the arrest at Pier 7, and proves the case can
actually be closed. It also pins the intended solution path, so a change that
makes the game unwinnable fails here rather than in somebody's playthrough.
"""

import pytest

from emerald_shadows import acts
from emerald_shadows.game_manager import GameManager


@pytest.fixture
def game(tmp_path, monkeypatch):
    """A game whose saves land in a temp dir and whose output is discarded."""
    monkeypatch.chdir(tmp_path)
    game = GameManager()
    # The car puzzle is the one that still takes a typed answer.
    game.puzzle_manager.solution_provider = lambda location: "WA-4471"
    return game


def play(game, *commands):
    """Run a sequence of commands the way the game loop would."""
    for command in commands:
        game.process_command(command.strip().lower())
        game.check_act_progress()


def ride_to(game, stop_name):
    """Board the tram and ride until the named stop, then step off."""
    for _ in range(12):
        if game.location_manager.trolley.routes[
            game.location_manager.trolley.position
        ]["exits"]["off"] == stop_name and not game.location_manager.trolley.in_motion:
            play(game, "off")
            return
        play(game, "next")
    raise AssertionError(f"never reached {stop_name}")


def test_full_walkthrough_closes_the_case(game, capsys):
    state = game.game_state

    # --- Act 1: the bullpen and the evidence room -------------------------
    play(game, "take all")
    assert "badge" in game.item_manager.get_inventory()
    assert "notebook" in game.item_manager.get_inventory()

    play(game, "upstairs", "take all", "examine photo", "examine radio_manual")
    assert "photo" in state["plate_fragments"]
    assert game.dialogue_manager.knows("sedan")

    # The cipher is broken by turning the wheel, not by typing a password.
    play(game, "turn wheel to h")
    assert state["decoded_notes"] is True

    play(game, "combine badge with photo")
    assert state["identified_suspect"] is True

    # --- the Eagles hall: a gated witness ---------------------------------
    play(game, "downstairs", "outside", "west", "take all", "examine membership_register")
    assert game.dialogue_manager.knows("voss")

    play(game, "ask porter about voss")
    assert state["porter_relented"] is True

    play(game, "back", "take all", "hall", "east")
    assert "meeting_minutes" in game.item_manager.get_inventory()

    # --- Smith Tower: one figure of the plate -----------------------------
    play(game, "north", "ask harold about sedan")
    assert "harold" in state["plate_fragments"]

    # --- the tram: the informant who signed himself 'R.' ------------------
    play(game, "trolley", "ask roy about case", "ask roy about supplies")
    assert game.dialogue_manager.knows("frequency")

    play(game, "ask roy about frequency", "take informant_note", "examine informant_note")
    assert "informant_note" in game.item_manager.get_inventory()
    assert state["found_emergency_frequency"] is True

    # --- Pioneer Square: the organisation ---------------------------------
    ride_to(game, "pioneer_square")
    play(game, "take all", "examine bulletin_notice")
    assert state["identified_organization"] is True

    # Two acts' worth of work is done; the city has noticed.
    assert acts.current_act(state) == 2

    # --- the Anchor: the last figure of the plate -------------------------
    play(game, "north", "south", "trolley")
    ride_to(game, "waterfront")
    play(game, "tavern", "use badge")
    assert state["ches_tip"] is True

    play(game, "ask ches about supplies", "ask ches about harbormaster",
         "ask ches about sullivan", "ask ches about sedan")
    assert "ches" in state["plate_fragments"]

    # --- back to Pioneer Square to name the car ---------------------------
    play(game, "outside", "trolley")
    ride_to(game, "pioneer_square")
    play(game, "solve")
    assert state["identified_vehicle"] is True

    # --- the warehouse office: sweep the band -----------------------------
    play(game, "north", "east", "enter", "take all", "office")
    assert game.location_manager.current_location == "warehouse_office"
    play(game, "tune 415.3")
    assert state["found_warehouse"] is False, "a near miss must not solve it"
    play(game, "tune 415.6")
    assert state["found_warehouse"] is True

    # --- the manifest, off the harbourmaster's shack ----------------------
    play(game, "door", "outside", "south", "shack", "take all", "outside")
    assert "manifest" in game.item_manager.get_inventory()

    # --- the tunnels: decode the tapping ----------------------------------
    play(game, "underground", "use flashlight", "listen")
    assert state["flashlight_lit"] is True
    play(game, "tap W22")
    assert state["observed_activity"] is True

    # --- Act 3 opens Pier 7 ----------------------------------------------
    assert acts.current_act(state) == 3
    assert state["act_three"] is True

    play(game, "up", "south")
    assert game.location_manager.current_location == "pier_seven"

    capsys.readouterr()
    play(game, "arrest")
    assert game.check_game_progress() is True
    assert "EXPENSE ACCOUNT MEMO" in capsys.readouterr().out


def test_pier_seven_is_shut_before_act_three(game, capsys):
    play(game, "outside", "south", "south")
    assert game.location_manager.current_location == "docks"
    assert "Finish the legwork" in capsys.readouterr().out


def test_arrest_without_the_evidence_is_refused(game, capsys):
    # Stand on the pier with nothing in your pockets.
    game.game_state["act_three"] = True
    game.location_manager.current_location = "pier_seven"

    capsys.readouterr()
    play(game, "arrest")
    assert game.check_game_progress() is False
    out = capsys.readouterr().out
    assert "shed door" in out
    assert "the Thursday minutes" in out


def test_arrest_elsewhere_does_nothing(game, capsys):
    capsys.readouterr()
    play(game, "arrest")
    assert game.check_game_progress() is False
    assert "nobody in front of you" in capsys.readouterr().out
