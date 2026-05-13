/**
 * ActivityCell component - represents a single cell in the calendar grid.
 *
 * A cell contains activities for a specific time slot and day.
 * Handles both empty cells and cells with activities.
 */

import React from "react";
import { CalendarEvent, CellCoordinates } from "../types/activity";
import ActivityCard from "./ActivityCard";

interface ActivityCellProps {
  cell: CellCoordinates;
  activities: CalendarEvent[];
  isSelected: boolean;
  selectedActivityId?: string;
  onSelectCell: (cell: CellCoordinates) => void;
  onSelectActivity: (activity: CalendarEvent, cell: CellCoordinates) => void;
  onHoverCell?: (cell: CellCoordinates | null) => void;
  enableActivityPopover: boolean;
  compactMode: boolean;
}

/**
 * ActivityCell renders a single calendar grid cell.
 *
 * Handles:
 * - Rendering multiple activities (stacked)
 * - Cell selection
 * - Activity selection
 * - Hover states
 * - Visual feedback
 */
const ActivityCell: React.FC<ActivityCellProps> = ({
  cell,
  activities,
  isSelected,
  selectedActivityId,
  onSelectCell,
  onSelectActivity,
  onHoverCell,
  enableActivityPopover,
  compactMode,
}) => {
  const hasActivities = activities.length > 0;

  const handleCellClick = () => {
    onSelectCell(cell);
  };

  const handleMouseEnter = () => {
    onHoverCell?.(cell);
  };

  const handleMouseLeave = () => {
    onHoverCell?.(null);
  };

  return (
    <div
      key={`cell-${cell.row}-${cell.column}`}
      className={`calendar-cell ${isSelected ? "selected" : ""} ${
        hasActivities ? "has-activity" : ""
      } ${compactMode ? "compact" : ""}`}
      onClick={handleCellClick}
      onMouseEnter={handleMouseEnter}
      onMouseLeave={handleMouseLeave}
      role="button"
      tabIndex={0}
      aria-label={`Calendar cell at row ${cell.row}, column ${cell.column}, date ${cell.date}`}
    >
      {hasActivities && (
        <div className="activities-container">
          {activities.map((activity) => (
            <ActivityCard
              key={activity.id}
              activity={activity}
              cell={cell}
              isSelected={selectedActivityId === activity.id}
              onSelect={onSelectActivity}
              enablePopover={enableActivityPopover}
            />
          ))}
        </div>
      )}
    </div>
  );
};

export default ActivityCell;
