"""
Themed calendar demo showing various theme configurations.

Shows:
- Different color schemes
- Theme customization
- Safe theming properties
- Responsive layout with themes
"""

import streamlit as st
from streamlit_activity_calendar import activity_calendar

# Page config
st.set_page_config(page_title="Themed Calendar", layout="wide")
st.title("🎨 Activity Calendar - Theme Showcase")

# Sample data
activities = [
    {
        "id": "1",
        "start": "2026-04-13",
        "title": "Morning Run",
        "color": "#FF6B6B",
        "category": "cardio",
    },
    {
        "id": "2",
        "start": "2026-04-13",
        "title": "Breakfast",
        "color": "#FFA500",
        "category": "nutrition",
    },
    {
        "id": "3",
        "start": "2026-04-13",
        "title": "Team Meeting",
        "color": "#4ECDC4",
        "category": "work",
    },
    {
        "id": "4",
        "start": "2026-04-14",
        "title": "Yoga Session",
        "color": "#95E1D3",
        "category": "wellness",
    },
    {
        "id": "5",
        "start": "2026-04-14",
        "title": "Code Review",
        "color": "#5F5FF0",
        "category": "work",
    },
    {
        "id": "6",
        "start": "2026-04-15",
        "title": "Lunch with Client",
        "color": "#FF6B9D",
        "category": "social",
    },
    {
        "id": "7",
        "start": "2026-04-15",
        "title": "Documentation",
        "color": "#C780FA",
        "category": "work",
    },
    {
        "id": "8",
        "start": "2026-04-16",
        "title": "Gym Session",
        "color": "#FF9671",
        "category": "fitness",
    },
    {
        "id": "9",
        "start": "2026-04-17",
        "title": "Project Planning",
        "color": "#02E1FF",
        "category": "work",
    },
]

# Theme presets
THEME_PRESETS = {
    "Light Mode": {
        "backgroundColor": "#ffffff",
        "gridColor": "#e0e0e0",
        "textColor": "#333333",
        "selectionColor": "#4CAF50",
        "borderRadius": 4,
    },
    "Dark Mode": {
        "backgroundColor": "#1e1e1e",
        "gridColor": "#404040",
        "textColor": "#e0e0e0",
        "selectionColor": "#66BB6A",
        "borderRadius": 4,
    },
    "Ocean": {
        "backgroundColor": "#e8f4f8",
        "gridColor": "#b3dce8",
        "textColor": "#003d66",
        "selectionColor": "#0099cc",
        "borderRadius": 8,
    },
    "Forest": {
        "backgroundColor": "#f0f4f1",
        "gridColor": "#c8d5ce",
        "textColor": "#1b3a1b",
        "selectionColor": "#2d5f2d",
        "borderRadius": 6,
    },
    "Sunset": {
        "backgroundColor": "#fef5e7",
        "gridColor": "#f8d8ae",
        "textColor": "#8b4513",
        "selectionColor": "#e67e22",
        "borderRadius": 8,
    },
    "Lavender": {
        "backgroundColor": "#f3e5f5",
        "gridColor": "#e1bee7",
        "textColor": "#4a148c",
        "selectionColor": "#7b1fa2",
        "borderRadius": 6,
    },
    "Minimalist": {
        "backgroundColor": "#fafafa",
        "gridColor": "#f0f0f0",
        "textColor": "#424242",
        "selectionColor": "#212121",
        "borderRadius": 2,
    },
    "Vibrant": {
        "backgroundColor": "#fffde7",
        "gridColor": "#fff59d",
        "textColor": "#f57f17",
        "selectionColor": "#ff6f00",
        "borderRadius": 10,
    },
}

# Sidebar theme selector
with st.sidebar:
    st.header("🎨 Theme Selection")
    
    theme_choice = st.selectbox(
        "Choose a preset theme:",
        list(THEME_PRESETS.keys()),
        index=0
    )
    
    st.divider()
    
    st.subheader("🎛️ Custom Theme")
    
    use_custom = st.checkbox("Use custom theme", False)
    
    if use_custom:
        col1, col2 = st.columns(2)
        
        with col1:
            bg_color = st.color_picker("Background", "#ffffff")
            grid_color = st.color_picker("Grid", "#e0e0e0")
        
        with col2:
            text_color = st.color_picker("Text", "#333333")
            selection_color = st.color_picker("Selection", "#4CAF50")
        
        border_radius = st.slider("Border Radius", 0, 20, 4)
        
        custom_theme = {
            "backgroundColor": bg_color,
            "gridColor": grid_color,
            "textColor": text_color,
            "selectionColor": selection_color,
            "borderRadius": border_radius,
        }
    else:
        custom_theme = THEME_PRESETS[theme_choice]
    
    st.divider()
    
    st.subheader("⚙️ Configuration")
    
    start_hour = st.slider("Start Hour", 0, 23, 7)
    end_hour = st.slider("End Hour", start_hour + 1, 24, 19)
    
    compact_mode = st.checkbox("Compact Mode", False)
    show_time_labels = st.checkbox("Show Time Labels", True)
    enable_popover = st.checkbox("Enable Popovers", True)

# Main content
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader(f"📅 Calendar - {theme_choice if not use_custom else 'Custom Theme'}")
    
    selection = activity_calendar(
        data=activities,
        adapter="flat_events",
        theme=custom_theme,
        start_hour=start_hour,
        end_hour=end_hour,
        selectable=True,
        compact_mode=compact_mode,
        show_time_labels=show_time_labels,
        enable_activity_popover=enable_popover,
        key="themed_calendar_main",
    )
    
    if selection:
        with st.container():
            st.success("✅ Selection received!")
            st.json(selection, expanded=False)

with col2:
    st.subheader("🎨 Theme Colors")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Preview:**")
        st.color_picker(
            "Background",
            value=custom_theme["backgroundColor"],
            disabled=True,
            key="preview_bg"
        )
        st.color_picker(
            "Grid",
            value=custom_theme["gridColor"],
            disabled=True,
            key="preview_grid"
        )
    
    with col2:
        st.write("**&nbsp;**")
        st.color_picker(
            "Text",
            value=custom_theme["textColor"],
            disabled=True,
            key="preview_text"
        )
        st.color_picker(
            "Selection",
            value=custom_theme["selectionColor"],
            disabled=True,
            key="preview_sel"
        )

st.divider()

# Theme comparison
st.subheader("📊 Theme Library")

cols = st.columns(4)
for idx, (theme_name, theme_colors) in enumerate(THEME_PRESETS.items()):
    with cols[idx % 4]:
        st.write(f"**{theme_name}**")
        
        col1, col2 = st.columns(2)
        with col1:
            st.color_picker(
                "BG",
                value=theme_colors["backgroundColor"],
                disabled=True,
                key=f"lib_bg_{theme_name}"
            )
            st.color_picker(
                "Grid",
                value=theme_colors["gridColor"],
                disabled=True,
                key=f"lib_grid_{theme_name}"
            )
        
        with col2:
            st.color_picker(
                "Text",
                value=theme_colors["textColor"],
                disabled=True,
                key=f"lib_text_{theme_name}"
            )
            st.color_picker(
                "Sel",
                value=theme_colors["selectionColor"],
                disabled=True,
                key=f"lib_sel_{theme_name}"
            )

st.divider()

# Activity summary
st.subheader("📋 Activities In View")

category_count = {}
for activity in activities:
    cat = activity.get("category", "other")
    category_count[cat] = category_count.get(cat, 0) + 1

col1, col2, col3, col4, col5 = st.columns(5)
cols = [col1, col2, col3, col4, col5]

for idx, (category, count) in enumerate(sorted(category_count.items())):
    with cols[idx % 5]:
        st.metric(category.title(), count)
