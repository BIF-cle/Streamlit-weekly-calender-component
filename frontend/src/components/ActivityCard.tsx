/**
 * ActivityCard component - renders a single activity in a calendar cell.
 *
 * Handles:
 * - Activity rendering with title and color
 * - Hover states
 * - Click selection
 * - Metadata display
 */

import React, { useMemo, useState } from "react";
import { CalendarEvent, CellCoordinates } from "../types/activity";
import { getActivityColor } from "../hooks/useTheme";
import ActivityPopover from "./ActivityPopover";

interface ActivityCardProps {
  activity: CalendarEvent;
  cell: CellCoordinates;
  isSelected: boolean;
  onSelect: (activity: CalendarEvent, cell: CellCoordinates) => void;
  enablePopover: boolean;
}

/**
 * ActivityCard displays a single activity with color-coding and interactivity.
 */
const ActivityCard: React.FC<ActivityCardProps> = ({
  activity,
  cell,
  isSelected,
  onSelect,
  enablePopover,
}) => {
  const [showPopover, setShowPopover] = useState(false);
  const backgroundColor = useMemo(() => getActivityColor(activity), [activity]);

  const handleClick = (e: React.MouseEvent) => {
    e.stopPropagation();
    onSelect(activity, cell);
    if (enablePopover) {
      setShowPopover(!showPopover);
    }
  };

  return (
    <div
      className={`activity-card ${isSelected ? "selected" : ""}`}
      style={{
        backgroundColor,
      }}
      onClick={handleClick}
      title={activity.title}
    >
      <span className="activity-title">{activity.title}</span>

      {activity.metadata?.sets && (
        <span className="activity-metadata">
          {activity.metadata.sets}x{activity.metadata.reps || ""}
        </span>
      )}

      {showPopover && enablePopover && (
        <ActivityPopover
          activity={activity}
          onClose={() => setShowPopover(false)}
        />
      )}
    </div>
  );
};

export default ActivityCard;
