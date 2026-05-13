# Quick Start Guide

## 🚀 Get Running in 5 Minutes

### 1. Install Dependencies

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install Python package
pip install streamlit>=1.20.0

# Build frontend
cd frontend
npm install
npm run build
cd ..
```

### 2. Install Package

```bash
# Install in development mode
pip install -e .
```

### 3. Run Example

```bash
streamlit run examples/basic_app.py
```

Open browser to `http://localhost:8501`

## 📚 Project Files Overview

### Python Package (`python/streamlit_activity_calendar/`)

| File | Purpose |
|------|---------|
| `__init__.py` | Public API exports |
| `component.py` | Streamlit integration |
| `adapters.py` | Data transformation |
| `types.py` | Type definitions |
| `utils.py` | Helper functions |

### Frontend (`frontend/src/`)

| Directory | Purpose |
|-----------|---------|
| `components/` | React components |
| `hooks/` | Custom React hooks |
| `state/` | Zustand store |
| `types/` | TypeScript types |
| `styles/` | CSS stylesheets |

### Examples (`examples/`)

| File | Purpose |
|------|---------|
| `basic_app.py` | Simple calendar |
| `crud_app.py` | Full CRUD demo |
| `medical_rehab_demo.py` | Adapter example |
| `themed_app.py` | Theme showcase |

### Tests (`tests/`)

| File | Purpose |
|------|---------|
| `test_python_api.py` | API tests |
| `test_adapters.py` | Adapter tests |
| `test_frontend_events.py` | Event tests |

### Configuration

| File | Purpose |
|------|---------|
| `pyproject.toml` | Python packaging |
| `frontend/package.json` | npm dependencies |
| `frontend/vite.config.ts` | Vite build config |
| `frontend/tsconfig.json` | TypeScript config |

### Documentation

| File | Purpose |
|------|---------|
| `README.md` | Main documentation |
| `DEVELOPMENT.md` | Development guide |
| `CHANGELOG.md` | Version history |

## 🎯 Common Tasks

### Run Basic Example
```bash
streamlit run examples/basic_app.py
```

### Run CRUD Demo
```bash
streamlit run examples/crud_app.py
```

### Run Medical Rehab Demo
```bash
streamlit run examples/medical_rehab_demo.py
```

### Run Tests
```bash
pytest tests/ -v
```

### Build Frontend
```bash
cd frontend
npm run build
cd ..
```

### Format Code
```bash
# Python
pip install black isort
black python/
isort python/

# TypeScript
cd frontend
npm install prettier
npm run format
cd ..
```

## 📖 API Quick Reference

### Basic Usage

```python
from streamlit_activity_calendar import activity_calendar

events = [
    {
        "id": "1",
        "start": "2026-04-13",
        "title": "Meeting",
        "color": "#2196F3"
    }
]

selection = activity_calendar(
    data=events,
    adapter="flat_events",
    key="my_calendar"
)

if selection:
    st.write(selection)
```

### Medical Rehab Adapter

```python
from streamlit_activity_calendar import activity_calendar

rehab_data = {
    "players": [
        {
            "id": "p1",
            "name": "Patient",
            "rehab_plans": [
                {
                    "weeks": [
                        {
                            "days": [
                                {
                                    "date": "2026-04-13",
                                    "activities": [
                                        {"id": "a1", "title": "Quad Sets"}
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
```

### Custom Theme

```python
theme = {
    "backgroundColor": "#ffffff",
    "gridColor": "#e0e0e0",
    "textColor": "#333333",
    "selectionColor": "#4CAF50",
    "borderRadius": 4
}

activity_calendar(
    data=events,
    adapter="flat_events",
    theme=theme,
    key="themed_calendar"
)
```

## 🔧 Configuration Options

```python
activity_calendar(
    data=events,                      # Event data
    adapter="flat_events",            # Data adapter
    theme=custom_theme,               # Theme config
    start_hour=6,                     # Start hour (0-23)
    end_hour=22,                      # End hour (0-23)
    selectable=True,                  # Enable selection
    show_time_labels=True,            # Show time labels
    compact_mode=False,               # Compact layout
    enable_activity_popover=True,     # Show activity details
    key="calendar"                    # Component key
)
```

## 📊 Event Payloads

### Cell Selection
```python
{
    "event": "cell_selected",
    "cell": {"row": 2, "column": 4, "date": "2026-04-13"}
}
```

### Activity Selection
```python
{
    "event": "activity_selected",
    "cell": {"row": 2, "column": 4},
    "calendarEvent": {
        "id": "1",
        "start": "2026-04-13",
        "title": "Meeting",
        ...
    },
    "raw": {...original_data...}
}
```

## 🐛 Troubleshooting

### Frontend not building
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
npm run build
cd ..
```

### Import errors
```bash
# Reinstall in development mode
pip install -e .
```

### Port already in use
```bash
streamlit run app.py --server.port 8502
```

### Tests failing
```bash
# Run with verbose output
pytest tests/ -vv

# Run specific test
pytest tests/test_adapters.py::TestMedicalRehabAdapter -v
```

## 📚 Next Steps

1. **Read Documentation** - See [README.md](README.md)
2. **Explore Examples** - Check `examples/` directory
3. **Review Architecture** - See [DEVELOPMENT.md](DEVELOPMENT.md)
4. **Run Tests** - `pytest tests/ -v`
5. **Build Frontend** - `cd frontend && npm run build`

## 🤝 Contributing

See [DEVELOPMENT.md](DEVELOPMENT.md) for:
- Code style guidelines
- Testing requirements
- Publishing instructions
- Git workflow

## 📞 Support

- Check [README.md](README.md) for usage
- Check [DEVELOPMENT.md](DEVELOPMENT.md) for development
- See `examples/` for code examples
- Run tests to verify setup

---

**Ready to build amazing calendars! 🚀**
