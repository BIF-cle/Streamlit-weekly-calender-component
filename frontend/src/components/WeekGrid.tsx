/**
 * WeekGrid component - renders the calendar week grid.
 *
 * Handles:
 * - Time slot labels
 * - Day headers (Mon-Sun)
 * - Calendar cells arranged in grid
 * - Responsive layout
 */

import React, { useMemo } from "react";
import { CalendarState, CellCoordinates } from "../types/activity";
import ActivityCell from "./ActivityCell";

interface WeekGridProps {
  calendarData: CalendarState;
  selectedCellRow?: number | null;
  selectedCellColumn?: number | null;
  selectedActivityId?: string;
  onSelectCell: (cell: CellCoordinates) => void;
  onSelectActivity: (activity: any, cell: CellCoordinates) => void;
  onHoverCell?: (cell: CellCoordinates | null) => void;
  showTimeLabels: boolean;
  enableActivityPopover: boolean;
  compactMode: boolean;
}

/**
 * WeekGrid renders the main calendar grid with days and time slots.
 */
const WeekGrid: React.FC<WeekGridProps> = ({
  calendarData,
  selectedCellRow,
  selectedCellColumn,
  selectedActivityId,
  onSelectCell,
  onSelectActivity,
  onHoverCell,
  showTimeLabels,
  enableActivityPopover,
  compactMode,
}) => {
  // Format time labels
  const timeLabels = useMemo(() => {
    return calendarData.timeSlots.map((slot) => slot.time);
  }, [calendarData.timeSlots]);

  // Format day headers
  const dayHeaders = useMemo(() => {
    return calendarData.days.map((day) => ({
      name: day.dayName,
      number: day.dayNumber,
    }));
  }, [calendarData.days]);

  return (
    <div className="calendar-grid-container">
      {/* Time Labels Column (optional) */}
      {showTimeLabels && (
        <div className="time-labels">
          <div className="time-label first"></div>
          {timeLabels.map((time, idx) => (
            <div key={`time-${idx}`} className={`time-label ${compactMode ? "compact" : ""}`}>
              {time}
            </div>
          ))}
        </div>
      )}

      {/* Main Grid */}
      <div style={{ flex: 1, display: "flex", flexDirection: "column", overflow: "auto" }}>
        {/* Day Headers */}
        <div className="day-header-row">
          {dayHeaders.map((day, idx) => (
            <div key={`day-${idx}`} className="day-header">
              <div className="day-name">{day.name}</div>
              <div className="day-number">{day.number}</div>
            </div>
          ))}
        </div>

        {/* Calendar Grid */}
        <div className={`calendar-grid ${compactMode ? "compact" : ""}`}>
          {calendarData.cells.map((row) =>
            row.map((cell) => (
              <ActivityCell
                key={`cell-${cell.row}-${cell.column}`}
                cell={cell}
                activities={cell.activities}
                isSelected={
                  selectedCellRow === cell.row &&
                  selectedCellColumn === cell.column
                }
                selectedActivityId={selectedActivityId}
                onSelectCell={onSelectCell}
                onSelectActivity={onSelectActivity}
                onHoverCell={onHoverCell}
                enableActivityPopover={enableActivityPopover}
                compactMode={compactMode}
              />
            ))
          )}
        </div>
      </div>
    </div>
  );
};

export default WeekGrid;
