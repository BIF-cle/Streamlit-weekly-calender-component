"""
Type definitions for the activity calendar component.

This module defines the canonical internal event model and supporting types
used throughout the component system.
"""

from typing import Any, Dict, List, Optional, TypedDict, Union
from dataclasses import dataclass, asdict
from datetime import datetime


class CalendarEventDict(TypedDict, total=False):
    """Canonical internal event model for calendar activities.
    
    This is the normalized representation that the React frontend expects.
    All incoming data must be flattened into CalendarEvent[] before rendering.
    """
    id: str
    start: str  # ISO date string or datetime
    end: Optional[str]  # Optional end time
    title: str
    color: Optional[str]  # Hex color code
    category: Optional[str]  # Activity category
    playerId: Optional[str]  # Player/subject identifier
    playerName: Optional[str]  # Player/subject name
    metadata: Optional[Dict[str, Any]]  # Arbitrary metadata
    raw: Optional[Any]  # Original nested object reference


@dataclass
class CalendarEvent:
    """Canonical internal event model.
    
    Represents a single activity on the calendar. All nested domain data
    must be normalized and flattened into instances of this class.
    
    Attributes:
        id: Unique event identifier
        start: ISO date string representing start time
        end: Optional ISO date string for end time
        title: Human-readable event title
        color: Optional hex color code (e.g., "#FF5733")
        category: Optional category label
        playerId: Optional player/subject identifier from domain model
        playerName: Optional player/subject name from domain model
        metadata: Additional structured metadata
        raw: Reference to original nested object for reconstruction
    """
    id: str
    start: str
    title: str
    end: Optional[str] = None
    color: Optional[str] = None
    category: Optional[str] = None
    playerId: Optional[str] = None
    playerName: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    raw: Optional[Any] = None

    def to_dict(self) -> CalendarEventDict:
        """Convert to dictionary representation for JSON serialization."""
        data = asdict(self)
        return {k: v for k, v in data.items() if v is not None}


class CellSelectionPayload(TypedDict, total=False):
    """Payload emitted when a calendar cell is selected.
    
    This represents a click on an empty calendar cell (no activity).
    """
    event: str  # "cell_selected"
    cell: Dict[str, Any]  # {"row": int, "column": int, "date": str}


class ActivitySelectionPayload(TypedDict, total=False):
    """Payload emitted when an activity is selected.
    
    This represents a click on an activity within a calendar cell.
    """
    event: str  # "activity_selected"
    cell: Dict[str, Any]  # {"row": int, "column": int}
    calendarEvent: CalendarEventDict  # Normalized event
    raw: Optional[Any]  # Original domain object


class ThemeConfig(TypedDict, total=False):
    """Safe theming configuration.
    
    Do NOT allow arbitrary CSS injection. Only these predefined
    properties can be customized.
    """
    backgroundColor: str  # Background color (hex)
    gridColor: str  # Grid line color (hex)
    textColor: str  # Text color (hex)
    borderRadius: int  # Border radius in pixels
    selectionColor: str  # Selection highlight color (hex)
    foregroundColor: Optional[str]  # Alternative foreground color
    accentColor: Optional[str]  # Accent color for interactions


class CalendarConfig(TypedDict, total=False):
    """Configuration for the calendar component."""
    startHour: int  # Start hour (0-23)
    endHour: int  # End hour (0-23)
    selectable: bool  # Enable selection interactions
    showTimeLabels: bool  # Show time labels on left
    compactMode: bool  # Compact layout mode
    enableActivityPopover: bool  # Show activity details on click


# Default theme configuration
DEFAULT_THEME: ThemeConfig = {
    "backgroundColor": "#ffffff",
    "gridColor": "#e0e0e0",
    "textColor": "#333333",
    "borderRadius": 4,
    "selectionColor": "#4CAF50",
    "foregroundColor": "#f5f5f5",
    "accentColor": "#2196F3",
}

# Default calendar configuration
DEFAULT_CALENDAR_CONFIG: CalendarConfig = {
    "startHour": 6,
    "endHour": 22,
    "selectable": True,
    "showTimeLabels": True,
    "compactMode": False,
    "enableActivityPopover": True,
}
