"""
Main Streamlit component wrapper for the activity calendar.

This module provides the primary API for integrating the React calendar
component into Streamlit applications.
"""

import os
import json
from typing import Any, Callable, Dict, List, Optional, Union
import streamlit.components.v1 as components

from .types import (
    CalendarEvent,
    CalendarConfig,
    ThemeConfig,
    ActivitySelectionPayload,
    CellSelectionPayload,
    DEFAULT_THEME,
    DEFAULT_CALENDAR_CONFIG,
)
from .adapters import (
    AdapterFunc,
    get_adapter,
    identity_adapter,
    flat_events_adapter,
)
from .utils import (
    validate_theme,
    sanitize_metadata,
    merge_dictionaries,
    parse_date,
)


# Get the absolute path to the component's built directory
_COMPONENT_DIR = os.path.join(os.path.dirname(__file__), "../../frontend/dist")

# Create the component wrapper
_activity_calendar = components.declare_component(
    "activity_calendar",
    path=_COMPONENT_DIR if os.path.exists(_COMPONENT_DIR) else "",
)


def activity_calendar(
    data: Union[List[Dict[str, Any]], Dict[str, Any]],
    adapter: Union[str, AdapterFunc] = "identity",
    theme: Optional[ThemeConfig] = None,
    start_hour: int = 6,
    end_hour: int = 22,
    selectable: bool = True,
    show_time_labels: bool = True,
    compact_mode: bool = False,
    enable_activity_popover: bool = True,
    key: str = "activity_calendar",
) -> Optional[Union[ActivitySelectionPayload, CellSelectionPayload]]:
    """
    Render an interactive activity calendar component in Streamlit.
    
    This component displays a weekly calendar with activities that can be
    selected and interacted with. Data is delivered through an adapter system
    that normalizes arbitrary nested domain structures into calendar events.
    
    Architecture:
    - Remains stateless: all application state in Streamlit session_state
    - Emits interaction events (cell_selected, activity_selected)
    - Data is normalized via adapters before rendering
    - Theme system uses safe predefined properties only
    - Supports arbitrary metadata on activities
    
    Args:
        data: Raw domain data (list or dictionary structure).
              Will be transformed by adapter into CalendarEvent[].
              
        adapter: Adapter to transform data into calendar events.
                 Can be adapter name string ("identity", "flat_events",
                 "medical_rehab", "project_timeline") or custom adapter function.
                 Default: "identity" (assumes data is already flat).
                 
        theme: Optional theme configuration dict. Safe properties:
               - backgroundColor: Background color hex
               - gridColor: Grid line color hex
               - textColor: Text color hex
               - borderRadius: Border radius in pixels
               - selectionColor: Selection highlight hex
               - foregroundColor: Foreground color hex
               - accentColor: Accent color hex
               
        start_hour: Calendar start hour (0-23). Default: 6
        end_hour: Calendar end hour (0-23). Default: 22
        
        selectable: Enable user interaction/selection. Default: True
        
        show_time_labels: Show time labels on calendar. Default: True
        
        compact_mode: Use compact layout. Default: False
        
        enable_activity_popover: Show activity details popover. Default: True
        
        key: Unique component key for Streamlit. Default: "activity_calendar"
    
    Returns:
        Selection payload dict when component emits an event, or None if no event.
        
        Cell selection event:
        {
            "event": "cell_selected",
            "cell": {"row": 2, "column": 4, "date": "2026-04-13"}
        }
        
        Activity selection event:
        {
            "event": "activity_selected",
            "cell": {"row": 2, "column": 4},
            "calendarEvent": {
                "id": "...",
                "title": "...",
                "start": "2026-04-13",
                ...
            },
            "raw": {...original domain object...}
        }
    
    Example:
        >>> from streamlit_activity_calendar import activity_calendar
        >>> 
        >>> events = [
        ...     {
        ...         "id": "1",
        ...         "start": "2026-04-13",
        ...         "title": "Meeting",
        ...         "color": "#4CAF50"
        ...     }
        ... ]
        >>> 
        >>> selection = activity_calendar(
        ...     data=events,
        ...     adapter="flat_events",
        ...     start_hour=8,
        ...     end_hour=18,
        ...     key="my_calendar"
        ... )
        >>> 
        >>> if selection:
        ...     if selection["event"] == "activity_selected":
        ...         st.write(f"Selected activity: {selection['calendarEvent']['title']}")
        ... 
    
    Example with medical rehab data:
        >>> rehab_data = {
        ...     "players": [
        ...         {
        ...             "id": "p1",
        ...             "name": "John Doe",
        ...             "rehab_plans": [
        ...                 {
        ...                     "weeks": [
        ...                         {
        ...                             "days": [
        ...                                 {
        ...                                     "date": "2026-04-13",
        ...                                     "activities": [
        ...                                         {
        ...                                             "id": "a1",
        ...                                             "title": "Quad Sets",
        ...                                             "category": "strengthening",
        ...                                             "sets": 3,
        ...                                             "reps": 10
        ...                                         }
        ...                                     ]
        ...                                 }
        ...                             ]
        ...                         }
        ...                     ]
        ...                 }
        ...             ]
        ...         }
        ...     ]
        ... }
        >>> 
        >>> selection = activity_calendar(
        ...     data=rehab_data,
        ...     adapter="medical_rehab",
        ...     key="rehab_calendar"
        ... )
    """
    # Resolve adapter
    if isinstance(adapter, str):
        adapter_func: AdapterFunc = get_adapter(adapter)
    else:
        adapter_func = adapter
    
    # Normalize data
    events: List[CalendarEvent] = adapter_func(data)
    
    # Convert CalendarEvent objects to dicts for JSON serialization
    events_dicts = []
    for event in events:
        event_dict = {
            "id": event.id,
            "start": parse_date(event.start) or event.start,
            "title": event.title,
        }
        
        if event.end:
            event_dict["end"] = parse_date(event.end) or event.end
        if event.color:
            event_dict["color"] = event.color
        if event.category:
            event_dict["category"] = event.category
        if event.playerId:
            event_dict["playerId"] = event.playerId
        if event.playerName:
            event_dict["playerName"] = event.playerName
        if event.metadata:
            event_dict["metadata"] = sanitize_metadata(event.metadata)
        if event.raw:
            # Store raw for reconstruction
            try:
                event_dict["raw"] = event.raw
            except TypeError:
                # Can't serialize raw object, store reference info only
                pass
        
        events_dicts.append(event_dict)
    
    # Validate and merge theme
    validated_theme = validate_theme(theme or {})
    final_theme = merge_dictionaries(DEFAULT_THEME, validated_theme)
    
    # Build calendar config
    calendar_config: CalendarConfig = {
        "startHour": max(0, min(23, start_hour)),
        "endHour": max(0, min(23, end_hour)),
        "selectable": bool(selectable),
        "showTimeLabels": bool(show_time_labels),
        "compactMode": bool(compact_mode),
        "enableActivityPopover": bool(enable_activity_popover),
    }
    
    # Build component props
    component_props = {
        "events": events_dicts,
        "theme": final_theme,
        "config": calendar_config,
        "version": "1.0.0",
    }
    
    # Call the React component
    result = _activity_calendar(props=component_props, key=key)
    
    return result


def activity_calendar_async(
    data: Union[List[Dict[str, Any]], Dict[str, Any]],
    on_selection: Optional[Callable[[Dict[str, Any]], None]] = None,
    adapter: Union[str, AdapterFunc] = "identity",
    theme: Optional[ThemeConfig] = None,
    start_hour: int = 6,
    end_hour: int = 22,
    selectable: bool = True,
    key: str = "activity_calendar",
) -> None:
    """
    Render calendar with automatic selection handling.
    
    This is a convenience wrapper that handles selection events and
    calls a provided callback function.
    
    Args:
        data: Calendar data
        on_selection: Callback function called with selection payload
        adapter: Data adapter (name or function)
        theme: Theme configuration
        start_hour: Start hour (0-23)
        end_hour: End hour (0-23)
        selectable: Enable selection
        key: Component key
        
    Example:
        >>> def handle_selection(payload):
        ...     st.write(f"Selected: {payload}")
        >>> 
        >>> activity_calendar_async(
        ...     data=events,
        ...     on_selection=handle_selection,
        ...     key="calendar"
        ... )
    """
    selection = activity_calendar(
        data=data,
        adapter=adapter,
        theme=theme,
        start_hour=start_hour,
        end_hour=end_hour,
        selectable=selectable,
        key=key,
    )
    
    if selection and on_selection:
        on_selection(selection)
