# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-04-13

### Added

#### Core Features
- ✨ Weekly activity calendar component with React frontend
- ✨ Production-quality Streamlit custom component wrapper
- ✨ Flexible data adapter system for normalizing nested domain data
- ✨ Cell and activity selection with event emission to Streamlit
- ✨ Safe theming system with predefined CSS properties
- ✨ Rich metadata support for activities

#### Adapters
- 📊 `identity_adapter` - For flat event lists
- 📊 `flat_events_adapter` - For flat events with metadata
- 📊 `medical_rehab_adapter` - For nested medical rehab data
- 📊 `project_timeline_adapter` - For project management data
- 📊 Custom adapter registration system

#### React Components
- 🎨 `Calendar` - Main orchestrator component
- 🎨 `WeekGrid` - Weekly grid rendering
- 🎨 `ActivityCell` - Individual calendar cells
- 🎨 `ActivityCard` - Activity rendering with colors
- 🎨 `ActivityPopover` - Activity detail display
- 🎨 `Toolbar` - Navigation and controls

#### React Hooks
- 🪝 `useCalendarData` - Process and organize events
- 🪝 `useSelection` - Handle selection events
- 🪝 `useTheme` - Apply theme configuration

#### State Management
- 🔄 Zustand store for UI interaction state
- 🔄 Cell selection tracking
- 🔄 Activity selection tracking
- 🔄 Hover state management
- 🔄 Multi-select mode support

#### Configuration
- ⚙️ Customizable time range (start_hour, end_hour)
- ⚙️ Toggle selection interactivity
- ⚙️ Compact layout mode
- ⚙️ Activity popover control
- ⚙️ Time label visibility toggle
- ⚙️ Theme customization

#### Type System
- 🏷️ Full TypeScript support in frontend
- 🏷️ Full type hints in Python
- 🏷️ CalendarEvent canonical model
- 🏷️ Shared type definitions (Python & TypeScript)

#### Documentation
- 📚 Comprehensive README with examples
- 📚 Development guide with setup instructions
- 📚 Architecture documentation
- 📚 API reference
- 📚 Adapter guide
- 📚 Theming guide

#### Examples
- 📖 Basic usage example (basic_app.py)
- 📖 Full CRUD demo (crud_app.py)
- 📖 Medical rehab data example (medical_rehab_demo.py)
- 📖 Theme showcase (themed_app.py)

#### Testing
- ✅ Python API unit tests
- ✅ Data adapter tests
- ✅ Event payload structure tests
- ✅ >80% test coverage target

#### Build & Deployment
- 📦 Vite-based React build
- 📦 Hatchling-based Python packaging
- 📦 PyPI distribution ready
- 📦 Development and production builds

#### Styling
- 🎨 CSS Grid-based responsive layout
- 🎨 CSS variables for theming
- 🎨 Responsive design for mobile
- 🎨 Accessible color contrasts
- 🎨 Dark mode support ready

### Architecture Highlights

- ✅ Stateless component design
- ✅ No backend coupling
- ✅ Adapter-based data normalization
- ✅ Safe property-based theming (no CSS injection)
- ✅ TypeScript full coverage
- ✅ Comprehensive error handling
- ✅ Production-ready code quality

### Dependencies

**Runtime:**
- `streamlit>=1.20.0`
- `react>=18.2.0`
- `zustand>=4.4.0`
- `dayjs>=1.11.0`

**Development:**
- `pytest>=7.0`
- `black>=22.0`
- `mypy>=0.990`
- `typescript>=5.0`
- `vite>=4.3.0`

### Known Limitations

- Single month view only (future: multi-month navigation)
- No drag-and-drop (future: planned)
- Basic time slot rendering (future: detailed time blocks)
- Export to PDF not yet implemented (future)

### Performance

- Component optimized for large datasets (dense calendars)
- Efficient re-renders with React memoization
- NormalizedCalendarEvent[] format prevents deep traversal
- CSS Grid layout for responsive performance

---

## Versioning Timeline

- **Pre-1.0** - Initial development
- **1.0.0** - Production release (current)
- **1.1.0** - Planned: Enhanced UI, improved accessibility
- **2.0.0** - Planned: Major feature additions, API improvements

---

## Contributing

Contributions are welcome! Please see [DEVELOPMENT.md](DEVELOPMENT.md) for guidelines.

## License

MIT License - see [LICENSE](LICENSE)
