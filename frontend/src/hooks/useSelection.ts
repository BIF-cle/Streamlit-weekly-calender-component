/**
 * useSelection hook for managing selected cells and activities.
 *
 * Integrates with Zustand store and handles emitting selection events.
 */

import { useCallback } from "react";
import { Streamlit } from "streamlit-component-lib";
import { CalendarEvent, CellCoordinates, SelectionEvent } from "../types/activity";
import { useCalendarStore } from "../state/calendarStore";

export interface UseSelectionProps {
  selectable: boolean;
  enableActivityPopover: boolean;
}

export interface UseSelectionReturn {
  selectCell: (cell: CellCoordinates) => void;
  selectActivity: (activity: CalendarEvent, cell: CellCoordinates) => void;
  isActivitySelected: (activity: CalendarEvent) => boolean;
  isCellSelected: (cell: CellCoordinates) => boolean;
}

/**
 * Hook for managing calendar cell and activity selection.
 *
 * Handles:
 * - Updating local selection state (Zustand)
 * - Emitting selection events through Streamlit
 * - Checking selection status
 */
export function useSelection({
  selectable,
}: UseSelectionProps): UseSelectionReturn {
  const {
    selectedCell,
    selectedActivity,
    selectCell: storeSelectCell,
    selectActivity: storeSelectActivity,
  } = useCalendarStore();

  const selectCell = useCallback(
    (cell: CellCoordinates) => {
      if (!selectable) return;

      // Update local state
      storeSelectCell(cell);

      // Emit event to Streamlit
      const event: SelectionEvent = {
        event: "cell_selected",
        cell,
      };

      Streamlit.setComponentValue(event);
    },
    [selectable, storeSelectCell]
  );

  const selectActivity = useCallback(
    (activity: CalendarEvent, cell: CellCoordinates) => {
      if (!selectable) return;

      // Update local state
      storeSelectActivity(activity, cell);

      // Emit event to Streamlit
      const event: SelectionEvent = {
        event: "activity_selected",
        cell,
        calendarEvent: activity,
        raw: activity.raw,
      };

      Streamlit.setComponentValue(event);
    },
    [selectable, storeSelectActivity]
  );

  const isActivitySelected = useCallback(
    (activity: CalendarEvent): boolean => {
      return selectedActivity?.id === activity.id;
    },
    [selectedActivity]
  );

  const isCellSelected = useCallback(
    (cell: CellCoordinates): boolean => {
      return (
        selectedCell?.row === cell.row &&
        selectedCell?.column === cell.column
      );
    },
    [selectedCell]
  );

  return {
    selectCell,
    selectActivity,
    isActivitySelected,
    isCellSelected,
  };
}
