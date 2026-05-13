"""
Utility functions for the activity calendar component.
"""

from typing import Any, Dict, List, Optional, Union
from datetime import datetime, timedelta
import json


def parse_date(date_value: Any) -> Optional[str]:
    """
    Parse a date value into ISO format string.
    
    Handles various input formats: datetime objects, date objects, strings.
    
    Args:
        date_value: Date in various formats
        
    Returns:
        ISO format date string or None if invalid
    """
    if date_value is None:
        return None
    
    if isinstance(date_value, str):
        # Try to parse ISO format
        try:
            datetime.fromisoformat(date_value.replace('Z', '+00:00'))
            return date_value.split('T')[0] if 'T' in date_value else date_value
        except (ValueError, AttributeError):
            return None
    
    if isinstance(date_value, datetime):
        return date_value.date().isoformat()
    
    if hasattr(date_value, 'isoformat'):  # date-like objects
        return date_value.isoformat()
    
    return None


def get_week_range(target_date: str) -> tuple[str, str]:
    """
    Get the Monday-Sunday range for a given date.
    
    Args:
        target_date: ISO format date string
        
    Returns:
        Tuple of (monday_date, sunday_date) as ISO strings
    """
    try:
        date = datetime.fromisoformat(target_date)
    except (ValueError, TypeError):
        # Default to today
        date = datetime.now()
    
    # Find Monday (weekday 0 is Monday)
    days_since_monday = date.weekday()
    monday = date - timedelta(days=days_since_monday)
    sunday = monday + timedelta(days=6)
    
    return (monday.date().isoformat(), sunday.date().isoformat())


def get_time_labels(start_hour: int, end_hour: int) -> List[str]:
    """
    Generate time labels for calendar display.
    
    Args:
        start_hour: Start hour (0-23)
        end_hour: End hour (0-23)
        
    Returns:
        List of formatted time strings
    """
    labels = []
    for hour in range(start_hour, end_hour + 1):
        labels.append(f"{hour:02d}:00")
    return labels


def normalize_color(color: Any) -> str:
    """
    Normalize a color value to hex format.
    
    Args:
        color: Color value (hex, rgb, rgba, or color name)
        
    Returns:
        Hex color code
    """
    if not color:
        return "#999999"
    
    color_str = str(color).strip().lower()
    
    # Already hex
    if color_str.startswith('#') and len(color_str) in (4, 7, 9):
        return color_str
    
    # RGB/RGBA
    if color_str.startswith('rgb'):
        return color_str
    
    # Named colors
    named_colors = {
        "red": "#FF0000",
        "green": "#00FF00",
        "blue": "#0000FF",
        "yellow": "#FFFF00",
        "purple": "#800080",
        "cyan": "#00FFFF",
        "magenta": "#FF00FF",
        "white": "#FFFFFF",
        "black": "#000000",
        "gray": "#808080",
        "grey": "#808080",
    }
    
    return named_colors.get(color_str, "#999999")


def validate_theme(theme: Any) -> Dict[str, Any]:
    """
    Validate and sanitize theme configuration.
    
    Ensures only safe theme properties can be customized.
    
    Args:
        theme: Theme configuration dictionary
        
    Returns:
        Validated theme dictionary
    """
    if not isinstance(theme, dict):
        return {}
    
    allowed_keys = {
        "backgroundColor",
        "gridColor",
        "textColor",
        "borderRadius",
        "selectionColor",
        "foregroundColor",
        "accentColor",
    }
    
    validated = {}
    
    for key, value in theme.items():
        if key not in allowed_keys:
            continue
        
        if key == "borderRadius":
            try:
                validated[key] = max(0, int(value))
            except (ValueError, TypeError):
                continue
        else:
            # Color properties
            color = normalize_color(value)
            validated[key] = color
    
    return validated


def create_storage_key(base_key: str, component_id: str) -> str:
    """
    Create a unique storage key for component state.
    
    Args:
        base_key: Base key name
        component_id: Component ID/key
        
    Returns:
        Unique storage key
    """
    return f"activity_calendar_{base_key}_{component_id}"


def merge_dictionaries(*dicts: Dict[str, Any]) -> Dict[str, Any]:
    """
    Deep merge multiple dictionaries.
    
    Later dictionaries override earlier ones.
    
    Args:
        *dicts: Variable number of dictionaries
        
    Returns:
        Merged dictionary
    """
    result = {}
    
    for d in dicts:
        if isinstance(d, dict):
            for key, value in d.items():
                if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                    result[key] = merge_dictionaries(result[key], value)
                else:
                    result[key] = value
    
    return result


def flatten_nested_list(nested_list: List[Any]) -> List[Any]:
    """
    Flatten a nested list structure.
    
    Args:
        nested_list: Potentially nested list
        
    Returns:
        Flattened list
    """
    result = []
    
    for item in nested_list:
        if isinstance(item, list):
            result.extend(flatten_nested_list(item))
        else:
            result.append(item)
    
    return result


def sanitize_metadata(metadata: Any, max_depth: int = 3, current_depth: int = 0) -> Any:
    """
    Sanitize metadata for safe JSON serialization.
    
    Prevents deeply nested structures and circular references.
    
    Args:
        metadata: Metadata to sanitize
        max_depth: Maximum nesting depth
        current_depth: Current recursion depth
        
    Returns:
        Sanitized metadata
    """
    if current_depth > max_depth:
        return None
    
    if metadata is None:
        return None
    
    if isinstance(metadata, (str, int, float, bool)):
        return metadata
    
    if isinstance(metadata, dict):
        result = {}
        for k, v in metadata.items():
            if isinstance(k, str):
                result[k] = sanitize_metadata(v, max_depth, current_depth + 1)
        return result
    
    if isinstance(metadata, list):
        return [sanitize_metadata(item, max_depth, current_depth + 1) for item in metadata]
    
    # Skip other types
    return None
