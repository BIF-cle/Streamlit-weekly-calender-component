"""
CRUD demonstration showing how to build a full activity management application.

Shows:
- Calendar rendering
- Selection handling
- Activity CRUD operations (Create, Read, Update, Delete)
- Streamlit session_state integration
- Form-based editing
- Persistent updates
"""

import streamlit as st
from streamlit_activity_calendar import activity_calendar
from datetime import datetime, timedelta
import uuid

# Page config
st.set_page_config(page_title="CRUD Activity Manager", layout="wide")
st.title("📋 Activity Management with Calendar")

# Initialize session state
if "activities" not in st.session_state:
    st.session_state.activities = [
        {
            "id": "act1",
            "start": "2026-04-13",
            "title": "Stand-up Meeting",
            "color": "#2196F3",
            "category": "meeting",
            "description": "Daily team sync",
        },
        {
            "id": "act2",
            "start": "2026-04-14",
            "title": "Code Review",
            "color": "#4CAF50",
            "category": "task",
            "description": "Review pull requests",
        },
        {
            "id": "act3",
            "start": "2026-04-15",
            "title": "Planning Session",
            "color": "#FF9800",
            "category": "meeting",
            "description": "Sprint planning",
        },
    ]

if "selected_activity_id" not in st.session_state:
    st.session_state.selected_activity_id = None

if "show_form" not in st.session_state:
    st.session_state.show_form = False

if "form_mode" not in st.session_state:
    st.session_state.form_mode = "create"  # "create" or "edit"


# Sidebar - CRUD controls
with st.sidebar:
    st.header("📌 Actions")
    
    if st.button("➕ Add New Activity", use_container_width=True):
        st.session_state.show_form = True
        st.session_state.form_mode = "create"
        st.session_state.selected_activity_id = None
        st.rerun()
    
    st.divider()
    st.subheader("📊 Statistics")
    st.metric("Total Activities", len(st.session_state.activities))
    
    # Activities by category
    categories = {}
    for activity in st.session_state.activities:
        cat = activity.get("category", "other")
        categories[cat] = categories.get(cat, 0) + 1
    
    for cat, count in sorted(categories.items()):
        st.metric(f"  {cat.title()}", count)


# Main content - Calendar
col1, col2 = st.columns([3, 1])

with col1:
    st.subheader("📅 Calendar View")
    
    # Render calendar
    selection = activity_calendar(
        data=st.session_state.activities,
        adapter="flat_events",
        start_hour=8,
        end_hour=18,
        selectable=True,
        key="crud_calendar",
    )
    
    # Handle selection
    if selection and selection["event"] == "activity_selected":
        st.session_state.selected_activity_id = selection["calendarEvent"]["id"]
        st.rerun()

with col2:
    st.subheader("ℹ️ Details")
    
    if st.session_state.selected_activity_id:
        activity = next(
            (a for a in st.session_state.activities 
             if a["id"] == st.session_state.selected_activity_id),
            None
        )
        
        if activity:
            st.write(f"**{activity['title']}**")
            st.write(f"📅 {activity['start']}")
            st.write(f"🏷️ {activity.get('category', 'N/A')}")
            st.write(f"📝 {activity.get('description', 'No description')}")
            
            st.divider()
            
            col_edit, col_del = st.columns(2)
            with col_edit:
                if st.button("✏️ Edit", use_container_width=True):
                    st.session_state.show_form = True
                    st.session_state.form_mode = "edit"
                    st.rerun()
            
            with col_del:
                if st.button("🗑️ Delete", use_container_width=True):
                    st.session_state.activities = [
                        a for a in st.session_state.activities
                        if a["id"] != st.session_state.selected_activity_id
                    ]
                    st.session_state.selected_activity_id = None
                    st.session_state.show_form = False
                    st.rerun()

st.divider()

# Form section
if st.session_state.show_form:
    st.subheader(
        f"{'✏️ Edit Activity' if st.session_state.form_mode == 'edit' else '➕ New Activity'}"
    )
    
    # Get current values if editing
    current_activity = None
    if st.session_state.form_mode == "edit" and st.session_state.selected_activity_id:
        current_activity = next(
            (a for a in st.session_state.activities 
             if a["id"] == st.session_state.selected_activity_id),
            None
        )
    
    # Form fields
    col1, col2 = st.columns(2)
    
    with col1:
        title = st.text_input(
            "Title*",
            value=current_activity.get("title", "") if current_activity else "",
            key="form_title"
        )
    
    with col2:
        date_val = st.date_input(
            "Date*",
            value=datetime.fromisoformat(current_activity.get("start", "2026-04-13")).date()
            if current_activity
            else datetime.now().date(),
            key="form_date"
        )
    
    col1, col2 = st.columns(2)
    
    with col1:
        category = st.selectbox(
            "Category*",
            ["meeting", "task", "break", "personal", "other"],
            index=["meeting", "task", "break", "personal", "other"].index(
                current_activity.get("category", "meeting") if current_activity else "meeting"
            ),
            key="form_category"
        )
    
    with col2:
        color = st.color_picker(
            "Color*",
            value=current_activity.get("color", "#2196F3") if current_activity else "#2196F3",
            key="form_color"
        )
    
    description = st.text_area(
        "Description",
        value=current_activity.get("description", "") if current_activity else "",
        key="form_description"
    )
    
    # Form actions
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button(
            "💾 Save",
            use_container_width=True,
            type="primary"
        ):
            if not title:
                st.error("Title is required")
            else:
                if st.session_state.form_mode == "create":
                    # Create new
                    new_activity = {
                        "id": str(uuid.uuid4())[:8],
                        "start": date_val.isoformat(),
                        "title": title,
                        "category": category,
                        "color": color,
                        "description": description,
                    }
                    st.session_state.activities.append(new_activity)
                else:
                    # Update existing
                    for activity in st.session_state.activities:
                        if activity["id"] == st.session_state.selected_activity_id:
                            activity["title"] = title
                            activity["start"] = date_val.isoformat()
                            activity["category"] = category
                            activity["color"] = color
                            activity["description"] = description
                            break
                
                st.session_state.show_form = False
                st.session_state.selected_activity_id = None
                st.success("✅ Activity saved!")
                st.rerun()
    
    with col2:
        if st.button("❌ Cancel", use_container_width=True):
            st.session_state.show_form = False
            st.rerun()

# Activities table
st.divider()
st.subheader("📋 All Activities")

if st.session_state.activities:
    # Sort by date
    sorted_activities = sorted(st.session_state.activities, key=lambda x: x["start"])
    
    for idx, activity in enumerate(sorted_activities):
        with st.container():
            col1, col2, col3, col4, col5 = st.columns([2, 2, 2, 1, 1])
            
            with col1:
                st.write(f"**{activity['title']}**")
            
            with col2:
                st.write(activity["start"])
            
            with col3:
                st.write(activity.get("category", "N/A"))
            
            with col4:
                if st.button("✏️", key=f"edit_{idx}", help="Edit"):
                    st.session_state.selected_activity_id = activity["id"]
                    st.session_state.show_form = True
                    st.session_state.form_mode = "edit"
                    st.rerun()
            
            with col5:
                if st.button("🗑️", key=f"delete_{idx}", help="Delete"):
                    st.session_state.activities = [
                        a for a in st.session_state.activities
                        if a["id"] != activity["id"]
                    ]
                    st.rerun()
        
        st.divider()
else:
    st.info("No activities yet. Click 'Add New Activity' to get started!")
