/**
 * Zustand store for managing calendar interaction state.
 *
 * This store manages:
 * - Cell selection
 * - Activity selection
 * - Hover state
 * - Multi-select mode
 *
 * This is UI interaction state only - NOT business/backend state.
 */

import { create } from "zustand";
import { CalendarEvent, CellCoordinates } from "../types/activity";
import { SelectionState, SelectionActions } from "../types/selection";

/**
 * Calendar selection store using Zustand.
 *
 * Provides:
 * - Single cell and activity selection
 * - Hover state tracking
 * - Multi-select mode (for future bulk operations)
 *
 * This store is UI-focused and does not handle persistencebusiness logic.
 */
export const useCalendarStore = create<SelectionState & SelectionActions>(
  (set) => ({
    // Initial state
    selectedCell: null,
    selectedActivity: null,
    hoveredCell: null,
    hoveredActivity: null,
    multiSelectMode: false,
    selectedCells: [],
    selectedActivities: [],

    // Actions
    selectCell: (cell: CellCoordinates) =>
      set((state) => ({
        selectedCell: cell,
        selectedActivity: null,
        selectedCells: state.multiSelectMode
          ? [...state.selectedCells, cell]
          : [cell],
      })),

    selectActivity: (activity: CalendarEvent, cell?: CellCoordinates) =>
      set((state) => ({
        selectedActivity: activity,
        selectedCell: cell || state.selectedCell,
        selectedActivities: state.multiSelectMode
          ? [...state.selectedActivities, activity]
          : [activity],
      })),

    hoverCell: (cell: CellCoordinates | null) =>
      set({
        hoveredCell: cell,
      }),

    hoverActivity: (activity: CalendarEvent | null) =>
      set({
        hoveredActivity: activity,
      }),

    clearSelection: () =>
      set({
        selectedCell: null,
        selectedActivity: null,
        selectedCells: [],
        selectedActivities: [],
        hoveredCell: null,
        hoveredActivity: null,
      }),

    toggleMultiSelectMode: () =>
      set((state) => ({
        multiSelectMode: !state.multiSelectMode,
        selectedCells: !state.multiSelectMode ? [] : state.selectedCells,
        selectedActivities: !state.multiSelectMode ? [] : state.selectedActivities,
      })),

    addToMultiSelection: (cell: CellCoordinates) =>
      set((state) => {
        const isAlreadySelected = state.selectedCells.some(
          (c) => c.row === cell.row && c.column === cell.column
        );
        return {
          selectedCells: isAlreadySelected
            ? state.selectedCells
            : [...state.selectedCells, cell],
        };
      }),

    removeFromMultiSelection: (cell: CellCoordinates) =>
      set((state) => ({
        selectedCells: state.selectedCells.filter(
          (c) => !(c.row === cell.row && c.column === cell.column)
        ),
      })),
  })
);
