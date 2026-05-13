/**
 * Main Calendar component - orchestrates the weekly activity calendar.
 *
 * Integrates:
 * - Data normalization (useCalendarData hook)
 * - Selection management (useSelection hook)
 * - Theme application (useTheme hook)
 * - Component composition (Toolbar, WeekGrid)
 * - Streamlit communication
 */

import React, { useMemo } from "react";
import { Streamlit } from "streamlit-component-lib";
import {
  CalendarEvent,
  CalendarComponentProps,
  CellCoordinates,
} from "../types/activity";
import { useCalendarData } from "../hooks/useCalendarData";
import { useSelection } from "../hooks/useSelection";
import { useTheme } from "../hooks/useTheme";
import { useCalendarStore } from "../state/calendarStore";
import Toolbar from "./Toolbar";
import WeekGrid from "./WeekGrid";
import "../styles/base.css";

interface CalendarProps extends CalendarComponentProps {}

/**
 * Main Calendar component.
 *
 * Handles:
 * - Rendering weekly calendar
 * - Managing selection state
 * - Emitting events to Streamlit
 * - Applying theme configuration
 * - Composing all subcomponents
 */
const Calendar: React.FC<CalendarProps> = ({
  events,
  theme,
  config,
}) => {
  // Apply theme
  useTheme(theme);

  // Get selection state from store
  const { selectedCell, selectedActivity } = useCalendarStore();

  // Process calendar data
  const calendarData = useCalendarData({
    events,
    config,
    selectedCellRow: selectedCell?.row ?? null,
    selectedCellColumn: selectedCell?.column ?? null,
  });

  // Setup selection handlers
  const { selectCell, selectActivity } = useSelection({
    selectable: config.selectable,
    enableActivityPopover: config.enableActivityPopover,
  });

  // Notify Streamlit that component is ready
  React.useEffect(() => {
    Streamlit.setComponentValue(null);
  }, []);

  if (!calendarData || !calendarData.cells || calendarData.cells.length === 0) {
    return (
      <div className="calendar-container">
        <div className="calendar-empty">
          <p>No activities to display</p>
        </div>
      </div>
    );
  }

  return (
    <div className="calendar-container">
      <Toolbar
        weekStart={calendarData.weekStart}
        weekEnd={calendarData.weekEnd}
      />
      <div className="calendar-wrapper">
        <WeekGrid
          calendarData={calendarData}
          selectedCellRow={selectedCell?.row}
          selectedCellColumn={selectedCell?.column}
          selectedActivityId={selectedActivity?.id}
          onSelectCell={selectCell}
          onSelectActivity={selectActivity}
          showTimeLabels={config.showTimeLabels}
          enableActivityPopover={config.enableActivityPopover}
          compactMode={config.compactMode}
        />
      </div>
    </div>
  );
};

export default Calendar;
