# 📅 Streamlit Activity Calendar

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/streamlit-1.20+-red.svg)](https://streamlit.io)
[![React](https://img.shields.io/badge/react-18+-blue.svg)](https://react.dev)
[![TypeScript](https://img.shields.io/badge/typescript-5+-blue.svg)](https://www.typescriptlang.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

A **production-quality Streamlit custom component** for interactive weekly activity calendars with a React frontend. Designed for flexibility, reusability, and seamless data adapter integration.

## 🎯 Features


- **Weekly Calendar View** - Clean, CSS Grid-based weekly calendar rendering
- **Flexible Data Adapters** - Transform nested domain data into calendar events
- **Activity Selection** - Cell and activity-level selection with event emission
- **Safe Theming** - Customizable theme with predefined CSS properties
- **Rich Metadata** - Support for arbitrary activity metadata
- **Type Safe** - Full TypeScript support, comprehensive Python types
- **Reusable Component** - Stateless by design, no backend coupling
- **CRUD Support** - Integrate seamlessly with Streamlit session_state
- **Responsive Design** - Adapts to different screen sizes
- **Production Ready** - Battle-tested patterns, comprehensive testing

## 📦 Installation

```bash
pip install streamlit-activity-calendar
```

### Development Installation

```bash
# Clone repository
git clone https://github.com/yourusername/streamlit-activity-calendar.git
cd streamlit-activity-calendar

# Install Python package in development mode
pip install -e .

# Install Python dev dependencies
pip install -e ".[dev]"

# Then build frontend
cd frontend
npm install
npm run build
cd ..
```

## 🚀 Quick Start

### Basic Example

```python
import streamlit as st
from streamlit_activity_calendar import activity_calendar

st.title("My Calendar")

events = [
    {
        "id": "1",
        "start": "2026-04-13",
        "title": "Team Meeting",
        "color": "#2196F3",
        "category": "work"
    },
    {
        "id": "2",
        "start": "2026-04-14",
        "title": "Project Review",
        "color": "#4CAF50",
        "category": "work"
    }
]

selection = activity_calendar(
    data=events,
    adapter="flat_events",
    start_hour=8,
    end_hour=18,
    key="my_calendar"
)

if selection:
    st.write(f"Selected: {selection}")
```

### CRUD Application

```python
import streamlit as st
from streamlit_activity_calendar import activity_calendar

# Initialize session state
if "activities" not in st.session_state:
    st.session_state.activities = []

# Render calendar
selection = activity_calendar(
    data=st.session_state.activities,
    adapter="flat_events",
    selectable=True,
    key="crud_calendar"
)

# Handle selection
if selection:
    if selection["event"] == "activity_selected":
        activity_id = selection["calendarEvent"]["id"]
        # Show edit form, delete button, etc.
```

### Medical Rehab Data

```python
from streamlit_activity_calendar import activity_calendar

# Nested rehab data
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
                                            "category": "strengthening",
                                            "sets": 3,
                                            "reps": 10
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

# Adapter automatically flattens nested structure
selection = activity_calendar(
    data=rehab_data,
    adapter="medical_rehab",
    key="rehab_calendar"
)
```

## 🏗️ Architecture

The component follows strict separation of concerns:

```
┌─────────────────────────────────────────────────┐
│         Streamlit Python Application            │
│  - CRUD logic                                   │
│  - Session state management                    │
│  - Business logic                              │
└────────────────┬────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────────┐
│   Python Wrapper (component.py)                 │
│  - Accepts raw domain data                     │
│  - Selects and applies adapter                 │
│  - Validates configuration                     │
│  - Sends normalized data to React              │
└────────────────┬────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────────┐
│   Data Adapter Layer (adapters.py)              │
│  - medical_rehab_adapter                        │
│  - project_timeline_adapter                     │
│  - flat_events_adapter                          │
│  - Custom adapters                              │
└────────────────┬────────────────────────────────┘
                 │
        ┌────────▼────────┐
        │ CalendarEvent[] │
        │ (Normalized)    │
        └────────┬────────┘
                 │
┌────────────────▼────────────────────────────────┐
│      React Component (Calendar.tsx)             │
│  - Renders weekly grid                         │
│  - Handles interactions                        │
│  - Emits selection events                      │
└────────────────┬────────────────────────────────┘
                 │
        ┌────────▼──────────┐
        │ Selection Payload │
        │ (JSON)            │
        └────────┬──────────┘
                 │
┌────────────────▼─────────────────────────────┐
│  Streamlit Component (Python callback)       │
└──────────────────────────────────────────────┘
```

## 📊 Data Adapters

The adapter system normalizes arbitrary nested data structures into `CalendarEvent[]`.

### Available Adapters

#### 1. **identity_adapter** (default)
Assumes input data is already flat `CalendarEvent[]` format.

```python
events = [{"id": "1", "start": "2026-04-13", "title": "Event"}]
activity_calendar(data=events, adapter="identity")
```

#### 2. **flat_events_adapter**
Transforms flat event lists with standard fields.

```python
events = [
    {
        "id": "1",
        "start": "2026-04-13",
        "title": "Meeting",
        "color": "#2196F3",
        "category": "work",
        "metadata": {"location": "Room 101"}
    }
]
activity_calendar(data=events, adapter="flat_events")
```

#### 3. **medical_rehab_adapter**
Handles nested medical rehabilitation data structures.

```python
rehab_data = {
    "players": [{
        "rehab_plans": [{
            "weeks": [{
                "days": [{
                    "date": "2026-04-13",
                    "activities": [{"id": "a1", "title": "Quad Sets", ...}]
                }]
            }]
        }]
    }]
}
activity_calendar(data=rehab_data, adapter="medical_rehab")
```

#### 4. **project_timeline_adapter**
Transforms project management data.

```python
projects = {
    "projects": [{
        "tasks": [{
            "title": "Design",
            "start_date": "2026-04-13",
            "status": "in_progress"
        }]
    }]
}
activity_calendar(data=projects, adapter="project_timeline")
```

### Custom Adapter

```python
from streamlit_activity_calendar import CalendarEvent, activity_calendar

def my_adapter(data):
    """Transform your domain data into CalendarEvent[]"""
    events = []
    for item in data:
        event = CalendarEvent(
            id=str(item["id"]),
            start=item["date"],
            title=item["task"]
        )
        events.append(event)
    return events

activity_calendar(data=my_data, adapter=my_adapter)
```

Register custom adapters for reuse:

```python
from streamlit_activity_calendar import register_adapter

register_adapter("my_domain", my_adapter)
activity_calendar(data=my_data, adapter="my_domain")
```

## 🎨 Theming

Safe theme customization using predefined CSS properties.

```python
theme = {
    "backgroundColor": "#ffffff",    # Calendar background
    "gridColor": "#e0e0e0",         # Grid lines
    "textColor": "#333333",          # Text color
    "borderRadius": 4,               # Border radius in pixels
    "selectionColor": "#4CAF50",    # Selection highlight
    "foregroundColor": "#f5f5f5",   # Foreground color
    "accentColor": "#2196F3",       # Accent color
}

activity_calendar(
    data=events,
    adapter="flat_events",
    theme=theme,
    key="themed_calendar"
)
```

## 📮 Selection Events

The component emits structured selection events back to Streamlit.

### Cell Selection

```python
selection = activity_calendar(data=events, key="cal")

if selection and selection["event"] == "cell_selected":
    cell = selection["cell"]
    # {"row": 2, "column": 4, "date": "2026-04-13"}
```

### Activity Selection

```python
if selection and selection["event"] == "activity_selected":
    activity = selection["calendarEvent"]
    # {"id": "...", "title": "...", "start": "...", ...}
    
    # Access original domain object
    raw = selection["raw"]
```

## 🔧 Configuration

```python
activity_calendar(
    data=events,
    adapter="flat_events",
    
    # Time Range
    start_hour=6,              # Start hour (0-23)
    end_hour=22,               # End hour (0-23)
    
    # Interaction
    selectable=True,           # Enable selection
    enable_activity_popover=True,  # Show activity details on click
    
    # Layout
    show_time_labels=True,     # Show time labels on left
    compact_mode=False,        # Compact layout
    
    # Component
    key="my_calendar",         # Unique key for Streamlit
    theme=theme,               # Theme config
)
```

## 📋 CalendarEvent Structure

```python
from streamlit_activity_calendar import CalendarEvent

event = CalendarEvent(
    id="unique_id",
    start="2026-04-13",           # ISO date
    title="Event Title",
    end="2026-04-13",             # Optional
    color="#2196F3",              # Optional hex color
    category="work",              # Optional category
    playerId="player1",           # Optional player/subject ID
    playerName="John Doe",        # Optional player/subject name
    metadata={                    # Optional custom data
        "sets": 3,
        "reps": 10,
        "notes": "..."
    },
    raw=original_object           # Optional original domain object
)
```

## 📚 Examples

See `examples/` directory:

- **basic_app.py** - Simple calendar with events
- **crud_app.py** - Full CRUD management with session state
- **medical_rehab_demo.py** - Nested medical data with adapters
- **themed_app.py** - Theme showcase with presets

Run examples:

```bash
streamlit run examples/basic_app.py
streamlit run examples/crud_app.py
streamlit run examples/medical_rehab_demo.py
streamlit run examples/themed_app.py
```

## 🧪 Testing

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_adapters.py

# With coverage
pytest --cov=python/streamlit_activity_calendar tests/

# Run frontend tests (TypeScript)
cd frontend
npm test
```

### Test Files

- **test_python_api.py** - Python API and component wrapper tests
- **test_adapters.py** - Data adapter system tests
- **test_frontend_events.py** - Event payload structure tests

## 📦 Development Setup

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn

### Development Workflow

```bash
# 1. Install Python dependencies
pip install -e ".[dev]"

# 2. Build frontend
cd frontend
npm install
npm run build
cd ..

# 3. Run example app in development
streamlit run examples/basic_app.py

# 4. Run tests
pytest

# 5. Type checking
mypy python/
```

### Frontend Development

```bash
cd frontend

# Development mode with hot reload
npm run dev

# Build for production
npm run build

# Preview build
npm run preview
```

### Frontend Stack

- **React 18** - UI framework
- **TypeScript** - Type safety
- **Vite** - Build tool
- **Zustand** - State management
- **dayjs** - Date utilities
- **CSS Grid** - Layout

### Python Stack

- **Streamlit** - Component framework
- **Hatchling** - Build backend
- **Pytest** - Testing

## 🎓 Best Practices

### 1. Keep Component Stateless

```python
# ❌ DON'T store business state in component
selection = activity_calendar(
    data=events,  # Changing this doesn't persist state
    key="calendar"
)

# ✅ DO store state in Streamlit session_state
if "selected_activity" not in st.session_state:
    st.session_state.selected_activity = None

selection = activity_calendar(data=events, key="calendar")
if selection:
    st.session_state.selected_activity = selection
```

### 2. Handle Selection Events

```python
# ✅ Always check event type
selection = activity_calendar(data=events, key="calendar")

if not selection:
    st.info("No selection")
elif selection["event"] == "cell_selected":
    st.write("Cell:", selection["cell"])
elif selection["event"] == "activity_selected":
    st.write("Activity:", selection["calendarEvent"]["title"])
```

### 3. Use Appropriate Adapters

```python
# ✅ Choose adapter matching your data structure
if has_nested_rehab_data:
    adapter = "medical_rehab"
elif has_project_tasks:
    adapter = "project_timeline"
else:
    adapter = "flat_events"
```

### 4. Validate Theme Configuration

```python
# ✅ Theme colors are automatically validated
theme = {
    "backgroundColor": "#ffffff",    # Valid hex
    "gridColor": "#e0e0e0",
    # Invalid keys are silently ignored
    "unknownKey": "value"
}

activity_calendar(data=events, theme=theme)  # Safe
```

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Write tests for new functionality
4. Submit a pull request

## 📄 License

MIT License - see [LICENSE](LICENSE) file

## 🆘 Support

- **Issues** - Report bugs on GitHub
- **Documentation** - See README and examples
- **Questions** - Create a discussion on GitHub

## 🗺️ Roadmap

- [ ] Multi-week navigation
- [ ] Drag-and-drop activity rearrangement
- [ ] Export calendar to PDF/image
- [ ] Activity filtering UI
- [ ] Advanced date range selection
- [ ] Activity search functionality
- [ ] Accessibility improvements (WCAG 2.1)

## 🙏 Acknowledgments

Built with:
- [Streamlit](https://streamlit.io)
- [React](https://react.dev)
- [Zustand](https://github.com/pmndrs/zustand)
- [dayjs](https://day.js.org)

---

**Made with ❤️ for building better Streamlit applications**
