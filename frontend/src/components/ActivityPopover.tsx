/**
 * ActivityPopover component - displays detailed activity information.
 *
 * Shows:
 * - Activity title
 * - Category
 * - Metadata (sets, reps, duration, notes)
 * - Player information
 */

import React, { useMemo } from "react";
import { CalendarEvent } from "../types/activity";

interface ActivityPopoverProps {
  activity: CalendarEvent;
  onClose: () => void;
}

/**
 * ActivityPopover displays detailed information about a selected activity.
 */
const ActivityPopover: React.FC<ActivityPopoverProps> = ({
  activity,
  onClose,
}) => {
  const formatDate = (dateStr: string): string => {
    try {
      return new Date(dateStr).toLocaleDateString();
    } catch {
      return dateStr;
    }
  };

  const hasMetadata = useMemo(
    () =>
      activity.metadata &&
      Object.keys(activity.metadata).filter((k) => activity.metadata![k])
        .length > 0,
    [activity.metadata]
  );

  return (
    <div className="activity-popover" onClick={(e) => e.stopPropagation()}>
      <div className="activity-popover-header">{activity.title}</div>
      <div className="activity-popover-body">
        {activity.category && (
          <div className="activity-popover-field">
            <span className="activity-popover-label">Category:</span>
            <span className="activity-popover-value">{activity.category}</span>
          </div>
        )}

        {activity.playerName && (
          <div className="activity-popover-field">
            <span className="activity-popover-label">Player:</span>
            <span className="activity-popover-value">{activity.playerName}</span>
          </div>
        )}

        {activity.start && (
          <div className="activity-popover-field">
            <span className="activity-popover-label">Date:</span>
            <span className="activity-popover-value">
              {formatDate(activity.start)}
            </span>
          </div>
        )}

        {hasMetadata && (
          <>
            {activity.metadata?.sets && (
              <div className="activity-popover-field">
                <span className="activity-popover-label">Sets:</span>
                <span className="activity-popover-value">
                  {activity.metadata.sets}
                </span>
              </div>
            )}

            {activity.metadata?.reps && (
              <div className="activity-popover-field">
                <span className="activity-popover-label">Reps:</span>
                <span className="activity-popover-value">
                  {activity.metadata.reps}
                </span>
              </div>
            )}

            {activity.metadata?.duration_minutes && (
              <div className="activity-popover-field">
                <span className="activity-popover-label">Duration:</span>
                <span className="activity-popover-value">
                  {activity.metadata.duration_minutes} min
                </span>
              </div>
            )}

            {activity.metadata?.notes && (
              <div className="activity-popover-field">
                <span className="activity-popover-label">Notes:</span>
                <span className="activity-popover-value">
                  {activity.metadata.notes}
                </span>
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
};

export default ActivityPopover;
