"""Tests for the trolley system module."""

import pytest
from emerald_shadows.trolley_system import TrolleySystem

@pytest.fixture
def trolley():
    """Create a TrolleySystem instance for testing."""
    return TrolleySystem()

def test_trolley_initialization(trolley):
    """Test that TrolleySystem initializes correctly."""
    assert trolley.current_stop == 0
    assert not trolley.on_trolley

def test_board_trolley(trolley):
    """Test boarding the trolley."""
    assert trolley.board_trolley()
    assert trolley.on_trolley
    
    # Test boarding when already on trolley
    assert not trolley.board_trolley()

def test_exit_trolley(trolley):
    """Test exiting the trolley."""
    trolley.board_trolley()
    assert trolley.exit_trolley() == "pike_place"
    assert not trolley.on_trolley
    
    # Test exiting when not on trolley
    assert trolley.exit_trolley() is None

def test_next_stop(trolley):
    """Test moving to next trolley stop."""
    # Test when not on trolley
    assert not trolley.next_stop()
    
    # Test when on trolley
    trolley.board_trolley()
    current_stop = trolley.current_stop
    assert trolley.next_stop()
    assert trolley.current_stop == (current_stop + 1) % 4  # 4 stops total

def test_get_stop_description(trolley):
    """Test getting stop descriptions."""
    # Test when not on trolley
    assert "not on the trolley" in trolley.get_stop_description().lower()
    
    # Test when on trolley
    trolley.board_trolley()
    description = trolley.get_stop_description()
    assert "Stop" in description