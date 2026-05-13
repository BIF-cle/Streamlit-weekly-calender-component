/**
 * Toolbar component - provides navigation and controls.
 * 
 * Allows users to:
 * - Navigate between weeks
 * - View current week/date
 * - Access settings (future)
 */

import React from "react";
import dayjs from "dayjs";

interface ToolbarProps {
  weekStart: string; // ISO date
  weekEnd: string; // ISO date
  onPreviousWeek?: () => void;
  onNextWeek?: () => void;
  onToday?: () => void;
}

/**
 * Toolbar provides navigation and information display.
 */
const Toolbar: React.FC<ToolbarProps> = ({
  weekStart,
  weekEnd,
  onPreviousWeek,
  onNextWeek,
  onToday,
}) => {
  const formatDateRange = (start: string, end: string): string => {
    const startDate = dayjs(start);
    const endDate = dayjs(end);

    if (startDate.format("YYYY-MM") === endDate.format("YYYY-MM")) {
      return `${startDate.format("MMM D")} - ${endDate.format("D, YYYY")}`;
    }

    return `${startDate.format("MMM D")} - ${endDate.format("MMM D, YYYY")}`;
  };

  return (
    <div className="calendar-header">
      <div>
        <h2 className="calendar-title">Activity Calendar</h2>
        <p className="calendar-week-label">{formatDateRange(weekStart, weekEnd)}</p>
      </div>
      <div className="calendar-toolbar">
        <button
          className="toolbar-button"
          onClick={onPreviousWeek}
          aria-label="Previous week"
        >
          ← Previous
        </button>
        <button
          className="toolbar-button"
          onClick={onToday}
          aria-label="Current week"
        >
          Today
        </button>
        <button
          className="toolbar-button"
          onClick={onNextWeek}
          aria-label="Next week"
        >
          Next →
        </button>
      </div>
    </div>
  );
};

export default Toolbar;
