# Development Guide

## 📋 Table of Contents

1. [Project Structure](#project-structure)
2. [Development Setup](#development-setup)
3. [Architecture Overview](#architecture-overview)
4. [Building](#building)
5. [Testing](#testing)
6. [Contributing](#contributing)
7. [Publishing](#publishing)

## 📁 Project Structure

```
streamlit-activity-calendar/
│
├── python/
│   └── streamlit_activity_calendar/
│       ├── __init__.py           # Public API exports
│       ├── component.py          # Streamlit component wrapper
│       ├── adapters.py           # Data transformation adapters
│       ├── types.py              # Type definitions
│       └── utils.py              # Utility functions
│
├── frontend/
│   ├── src/
│   │   ├── main.tsx              # React entry point
│   │   ├── Calendar.tsx          # Main component
│   │   ├── components/           # React components
│   │   │   ├── WeekGrid.tsx
│   │   │   ├── ActivityCell.tsx
│   │   │   ├── ActivityCard.tsx
│   │   │   ├── ActivityPopover.tsx
│   │   │   └── Toolbar.tsx
│   │   ├── hooks/                # Custom React hooks
│   │   │   ├── useCalendarData.ts
│   │   │   ├── useSelection.ts
│   │   │   └── useTheme.ts
│   │   ├── state/                # Zustand store
│   │   │   └── calendarStore.ts
│   │   ├── types/                # TypeScript types
│   │   │   ├── activity.ts
│   │   │   └── selection.ts
│   │   └── styles/               # CSS styles
│   │       └── base.css
│   ├── index.html
│   ├── package.json
│   ├── vite.config.ts
│   ├── tsconfig.json
│   └── tsconfig.node.json
│
├── examples/
│   ├── basic_app.py              # Simple example
│   ├── crud_app.py               # CRUD demo
│   ├── medical_rehab_demo.py     # Adapter example
│   └── themed_app.py             # Theme showcase
│
├── tests/
│   ├── test_python_api.py        # API tests
│   ├── test_adapters.py          # Adapter tests
│   └── test_frontend_events.py   # Event tests
│
├── pyproject.toml                # Python package config
├── README.md                     # Main documentation
└── .gitignore
```

## 🚀 Development Setup

### Prerequisites

- Python 3.8+ ([Download](https://www.python.org/downloads/))
- Node.js 16+ ([Download](https://nodejs.org/))
- Git ([Download](https://git-scm.com/))

### Initial Setup

```bash
# Clone repository
git clone https://github.com/yourusername/streamlit-activity-calendar.git
cd streamlit-activity-calendar

# Create Python virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install Python package in development mode
pip install -e .
pip install -e ".[dev]"

# Install frontend dependencies
cd frontend
npm install
cd ..

# Build frontend
cd frontend
npm run build
cd ..
```

### Verify Setup

```bash
# Test Python imports
python -c "from streamlit_activity_calendar import activity_calendar; print('✓ Python OK')"

# Check frontend build
ls frontend/dist/index.js && echo "✓ Frontend OK"

# Run a test
pytest tests/test_python_api.py::TestCalendarEvent::test_create_basic_event -v
```

## 🏗️ Architecture Overview

### Design Principles

1. **Separation of Concerns**
   - React component handles UI only
   - Python wrapper handles communication
   - Adapters handle data transformation
   - Streamlit app handles business logic

2. **Stateless Component**
   - No persistent state in React
   - All state in Streamlit session_state
   - Events emitted to parent Streamlit app

3. **Type Safety**
   - Full TypeScript in frontend
   - Full type hints in Python
   - Shared type definitions

4. **Reusability**
   - Generic calendar, not domain-specific
   - Adapter system for data flexibility
   - Safe theme customization

### Data Flow

```
Streamlit App
    ↓
activity_calendar(data=events, adapter="...")
    ↓ [Python wrapper]
    ├─ Adapter transforms data
    ├─ Validates configuration
    └─ Sends to React
    ↓ [Frontend]
    ├─ Renders calendar
    ├─ Handles interactions
    └─ Emits events
    ↓ [Python callback]
Selection payload returned to Streamlit App
```

### Key Components

**Python Layer:**
- `component.py` - Streamlit integration, API entry point
- `adapters.py` - Data transformation pipeline
- `types.py` - Shared type definitions
- `utils.py` - Helpers for validation and parsing

**React Layer:**
- `Calendar.tsx` - Main orchestrator component
- `WeekGrid.tsx` - Grid layout and structure
- `ActivityCell.tsx` - Individual cells with activities
- `ActivityCard.tsx` - Individual activity rendering
- `calendarStore.ts` - Zustand selection state
- `useCalendarData.ts` - Data processing hook
- `useSelection.ts` - Selection event handling

## 🔨 Building

### Development Build

```bash
# Build frontend for development
cd frontend
npm run dev
cd ..

# In another terminal, run Streamlit app
streamlit run examples/basic_app.py
```

### Production Build

```bash
# Build frontend
cd frontend
npm run build
cd ..

# Verify build output
ls -la frontend/dist/

# Build Python package
python -m build

# Verify wheel
ls -la dist/
```

### Frontend Build Process

```bash
cd frontend

# 1. Install dependencies
npm install

# 2. Run TypeScript compiler
npm run build

# Output files
# dist/index.js       - Main bundle
# dist/index.css      - Styles (if any)
```

The built files in `frontend/dist/` are referenced by the Python component wrapper.

## 🧪 Testing

### Running Tests

```bash
# Run all tests
pytest -v

# Run specific test file
pytest tests/test_adapters.py -v

# Run specific test
pytest tests/test_adapters.py::TestMedicalRehabAdapter::test_medical_rehab_adapter_basic -v

# With coverage report
pytest --cov=python/streamlit_activity_calendar tests/

# Generate HTML coverage report
pytest --cov=python/streamlit_activity_calendar --cov-report=html tests/
# Open htmlcov/index.html
```

### Test Structure

**test_python_api.py**
- CalendarEvent creation and serialization
- Theme validation and sanitization
- Color normalization
- Date parsing
- Event payload structures

**test_adapters.py**
- Identity adapter
- Flat events adapter
- Medical rehab adapter
- Project timeline adapter
- Custom adapter registration
- Category color mapping

**test_frontend_events.py**
- Event payload structures
- Component props validation
- Calendar state structure
- Selection state validation

### Writing Tests

```python
def test_my_feature():
    """Test description."""
    # Arrange
    data = {...}
    
    # Act
    result = function(data)
    
    # Assert
    assert result == expected
```

### Type Checking

```bash
# Run mypy type checker
mypy python/streamlit_activity_calendar --strict

# Check specific file
mypy python/streamlit_activity_calendar/adapters.py
```

## 📝 Contributing

### Code Style

**Python:**
```bash
# Format code
black python/

# Sort imports
isort python/

# Lint
flake8 python/

# Type check (optional)
mypy python/
```

**TypeScript/React:**
```bash
# Format
cd frontend
npm run format

# Lint
npm run lint
```

### Commit Messages

```
type(scope): brief description

- Detailed explanation
- Additional context
- References issue #123
```

Types: `feat`, `fix`, `refactor`, `docs`, `test`, `chore`

### Pull Request Process

1. Create feature branch: `git checkout -b feature/my-feature`
2. Make changes with tests
3. Run full test suite: `pytest`
4. Format code: `black python/ && cd frontend && npm run format`
5. Commit with meaningful message
6. Push to fork and create pull request
7. Ensure CI passes

## 📦 Publishing

### PyPI Publication

#### 1. Prepare Release

```bash
# Update version in pyproject.toml
vim pyproject.toml
# Change: version = "1.0.1"

# Update version in __init__.py
vim python/streamlit_activity_calendar/__init__.py
# Change: __version__ = "1.0.1"

# Create tag
git tag v1.0.1
```

#### 2. Build

```bash
# Clean previous builds
rm -rf build/ dist/ *.egg-info

# Build distribution
python -m build

# Verify contents
tar -tzf dist/streamlit-activity-calendar-1.0.1.tar.gz | head -20
```

#### 3. Test PyPI Upload (Recommended)

```bash
# Install twine
pip install twine

# Upload to TestPyPI
twine upload -r testpypi dist/*

# Test installation
pip install -i https://test.pypi.org/simple/ streamlit-activity-calendar
```

#### 4. Production PyPI Upload

```bash
# Upload to PyPI
twine upload dist/*

# Verify
pip install streamlit-activity-calendar --upgrade
```

### Publishing Checklist

- [ ] Tests passing
- [ ] Code formatted
- [ ] Type checks passing
- [ ] README updated
- [ ] Changelog updated
- [ ] Version bumped in pyproject.toml
- [ ] Version bumped in __init__.py
- [ ] Git tag created
- [ ] Built successfully
- [ ] Tested on TestPyPI
- [ ] Uploaded to PyPI
- [ ] Release notes published

### Version Bumping

Follow [Semantic Versioning](https://semver.org/):
- MAJOR: Breaking changes (1.0.0)
- MINOR: New features, backward compatible (1.1.0)
- PATCH: Bug fixes, backward compatible (1.0.1)

Example progression:
```
1.0.0-alpha  →  1.0.0-beta  →  1.0.0  →  1.0.1  →  1.1.0  →  2.0.0
```

## 📊 Project Statistics

- **Languages:** Python, TypeScript, React, CSS
- **Python Files:** ~4 core modules + examples + tests
- **React Components:** ~5 main components + hooks
- **Type Definitions:** Shared between Python and TypeScript
- **Test Coverage:** >80% target
- **Build Size:** Frontend ~50KB gzipped, Python ~30KB

## 🔗 Resources

- [Streamlit Components Documentation](https://docs.streamlit.io/library/components/custom-components)
- [React Documentation](https://react.dev)
- [Zustand Documentation](https://github.com/pmndrs/zustand)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)
- [Vite Guide](https://vitejs.dev/guide/)

## 🐛 Debugging

### Python Debugging

```python
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

logger.debug(f"Event received: {event}")
```

### Frontend Debugging

```typescript
console.log("Rendered with props:", props);
console.debug("Selection state:", store.getState());
```

### Streamlit Debugging

```bash
# Enable Streamlit logger
streamlit run app.py --logger.level=debug
```

## 📚 Additional Documentation

- [README.md](README.md) - User documentation
- [examples/](examples/) - Working examples
- [LICENSE](LICENSE) - MIT license information

---

For questions or issues, please open a GitHub issue.
