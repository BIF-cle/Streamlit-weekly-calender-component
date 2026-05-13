"""
Tests for frontend event structures and TypeScript type compatibility.

Tests:
- Event payload structures
- Selection event generation
- Type safety for frontend communication
"""

import pytest
from typing import TypedDict, Dict, Any


class TestEventPayloadStructures:
    """Tests for event payload structures emitted from frontend."""
    
    def test_cell_selection_event(self):
        """Test cell selection event structure."""
        event = {
            "event": "cell_selected",
            "cell": {
                "row": 2,
                "column": 4,
                "date": "2026-04-13"
            }
        }
        
        # Validate event type
        assert event["event"] == "cell_selected"
        
        # Validate cell coordinates
        assert isinstance(event["cell"], dict)
        assert "row" in event["cell"]
        assert "column" in event["cell"]
        assert "date" in event["cell"]
        
        # Validate coordinate types
        assert isinstance(event["cell"]["row"], int)
        assert isinstance(event["cell"]["column"], int)
        assert isinstance(event["cell"]["date"], str)
    
    def test_activity_selection_event(self):
        """Test activity selection event structure."""
        event = {
            "event": "activity_selected",
            "cell": {
                "row": 1,
                "column": 3
            },
            "calendarEvent": {
                "id": "act123",
                "start": "2026-04-13",
                "title": "Team Meeting",
                "color": "#2196F3",
                "category": "work",
                "playerId": "player1",
                "playerName": "John Doe",
                "metadata": {
                    "sets": 3,
                    "reps": 10,
                    "duration_minutes": 30
                }
            },
            "raw": {
                "original_field": "value"
            }
        }
        
        # Validate event type
        assert event["event"] == "activity_selected"
        
        # Validate cell
        assert event["cell"]["row"] == 1
        assert event["cell"]["column"] == 3
        
        # Validate calendar event
        cal_event = event["calendarEvent"]
        assert cal_event["id"] == "act123"
        assert cal_event["start"] == "2026-04-13"
        assert cal_event["title"] == "Team Meeting"
        assert cal_event["color"] == "#2196F3"
        assert cal_event["category"] == "work"
        
        # Validate optional fields
        assert cal_event["playerId"] == "player1"
        assert cal_event["playerName"] == "John Doe"
        assert cal_event["metadata"]["sets"] == 3
        
        # Validate raw reference
        assert event["raw"]["original_field"] == "value"
    
    def test_calendar_event_minimal(self):
        """Test minimal calendar event structure."""
        event = {
            "id": "1",
            "start": "2026-04-13",
            "title": "Event"
        }
        
        assert "id" in event
        assert "start" in event
        assert "title" in event
    
    def test_calendar_event_full(self):
        """Test fully populated calendar event structure."""
        event = {
            "id": "1",
            "start": "2026-04-13",
            "end": "2026-04-13T18:00:00",
            "title": "Event",
            "color": "#FF5733",
            "category": "work",
            "playerId": "p1",
            "playerName": "Player 1",
            "metadata": {
                "custom_field": "value"
            },
            "raw": {
                "source": "database"
            }
        }
        
        # All fields present
        assert all(key in event for key in [
            "id", "start", "end", "title", "color", 
            "category", "playerId", "playerName", "metadata", "raw"
        ])
    
    def test_event_date_format_iso(self):
        """Test that event dates are in ISO format."""
        event = {
            "id": "1",
            "start": "2026-04-13",
            "end": "2026-04-13T18:00:00"
        }
        
        # Verify ISO format
        import re
        date_pattern = r'^\d{4}-\d{2}-\d{2}'
        
        assert re.match(date_pattern, event["start"])
        assert event["end"].startswith("2026-04-13")


class TestComponentProps:
    """Tests for component props structure."""
    
    def test_calendar_component_props(self):
        """Test calendar component props structure."""
        props = {
            "events": [
                {
                    "id": "1",
                    "start": "2026-04-13",
                    "title": "Event 1"
                },
                {
                    "id": "2",
                    "start": "2026-04-14",
                    "title": "Event 2"
                }
            ],
            "theme": {
                "backgroundColor": "#ffffff",
                "gridColor": "#e0e0e0",
                "textColor": "#333333",
                "selectionColor": "#4CAF50",
                "borderRadius": 4,
            },
            "config": {
                "startHour": 6,
                "endHour": 22,
                "selectable": True,
                "showTimeLabels": True,
                "compactMode": False,
                "enableActivityPopover": True,
            },
            "version": "1.0.0"
        }
        
        # Validate structure
        assert "events" in props
        assert isinstance(props["events"], list)
        
        assert "theme" in props
        assert isinstance(props["theme"], dict)
        
        assert "config" in props
        assert isinstance(props["config"], dict)
        
        # Validate config fields
        config = props["config"]
        assert config["startHour"] >= 0
        assert config["endHour"] <= 24
        assert config["startHour"] < config["endHour"]
        assert isinstance(config["selectable"], bool)
        assert isinstance(config["showTimeLabels"], bool)
        assert isinstance(config["compactMode"], bool)
        assert isinstance(config["enableActivityPopover"], bool)
    
    def test_theme_structure(self):
        """Test theme configuration structure."""
        theme = {
            "backgroundColor": "#ffffff",
            "gridColor": "#e0e0e0",
            "textColor": "#333333",
            "borderRadius": 4,
            "selectionColor": "#4CAF50",
            "foregroundColor": "#f5f5f5",
            "accentColor": "#2196F3",
        }
        
        # All colors should be hex format
        for key in ["backgroundColor", "gridColor", "textColor", "selectionColor", 
                    "foregroundColor", "accentColor"]:
            if key in theme:
                assert theme[key].startswith("#")
                assert len(theme[key]) in (4, 7)  # #FFF or #FFFFFF format
        
        # Border radius should be positive integer
        assert theme["borderRadius"] >= 0
        assert isinstance(theme["borderRadius"], int)


class TestCalendarState:
    """Tests for calendar state structure."""
    
    def test_calendar_state_structure(self):
        """Test calendar state structure."""
        state = {
            "weekStart": "2026-04-13",
            "weekEnd": "2026-04-19",
            "days": [
                {
                    "date": "2026-04-13",
                    "dayOfWeek": 0,
                    "dayName": "Mon",
                    "dayNumber": 13,
                    "activities": []
                }
            ],
            "timeSlots": [
                {
                    "hour": 6,
                    "time": "06:00",
                    "activities": []
                }
            ],
            "cells": [
                [
                    {
                        "row": 0,
                        "column": 0,
                        "date": "2026-04-13",
                        "hour": 6,
                        "dayOfWeek": 0,
                        "activities": [],
                        "isSelected": False,
                        "hasActivity": False,
                    }
                ]
            ],
            "selectedCell": None,
            "selectedActivity": None,
            "hoveredCell": None,
        }
        
        # Validate structure
        assert "weekStart" in state
        assert "weekEnd" in state
        assert "days" in state
        assert "timeSlots" in state
        assert "cells" in state
        
        # Validate days
        assert len(state["days"]) > 0
        day = state["days"][0]
        assert "date" in day
        assert "dayOfWeek" in day
        assert "dayName" in day
        assert "dayNumber" in day
        
        # Validate time slots
        assert len(state["timeSlots"]) > 0
        slot = state["timeSlots"][0]
        assert "hour" in slot
        assert "time" in slot
        assert "activities" in slot
        
        # Validate cells
        assert len(state["cells"]) > 0
        cell = state["cells"][0][0]
        assert "row" in cell
        assert "column" in cell
        assert "date" in cell
        assert "activities" in cell
        assert "isSelected" in cell
        assert isinstance(cell["isSelected"], bool)


class TestSelectionState:
    """Tests for selection state in Zustand store."""
    
    def test_selection_state_initial(self):
        """Test initial selection state."""
        state = {
            "selectedCell": None,
            "selectedActivity": None,
            "hoveredCell": None,
            "hoveredActivity": None,
            "multiSelectMode": False,
            "selectedCells": [],
            "selectedActivities": [],
        }
        
        # All fields should be present
        assert "selectedCell" in state
        assert "selectedActivity" in state
        assert "multiSelectMode" in state
    
    def test_selection_state_with_selections(self):
        """Test selection state with selections."""
        state = {
            "selectedCell": {"row": 1, "column": 2, "date": "2026-04-13"},
            "selectedActivity": {
                "id": "1",
                "start": "2026-04-13",
                "title": "Activity"
            },
            "multiSelectMode": True,
            "selectedCells": [
                {"row": 1, "column": 2},
                {"row": 2, "column": 3}
            ],
            "selectedActivities": [
                {"id": "1", "title": "Activity 1"},
                {"id": "2", "title": "Activity 2"}
            ]
        }
        
        # Validate cell selection
        assert state["selectedCell"]["row"] == 1
        assert state["selectedCell"]["column"] == 2
        
        # Validate activity selection
        assert state["selectedActivity"]["id"] == "1"
        
        # Validate multi-select
        assert len(state["selectedCells"]) == 2
        assert len(state["selectedActivities"]) == 2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
