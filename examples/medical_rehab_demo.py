"""
Medical rehabilitation demo showing nested data adapter usage.

Shows:
- Nested rehab plan data structure
- Medical rehab adapter transformation
- Multiple players support
- Activity details and metadata
- Raw object inspection
"""

import streamlit as st
from streamlit_activity_calendar import activity_calendar
from datetime import datetime, timedelta

# Page config
st.set_page_config(page_title="Medical Rehab Calendar", layout="wide")
st.title("🏥 Physical Rehabilitation Schedule")

# Sample medical rehab data - nested structure
rehab_data = {
    "players": [
        {
            "id": "p001",
            "name": "John Smith",
            "medical_events": [
                {
                    "id": "med1",
                    "date": "2026-04-13",
                    "type": "appointment",
                    "title": "PT Session - Initial Assessment",
                    "notes": "Comprehensive evaluation and baseline testing"
                },
                {
                    "id": "med2",
                    "date": "2026-04-17",
                    "type": "follow_up",
                    "title": "Follow-up Assessment",
                    "notes": "Progress evaluation"
                }
            ],
            "rehab_plans": [
                {
                    "id": "plan1",
                    "name": "Post-ACL Surgery Rehabilitation",
                    "weeks": [
                        {
                            "week_number": 1,
                            "days": [
                                {
                                    "date": "2026-04-13",
                                    "activities": [
                                        {
                                            "id": "a1",
                                            "title": "Quad Sets",
                                            "category": "strengthening",
                                            "sets": 3,
                                            "reps": 10,
                                            "duration_minutes": 15,
                                            "notes": "Isometric quadriceps activation"
                                        },
                                        {
                                            "id": "a2",
                                            "title": "Straight Leg Raise",
                                            "category": "strengthening",
                                            "sets": 3,
                                            "reps": 10,
                                            "duration_minutes": 10,
                                            "notes": "Keep knee straight, hold 2 seconds"
                                        },
                                        {
                                            "id": "a3",
                                            "title": "Heel Walks",
                                            "category": "mobility",
                                            "sets": 2,
                                            "duration_minutes": 5,
                                            "notes": "Walk on heels across room"
                                        }
                                    ]
                                },
                                {
                                    "date": "2026-04-14",
                                    "activities": [
                                        {
                                            "id": "a4",
                                            "title": "Hamstring Stretching",
                                            "category": "stretching",
                                            "sets": 3,
                                            "duration_minutes": 20,
                                            "notes": "Hold each stretch 30 seconds"
                                        },
                                        {
                                            "id": "a5",
                                            "title": "Quad Stretching",
                                            "category": "stretching",
                                            "sets": 3,
                                            "duration_minutes": 15,
                                            "notes": "Hold each stretch 30 seconds"
                                        }
                                    ]
                                },
                                {
                                    "date": "2026-04-15",
                                    "activities": [
                                        {
                                            "id": "a6",
                                            "title": "Balance Board Work",
                                            "category": "balance",
                                            "sets": 3,
                                            "duration_minutes": 15,
                                            "notes": "Start with support, progress to no support"
                                        },
                                        {
                                            "id": "a7",
                                            "title": "Seated Knee Extension",
                                            "category": "strengthening",
                                            "sets": 3,
                                            "reps": 12,
                                            "duration_minutes": 10,
                                            "notes": "Light resistance band"
                                        }
                                    ]
                                },
                                {
                                    "date": "2026-04-16",
                                    "activities": [
                                        {
                                            "id": "a8",
                                            "title": "Heel Slides",
                                            "category": "flexibility",
                                            "sets": 3,
                                            "reps": 10,
                                            "duration_minutes": 10,
                                            "notes": "Slide heel toward buttock on flat surface"
                                        }
                                    ]
                                },
                                {
                                    "date": "2026-04-17",
                                    "activities": [
                                        {
                                            "id": "a9",
                                            "title": "Calf Raises",
                                            "category": "strengthening",
                                            "sets": 2,
                                            "reps": 15,
                                            "duration_minutes": 10,
                                            "notes": "Hold wall support as needed"
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ]
        },
        {
            "id": "p002",
            "name": "Sarah Johnson",
            "medical_events": [
                {
                    "id": "med3",
                    "date": "2026-04-14",
                    "type": "appointment",
                    "title": "Shoulder Rehab Session",
                    "notes": "Focus on rotator cuff"
                }
            ],
            "rehab_plans": [
                {
                    "id": "plan2",
                    "name": "Rotator Cuff Recovery",
                    "weeks": [
                        {
                            "week_number": 1,
                            "days": [
                                {
                                    "date": "2026-04-14",
                                    "activities": [
                                        {
                                            "id": "b1",
                                            "title": "Pendulum Exercises",
                                            "category": "mobility",
                                            "sets": 2,
                                            "duration_minutes": 15,
                                            "notes": "Gentle circular motion to reduce stiffness"
                                        },
                                        {
                                            "id": "b2",
                                            "title": "External Rotation",
                                            "category": "strengthening",
                                            "sets": 3,
                                            "reps": 10,
                                            "duration_minutes": 10,
                                            "notes": "Elbow at 90 degrees, light resistance"
                                        }
                                    ]
                                },
                                {
                                    "date": "2026-04-16",
                                    "activities": [
                                        {
                                            "id": "b3",
                                            "title": "Shoulder Blade Squeezes",
                                            "category": "strengthening",
                                            "sets": 3,
                                            "reps": 15,
                                            "duration_minutes": 10,
                                            "notes": "Scapular retraction and hold"
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

# Sidebar - Player selection
with st.sidebar:
    st.header("👥 Players")
    player_names = [p["name"] for p in rehab_data["players"]]
    selected_player_idx = st.selectbox("Select Player", range(len(player_names)), 
                                       format_func=lambda i: player_names[i])
    selected_player = rehab_data["players"][selected_player_idx]

st.subheader(f"📅 Schedule for {selected_player['name']}")

# Create filtered data for selected player
filtered_data = {
    "players": [selected_player]
}

# Render calendar with medical_rehab adapter
selection = activity_calendar(
    data=filtered_data,
    adapter="medical_rehab",
    theme={
        "backgroundColor": "#f8f9fa",
        "gridColor": "#dee2e6",
        "textColor": "#212529",
        "selectionColor": "#28a745",
        "accentColor": "#007bff",
    },
    start_hour=6,
    end_hour=20,
    selectable=True,
    key=f"rehab_calendar_{selected_player_idx}",
)

st.divider()

# Selection details
if selection and selection["event"] == "activity_selected":
    activity = selection["calendarEvent"]
    st.subheader(f"🎯 Activity Details: {activity['title']}")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Category", activity.get("category", "N/A"))
        st.metric("Date", activity.get("start", "N/A"))
    
    with col2:
        raw_data = activity.get("raw", {})
        if raw_data:
            if raw_data.get("sets"):
                st.metric("Sets", raw_data["sets"])
            if raw_data.get("reps"):
                st.metric("Reps", raw_data["reps"])
    
    with col3:
        if raw_data.get("duration_minutes"):
            st.metric("Duration", f"{raw_data['duration_minutes']} min")
    
    st.divider()
    
    # Detailed information
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Notes:**")
        st.write(raw_data.get("notes", "No notes"))
    
    with col2:
        st.write("**Player Information:**")
        st.write(f"Name: {activity.get('playerName', 'N/A')}")
        st.write(f"ID: {activity.get('playerId', 'N/A')}")

st.divider()

# Medical events
st.subheader("🏥 Medical Events")

medical_events = selected_player.get("medical_events", [])
if medical_events:
    for event in medical_events:
        with st.container():
            col1, col2, col3 = st.columns([1, 2, 2])
            
            with col1:
                st.write(f"📅 {event['date']}")
            
            with col2:
                st.write(f"**{event['title']}**")
                st.write(f"*{event['type']}*")
            
            with col3:
                st.write(f"📝 {event.get('notes', 'No notes')}")
        
        st.divider()
else:
    st.info("No medical events scheduled")

st.divider()

# Rehabilitation plan info
st.subheader("📋 Rehabilitation Plans")

for plan in selected_player.get("rehab_plans", []):
    with st.expander(f"📌 {plan['name']}"):
        total_activities = sum(
            len(day.get("activities", []))
            for week in plan.get("weeks", [])
            for day in week.get("days", [])
        )
        
        st.write(f"**Plan ID:** {plan['id']}")
        st.write(f"**Total Activities:** {total_activities}")
        
        for week in plan.get("weeks", []):
            st.write(f"**Week {week.get('week_number', '?')}**")
            
            for day in week.get("days", []):
                st.write(f"*{day['date']}*")
                
                activities = day.get("activities", [])
                if activities:
                    for activity in activities:
                        activity_str = f"- {activity['title']}"
                        if activity.get("sets"):
                            activity_str += f" ({activity['sets']}x"
                            if activity.get("reps"):
                                activity_str += f"{activity['reps']}"
                            activity_str += ")"
                        st.write(activity_str)
                else:
                    st.write("- Rest day")

st.divider()

# Statistics
st.subheader("📊 Progress Statistics")

total_activities = sum(
    len(day.get("activities", []))
    for plan in selected_player.get("rehab_plans", [])
    for week in plan.get("weeks", [])
    for day in week.get("days", [])
)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Activities", total_activities)

with col2:
    strengthening = sum(
        1 for plan in selected_player.get("rehab_plans", [])
        for week in plan.get("weeks", [])
        for day in week.get("days", [])
        for activity in day.get("activities", [])
        if activity.get("category") == "strengthening"
    )
    st.metric("Strengthening", strengthening)

with col3:
    stretching = sum(
        1 for plan in selected_player.get("rehab_plans", [])
        for week in plan.get("weeks", [])
        for day in week.get("days", [])
        for activity in day.get("activities", [])
        if activity.get("category") == "stretching"
    )
    st.metric("Stretching", stretching)

with col4:
    balance = sum(
        1 for plan in selected_player.get("rehab_plans", [])
        for week in plan.get("weeks", [])
        for day in week.get("days", [])
        for activity in day.get("activities", [])
        if activity.get("category") == "balance"
    )
    st.metric("Balance", balance)
