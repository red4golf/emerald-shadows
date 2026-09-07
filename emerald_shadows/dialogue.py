"""Conversation system for Emerald Shadows.

A detective game needs a way to lean on somebody. Topics are global knowledge:
learning that there's a blue sedan worth asking about lets Diamond raise it with
anyone in the city, and different people know different pieces. That's the loop —
you go back around town because you have a better question than you had before.
"""

from __future__ import annotations

import logging
from typing import Dict, List, Optional, Set

from .config_dialogue import NPCS, STARTING_TOPICS, TOPICS, npc_at, resolve_npc, resolve_topic
from .utils import print_text


class DialogueManager:
    """Tracks what Diamond knows to ask and who he has already worked over."""

    def __init__(self) -> None:
        self.known_topics: Set[str] = set(STARTING_TOPICS)
        self.met: Set[str] = set()
        self.spoken: Set[str] = set()  # "npc:topic" pairs already fully answered

    # ------------------------------------------------------------------
    # Knowledge
    # ------------------------------------------------------------------
    def learn(self, *topics: str, announce: bool = True) -> List[str]:
        """Add topics to what Diamond knows to ask about. Returns the new ones."""
        gained = [t for t in topics if t in TOPICS and t not in self.known_topics]
        self.known_topics.update(gained)
        if gained and announce:
            labels = ", ".join(TOPICS[t]["label"] for t in gained)
            print_text(f"\n[New line of questioning: {labels}]")
        return gained

    def knows(self, topic: str) -> bool:
        return topic in self.known_topics

    def list_topics(self) -> None:
        """Show what Diamond currently knows to ask about."""
        if not self.known_topics:
            print_text("\nYou haven't got a question worth asking yet.")
            return
        print_text("\nYou know to ask about:")
        for key in sorted(self.known_topics, key=lambda k: TOPICS[k]["label"].lower()):
            print_text(f"  - {TOPICS[key]['label']}")
        print_text("\nTry 'ask <person> about <topic>'.")

    # ------------------------------------------------------------------
    # Talking
    # ------------------------------------------------------------------
    def people_here(self, location: str, act: int) -> List[str]:
        return npc_at(location, act)

    def describe_presence(self, location: str, act: int) -> Optional[str]:
        """One line naming who's available to talk to here, or None."""
        keys = self.people_here(location, act)
        if not keys:
            return None
        described = [f"{NPCS[k]['name']} ({NPCS[k]['title']})" for k in keys]
        return "Here with you: " + ", ".join(described)

    def talk_to(self, target: str, location: str, act: int, game_state: Dict) -> bool:
        """Open a conversation. Returns True if somebody answered."""
        key = self._find_present(target, location, act)
        if not key:
            return False

        npc = NPCS[key]
        if not self._gate_ok(npc, game_state):
            print_text("\n" + npc.get("locked", "They've nothing to say to you."))
            return True

        if key not in self.met:
            self.met.add(key)
            print_text("\n" + npc["greeting"])
        else:
            print_text(f"\n{npc['name']} waits. You've been here before; he knows the shape of it.")

        self._show_available(key)
        return True

    def ask(
        self,
        target: str,
        topic_word: str,
        location: str,
        act: int,
        game_state: Dict,
    ) -> Optional[str]:
        """Ask somebody about something.

        Returns the key of an item they handed over, if any, so the caller can
        place it in the world.
        """
        key = self._find_present(target, location, act)
        if not key:
            return None

        npc = NPCS[key]
        if not self._gate_ok(npc, game_state):
            print_text("\n" + npc.get("locked", "They've nothing to say to you."))
            return None

        if key not in self.met:
            self.met.add(key)
            print_text("\n" + npc["greeting"])

        topic = resolve_topic(topic_word)
        if not topic:
            print_text(
                "\nYou'd have to put that more plainly. ('topics' lists what you know "
                "to ask about.)"
            )
            return None

        if not self.knows(topic):
            print_text(
                "\nYou don't know enough to ask that yet — and a question you can't "
                "back up is a question that warns somebody."
            )
            return None

        entry = npc["topics"].get(topic)
        if entry is None:
            print_text("\n" + npc.get("deflection", "They shake their head."))
            return None

        return self._deliver(key, topic, entry, game_state)

    # ------------------------------------------------------------------
    # Internals
    # ------------------------------------------------------------------
    def _deliver(self, key: str, topic: str, entry: Dict, game_state: Dict) -> Optional[str]:
        """Print a topic response and apply its effects once."""
        npc = NPCS[key]
        pair = f"{key}:{topic}"
        repeat = pair in self.spoken

        if repeat and entry.get("once"):
            print_text(
                f"\n{npc['name']} has given you that already, and giving it again would "
                "cost him more than it would give you."
            )
            return None

        print_text("\n" + entry["text"])

        if repeat:
            return None
        self.spoken.add(pair)

        self.learn(*entry.get("unlocks", []))

        flag = entry.get("sets")
        if flag:
            game_state[flag] = True

        fragment = entry.get("fragment")
        if fragment:
            fragments = list(game_state.get("plate_fragments", []))
            if fragment not in fragments:
                fragments.append(fragment)
                game_state["plate_fragments"] = fragments
                print_text("\n[You write it in the notebook.]")

        points = entry.get("score", 0)
        if points:
            game_state["score"] = game_state.get("score", 0) + points

        granted = entry.get("gives")
        if granted:
            logging.info("Dialogue granted item %s from %s", granted, key)
        return granted

    def _find_present(self, target: str, location: str, act: int) -> str:
        """Resolve a name to somebody actually standing here."""
        present = self.people_here(location, act)
        if not present:
            print_text("\nThere's nobody here worth the breath.")
            return ""

        if not target.strip():
            if len(present) == 1:
                return present[0]
            names = ", ".join(NPCS[k]["name"] for k in present)
            print_text(f"\nTalk to whom? {names}.")
            return ""

        key = resolve_npc(target)
        if not key:
            names = ", ".join(NPCS[k]["name"] for k in present)
            print_text(f"\nThere's no {target} here. {names} is who you've got.")
            return ""
        if key not in present:
            npc = NPCS[key]
            print_text(
                f"\n{npc['name']} isn't here. Last you knew, {npc['title']}."
            )
            return ""
        return key

    @staticmethod
    def _gate_ok(npc: Dict, game_state: Dict) -> bool:
        gate = npc.get("requires")
        return bool(game_state.get(gate, False)) if gate else True

    def _show_available(self, key: str) -> None:
        """List the topics this person will actually engage with."""
        npc = NPCS[key]
        answerable = [t for t in npc["topics"] if t in self.known_topics]
        if not answerable:
            print_text(
                "\nYou haven't got a question for him yet. Go and find one."
            )
            return
        labels = ", ".join(TOPICS[t]["label"] for t in sorted(answerable))
        print_text(f"\nYou could ask about: {labels}.")

    # ------------------------------------------------------------------
    # Persistence
    # ------------------------------------------------------------------
    def get_state(self) -> Dict:
        return {
            "known_topics": sorted(self.known_topics),
            "met": sorted(self.met),
            "spoken": sorted(self.spoken),
        }

    def restore_state(self, state: Optional[Dict]) -> None:
        """Restore from save data. Saves predating dialogue restore to the start."""
        state = state or {}
        self.known_topics = set(state.get("known_topics", STARTING_TOPICS))
        self.met = set(state.get("met", []))
        self.spoken = set(state.get("spoken", []))
