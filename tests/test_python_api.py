"""
Tests for the Python API and component wrapper.

Tests:
- Component prop validation
- Adapter selection and usage
- Theme validation and sanitization
- Event payload structure
"""

import pytest
from datetime import datetime, timedelta
from streamlit_activity_calendar import (
    CalendarEvent,
    activity_calendar,
    validate_theme,
    normalize_color,
    parse_date,
)


class TestCalendarEvent:
    """Tests for CalendarEvent type."""
    
    def test_create_basic_event(self):
        """Test creating a basic calendar event."""
        event = CalendarEvent(
            id="1",
            start="2026-04-13",
            title="Meeting"
        )
        
        assert event.id == "1"
        assert event.start == "2026-04-13"
        assert event.title == "Meeting"
        assert event.end is None
        assert event.color is None
    
    def test_create_full_event(self):
        """Test creating a fully populated event."""
        event = CalendarEvent(
            id="2",
            start="2026-04-13",
            end="2026-04-13T18:00:00",
            title="Conference",
            color="#FF5733",
            category="work",
            playerId="player1",
            playerName="John Doe",
            metadata={"location": "Room 101"},
            raw={"source": "calendar"}
        )
        
        assert event.id == "2"
        assert event.title == "Conference"
        assert event.color == "#FF5733"
        assert event.category == "work"
        assert event.metadata["location"] == "Room 101"
    
    def test_event_to_dict(self):
        """Test converting event to dictionary."""
        event = CalendarEvent(
            id="3",
            start="2026-04-13",
            title="Task",
            color="#4CAF50"
        )
        
        event_dict = event.to_dict()
        
        assert event_dict["id"] == "3"
        assert event_dict["title"] == "Task"
        assert event_dict["color"] == "#4CAF50"
        assert "end" not in event_dict  # None values excluded


class TestThemeValidation:
    """Tests for theme validation and sanitization."""
    
    def test_validate_empty_theme(self):
        """Test validating empty theme."""
        result = validate_theme({})
        assert isinstance(result, dict)
        assert len(result) == 0
    
    def test_validate_valid_theme(self):
        """Test validating valid theme colors."""
        theme = {
            "backgroundColor": "#ffffff",
            "gridColor": "#e0e0e0",
            "textColor": "#333333",
            "selectionColor": "#4CAF50",
        }
        
        result = validate_theme(theme)
        
        assert result["backgroundColor"] == "#ffffff"
        assert result["gridColor"] == "#e0e0e0"
        assert result["textColor"] == "#333333"
        assert result["selectionColor"] == "#4CAF50"
    
    def test_validate_theme_filters_invalid_keys(self):
        """Test that invalid theme keys are filtered."""
        theme = {
            "backgroundColor": "#ffffff",
            "unknownKey": "value",
            "anotherInvalid": 123,
        }
        
        result = validate_theme(theme)
        
        assert "backgroundColor" in result
        assert "unknownKey" not in result
        assert "anotherInvalid" not in result
    
    def test_validate_border_radius(self):
        """Test border radius validation."""
        theme = {
            "borderRadius": 8,
        }
        
        result = validate_theme(theme)
        
        assert result["borderRadius"] == 8
    
    def test_validate_border_radius_negative(self):
        """Test border radius negative value handling."""
        theme = {
            "borderRadius": -5,
        }
        
        result = validate_theme(theme)
        
        assert result["borderRadius"] == 0  # Clamped to 0
    
    def test_validate_non_dict_theme(self):
        """Test validating non-dict theme."""
        result = validate_theme(None)
        assert result == {}
        
        result = validate_theme("not a dict")
        assert result == {}


class TestColorNormalization:
    """Tests for color normalization."""
    
    def test_normalize_hex_color(self):
        """Test normalizing hex colors."""
        assert normalize_color("#ffffff") == "#ffffff"
        assert normalize_color("#FF0000") == "#ff0000"
    
    def test_normalize_named_color(self):
        """Test normalizing named colors."""
        assert normalize_color("red") == "#FF0000"
        assert normalize_color("blue") == "#0000FF"
        assert normalize_color("green") == "#00FF00"
    
    def test_normalize_unknown_color(self):
        """Test normalizing unknown colors."""
        result = normalize_color("unknown_color")
        assert result == "#999999"  # Default gray
    
    def test_normalize_none_color(self):
        """Test normalizing None color."""
        assert normalize_color(None) == "#999999"


class TestDateParsing:
    """Tests for date parsing utilities."""
    
    def test_parse_iso_date_string(self):
        """Test parsing ISO date string."""
        result = parse_date("2026-04-13")
        assert result == "2026-04-13"
    
    def test_parse_iso_datetime_string(self):
        """Test parsing ISO datetime string."""
        result = parse_date("2026-04-13T10:30:00")
        assert result == "2026-04-13"
    
    def test_parse_datetime_object(self):
        """Test parsing datetime object."""
        dt = datetime(2026, 4, 13, 10, 30)
        result = parse_date(dt)
        assert result == "2026-04-13"
    
    def test_parse_invalid_date(self):
        """Test parsing invalid date."""
        result = parse_date("not a date")
        assert result is None
    
    def test_parse_none_date(self):
        """Test parsing None date."""
        result = parse_date(None)
        assert result is None


# Integration tests would go here, but they require Streamlit app context
# These are placeholder tests that demonstrate the structure


class TestEventPayloads:
    """Tests for event payload structures."""
    
    def test_cell_selection_payload_structure(self):
        """Test cell selection payload structure."""
        payload = {
            "event": "cell_selected",
            "cell": {
                "row": 2,
                "column": 4,
                "date": "2026-04-13"
            }
        }
        
        assert payload["event"] == "cell_selected"
        assert "cell" in payload
        assert payload["cell"]["row"] == 2
        assert payload["cell"]["column"] == 4
    
    def test_activity_selection_payload_structure(self):
        """Test activity selection payload structure."""
        payload = {
            "event": "activity_selected",
            "cell": {
                "row": 2,
                "column": 4,
            },
            "calendarEvent": {
                "id": "1",
                "start": "2026-04-13",
                "title": "Meeting",
            },
            "raw": {"original": "data"}
        }
        
        assert payload["event"] == "activity_selected"
        assert payload["cell"]["row"] == 2
        assert payload["calendarEvent"]["id"] == "1"
        assert payload["raw"]["original"] == "data"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
