"""
Basic example demonstrating the activity calendar component.

Shows:
- Simple event list
- Basic calendar rendering
- Selection handling
- Simple event display
"""

import streamlit as st
from streamlit_activity_calendar import activity_calendar

# Page config
st.set_page_config(page_title="Basic Calendar", layout="wide")
st.title("🗓️ Basic Activity Calendar")

# Sample events data
sample_events = [
    {
        "id": "1",
        "start": "2026-04-13",
        "title": "Team Meeting",
        "color": "#2196F3",
        "category": "general",
    },
    {
        "id": "2",
        "start": "2026-04-13",
        "title": "Lunch Break",
        "color": "#FF9800",
        "category": "break",
    },
    {
        "id": "3",
        "start": "2026-04-14",
        "title": "Project Review",
        "color": "#4CAF50",
        "category": "work",
    },
    {
        "id": "4",
        "start": "2026-04-15",
        "title": "Client Call",
        "color": "#9C27B0",
        "category": "meeting",
    },
    {
        "id": "5",
        "start": "2026-04-16",
        "title": "Documentation",
        "color": "#F44336",
        "category": "task",
    },
]

# Display events
st.subheader("📋 Event List")
for event in sample_events:
    with st.container():
        col1, col2, col3 = st.columns([2, 2, 1])
        with col1:
            st.text(event["title"])
        with col2:
            st.text(event["start"])
        with col3:
            st.text(event["category"])

st.divider()

# Calendar component
st.subheader("📅 Calendar")

selection = activity_calendar(
    data=sample_events,
    adapter="flat_events",
    start_hour=8,
    end_hour=18,
    selectable=True,
    key="basic_calendar",
)

# Handle selection
if selection:
    st.subheader("✅ Selection")
    
    if selection["event"] == "cell_selected":
        st.success(f"Cell selected: {selection['cell']['date']}")
    
    elif selection["event"] == "activity_selected":
        event = selection["calendarEvent"]
        st.success(f"Activity selected: {event['title']}")
        
        # Display activity details
        col1, col2 = st.columns(2)
        with col1:
            st.write("**Event Details:**")
            st.write(f"ID: {event['id']}")
            st.write(f"Title: {event['title']}")
            st.write(f"Date: {event['start']}")
        
        with col2:
            st.write("**Category:**")
            st.write(f"{event.get('category', 'N/A')}")
            
            st.write("**Color:**")
            if event.get('color'):
                st.color_picker("", value=event['color'], disabled=True)

st.divider()

# Configuration demo
st.subheader("⚙️ Configuration")

col1, col2, col3 = st.columns(3)
with col1:
    start_hour = st.slider("Start Hour", 0, 23, 8, key="start_hour_demo")
with col2:
    end_hour = st.slider("End Hour", start_hour + 1, 24, 18, key="end_hour_demo")
with col3:
    compact_mode = st.checkbox("Compact Mode", False)

st.divider()

# Advanced configuration
st.subheader("🎨 Theme Configuration")

theme_col1, theme_col2, theme_col3 = st.columns(3)

with theme_col1:
    bg_color = st.color_picker("Background Color", "#ffffff")
    grid_color = st.color_picker("Grid Color", "#e0e0e0")

with theme_col2:
    text_color = st.color_picker("Text Color", "#333333")
    selection_color = st.color_picker("Selection Color", "#4CAF50")

with theme_col3:
    border_radius = st.slider("Border Radius", 0, 20, 4)

custom_theme = {
    "backgroundColor": bg_color,
    "gridColor": grid_color,
    "textColor": text_color,
    "selectionColor": selection_color,
    "borderRadius": border_radius,
}

# Display calendar with custom theme
st.subheader("📅 Calendar with Custom Theme")

selection2 = activity_calendar(
    data=sample_events,
    adapter="flat_events",
    theme=custom_theme,
    start_hour=start_hour,
    end_hour=end_hour,
    compact_mode=compact_mode,
    key="themed_calendar",
)
