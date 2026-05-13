"""
Streamlit Activity Calendar - Production-Quality Reusable Component

A Streamlit custom component library providing a React-powered weekly activity
calendar with flexible data adapters, theming, and selection handling.

This library enables rapid development of calendar-based applications by:
- Normalizing arbitrary nested domain data via the adapter system
- Providing a reusable, stateless React component
- Handling all application state in Streamlit
- Supporting rich metadata and CRUD workflows

Architecture:
The component follows a strict separation of concerns:
- React frontend: renders calendar and handles UI interactions
- Streamlit wrapper: manages component lifecycle and data flows
- Adapter system: normalizes domain data to calendar events
- Application layer (your Streamlit app): handles CRUD and business logic

The component remains completely generic and reusable:
- Does not store application state
- Does not mutate backend data
- Does not understand domain-specific schemas
- Emits interaction events for external handling

Installation:
    pip install streamlit-activity-calendar

Quick Start:
    import streamlit as st
    from streamlit_activity_calendar import activity_calendar
    
    events = [
        {
            "id": "1",
            "start": "2026-04-13",
            "title": "Team Meeting",
            "color": "#4CAF50"
        }
    ]
    
    selection = activity_calendar(
        data=events,
        adapter="flat_events",
        key="my_calendar"
    )
    
    if selection:
        st.write(f"Selected: {selection}")

Advanced Usage - Medical Rehab Data:
    from streamlit_activity_calendar import activity_calendar
    
    rehab_data = {
        "players": [
            {
                "id": "p1",
                "name": "John Doe",
                "rehab_plans": [
                    {
                        "weeks": [
                            {
                                "days": [
                                    {
                                        "date": "2026-04-13",
                                        "activities": [
                                            {
                                                "id": "a1",
                                                "title": "Quad Sets",
                                                "category": "strengthening"
                                            }
                                        ]
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }
        ]
    }
    
    selection = activity_calendar(
        data=rehab_data,
        adapter="medical_rehab",
        key="rehab_calendar"
    )

Custom Adapters:
    from streamlit_activity_calendar import activity_calendar, CalendarEvent
    
    def my_adapter(data):
        # Transform your domain data into CalendarEvent[]
        events = []
        for item in data:
            event = CalendarEvent(
                id=str(item["id"]),
                start=item["date"],
                title=item["task"]
            )
            events.append(event)
        return events
    
    selection = activity_calendar(
        data=my_data,
        adapter=my_adapter,
        key="calendar"
    )

Attributes:
    __version__: Package version
    __author__: Package author
"""

__version__ = "1.0.0"
__author__ = "Your Company"

from .component import (
    activity_calendar,
    activity_calendar_async,
)

from .types import (
    CalendarEvent,
    CalendarEventDict,
    CellSelectionPayload,
    ActivitySelectionPayload,
    ThemeConfig,
    CalendarConfig,
    DEFAULT_THEME,
    DEFAULT_CALENDAR_CONFIG,
)

from .adapters import (
    identity_adapter,
    flat_events_adapter,
    medical_rehab_adapter,
    project_timeline_adapter,
    get_adapter,
    register_adapter,
    ADAPTERS,
)

from .utils import (
    parse_date,
    normalize_color,
    validate_theme,
    get_week_range,
    get_time_labels,
)

__all__ = [
    # Main component API
    "activity_calendar",
    "activity_calendar_async",
    # Type definitions
    "CalendarEvent",
    "CalendarEventDict",
    "CellSelectionPayload",
    "ActivitySelectionPayload",
    "ThemeConfig",
    "CalendarConfig",
    "DEFAULT_THEME",
    "DEFAULT_CALENDAR_CONFIG",
    # Adapters
    "identity_adapter",
    "flat_events_adapter",
    "medical_rehab_adapter",
    "project_timeline_adapter",
    "get_adapter",
    "register_adapter",
    "ADAPTERS",
    # Utilities
    "parse_date",
    "normalize_color",
    "validate_theme",
    "get_week_range",
    "get_time_labels",
]
