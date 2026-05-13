"""
Data adapter system for normalizing nested domain data into calendar events.

This module provides adapters that transform domain-specific nested structures
into the canonical CalendarEvent[] format expected by the React frontend.

The adapter pattern allows the component to remain generic while supporting
arbitrary nested domain models (medical rehab data, project planning, etc.).
"""

from typing import Any, Callable, Dict, List, Optional
from datetime import datetime, timedelta
import uuid
from .types import CalendarEvent


AdapterFunc = Callable[[Any], List[CalendarEvent]]


def identity_adapter(data: Any) -> List[CalendarEvent]:
    """
    Identity adapter - assumes data is already in CalendarEvent[] format.
    
    Use this when your data is already properly structured as a list of
    events with id, start, title, etc.
    
    Args:
        data: List of event dictionaries or CalendarEvent objects
        
    Returns:
        List of CalendarEvent objects
    """
    if isinstance(data, list):
        events = []
        for item in data:
            if isinstance(item, dict):
                event = CalendarEvent(**item)
                events.append(event)
            elif isinstance(item, CalendarEvent):
                events.append(item)
        return events
    return []


def flat_events_adapter(data: List[Dict[str, Any]]) -> List[CalendarEvent]:
    """
    Adapter for flat event lists with standard fields.
    
    Expects events to have: id, start, title, and optional: end, color, category, etc.
    
    Args:
        data: List of event dictionaries
        
    Returns:
        List of CalendarEvent objects
    """
    events = []
    for item in data:
        if not isinstance(item, dict):
            continue
            
        event = CalendarEvent(
            id=str(item.get("id", str(uuid.uuid4()))),
            start=str(item.get("start", "")),
            title=str(item.get("title", "Untitled")),
            end=str(item.get("end")) if item.get("end") else None,
            color=str(item.get("color")) if item.get("color") else None,
            category=str(item.get("category")) if item.get("category") else None,
            playerId=str(item.get("playerId")) if item.get("playerId") else None,
            playerName=str(item.get("playerName")) if item.get("playerName") else None,
            metadata=item.get("metadata", {}),
            raw=item,
        )
        events.append(event)
    
    return events


def medical_rehab_adapter(data: Dict[str, Any]) -> List[CalendarEvent]:
    """
    Adapter for nested medical rehabilitation plan data.
    
    Transforms hierarchical rehab data into flat calendar events:
    
    {
        "players": [
            {
                "id": "player1",
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
                                                "id": "act1",
                                                "title": "Quad Sets",
                                                "category": "strengthening",
                                                "duration_minutes": 15,
                                                "sets": 3,
                                                "reps": 10,
                                                "notes": "..."
                                            }
                                        ]
                                    }
                                ]
                            }
                        ]
                    }
                ],
                "medical_events": [
                    {
                        "date": "2026-04-13",
                        "type": "appointment",
                        "title": "Physical Therapy Session",
                        "notes": "..."
                    }
                ]
            }
        ]
    }
    
    Args:
        data: Nested rehab plan structure
        
    Returns:
        Flattened list of CalendarEvent objects
    """
    events = []
    
    if not isinstance(data, dict):
        return events
    
    players = data.get("players", [])
    if not isinstance(players, list):
        return events
    
    for player in players:
        if not isinstance(player, dict):
            continue
        
        player_id = str(player.get("id", "unknown"))
        player_name = str(player.get("name", "Unknown"))
        
        # Process rehab plans
        rehab_plans = player.get("rehab_plans", [])
        if isinstance(rehab_plans, list):
            for plan in rehab_plans:
                if not isinstance(plan, dict):
                    continue
                
                weeks = plan.get("weeks", [])
                if isinstance(weeks, list):
                    for week in weeks:
                        if not isinstance(week, dict):
                            continue
                        
                        days = week.get("days", [])
                        if isinstance(days, list):
                            for day in days:
                                if not isinstance(day, dict):
                                    continue
                                
                                day_date = str(day.get("date", ""))
                                activities = day.get("activities", [])
                                
                                if isinstance(activities, list):
                                    for activity in activities:
                                        if not isinstance(activity, dict):
                                            continue
                                        
                                        event = CalendarEvent(
                                            id=str(activity.get("id", str(uuid.uuid4()))),
                                            start=day_date,
                                            title=str(activity.get("title", "Activity")),
                                            category=str(activity.get("category", "general")),
                                            color=category_to_color(
                                                activity.get("category", "general")
                                            ),
                                            playerId=player_id,
                                            playerName=player_name,
                                            metadata={
                                                "sets": activity.get("sets"),
                                                "reps": activity.get("reps"),
                                                "duration_minutes": activity.get("duration_minutes"),
                                                "notes": activity.get("notes"),
                                            },
                                            raw=activity,
                                        )
                                        events.append(event)
        
        # Process medical events
        medical_events = player.get("medical_events", [])
        if isinstance(medical_events, list):
            for med_event in medical_events:
                if not isinstance(med_event, dict):
                    continue
                
                event = CalendarEvent(
                    id=str(med_event.get("id", str(uuid.uuid4()))),
                    start=str(med_event.get("date", "")),
                    title=str(med_event.get("title", "Medical Event")),
                    category="medical",
                    color="#FF6B6B",  # Red for medical
                    playerId=player_id,
                    playerName=player_name,
                    metadata={
                        "type": med_event.get("type"),
                        "notes": med_event.get("notes"),
                    },
                    raw=med_event,
                )
                events.append(event)
    
    return events


def project_timeline_adapter(data: Dict[str, Any]) -> List[CalendarEvent]:
    """
    Adapter for project management timeline data.
    
    Transforms project/task hierarchy into calendar events:
    
    {
        "projects": [
            {
                "id": "proj1",
                "name": "Website Redesign",
                "tasks": [
                    {
                        "id": "task1",
                        "title": "Design mockups",
                        "start_date": "2026-04-13",
                        "end_date": "2026-04-15",
                        "status": "in_progress",
                        "assignee": "Jane"
                    }
                ]
            }
        ]
    }
    
    Args:
        data: Nested project/task structure
        
    Returns:
        Flattened list of CalendarEvent objects
    """
    events = []
    
    if not isinstance(data, dict):
        return events
    
    projects = data.get("projects", [])
    if not isinstance(projects, list):
        return events
    
    status_colors = {
        "pending": "#FFC107",
        "in_progress": "#2196F3",
        "completed": "#4CAF50",
        "on_hold": "#9C27B0",
    }
    
    for project in projects:
        if not isinstance(project, dict):
            continue
        
        project_id = str(project.get("id", "unknown"))
        project_name = str(project.get("name", "Project"))
        
        tasks = project.get("tasks", [])
        if isinstance(tasks, list):
            for task in tasks:
                if not isinstance(task, dict):
                    continue
                
                status = task.get("status", "pending")
                color = status_colors.get(status, "#999999")
                
                event = CalendarEvent(
                    id=str(task.get("id", str(uuid.uuid4()))),
                    start=str(task.get("start_date", "")),
                    end=str(task.get("end_date")) if task.get("end_date") else None,
                    title=str(task.get("title", "Task")),
                    category=status,
                    color=color,
                    playerId=project_id,
                    playerName=project_name,
                    metadata={
                        "assignee": task.get("assignee"),
                        "status": status,
                        "priority": task.get("priority"),
                        "description": task.get("description"),
                    },
                    raw=task,
                )
                events.append(event)
    
    return events


def category_to_color(category: str) -> str:
    """
    Map activity category to a safe hex color.
    
    Uses a predefined color palette for different activity types.
    
    Args:
        category: Activity category name
        
    Returns:
        Hex color code
    """
    color_map = {
        "strengthening": "#4CAF50",  # Green
        "flexibility": "#2196F3",  # Blue
        "balance": "#FF9800",  # Orange
        "cardio": "#E91E63",  # Pink
        "neurological": "#9C27B0",  # Purple
        "stretching": "#00BCD4",  # Cyan
        "mobility": "#8BC34A",  # Light Green
        "functional": "#FFEB3B",  # Yellow
        "general": "#9E9E9E",  # Gray
        "medical": "#FF5252",  # Red
    }
    return color_map.get(str(category).lower(), "#999999")


# Registry of available adapters
ADAPTERS: Dict[str, AdapterFunc] = {
    "identity": identity_adapter,
    "flat_events": flat_events_adapter,
    "medical_rehab": medical_rehab_adapter,
    "project_timeline": project_timeline_adapter,
}


def get_adapter(adapter_name: str) -> AdapterFunc:
    """
    Get an adapter by name from the registry.
    
    Args:
        adapter_name: Name of the adapter
        
    Returns:
        Adapter function
        
    Raises:
        ValueError: If adapter not found
    """
    if adapter_name not in ADAPTERS:
        raise ValueError(
            f"Unknown adapter: {adapter_name}. "
            f"Available adapters: {', '.join(ADAPTERS.keys())}"
        )
    return ADAPTERS[adapter_name]


def register_adapter(name: str, adapter: AdapterFunc) -> None:
    """
    Register a custom adapter.
    
    Args:
        name: Name for the adapter
        adapter: Adapter function
    """
    ADAPTERS[name] = adapter
