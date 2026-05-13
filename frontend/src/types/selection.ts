/**
 * Selection state types for the calendar component.
 */

import { CalendarEvent, CellCoordinates } from "./activity";

export interface SelectionState {
  selectedCell: CellCoordinates | null;
  selectedActivity: CalendarEvent | null;
  hoveredCell: CellCoordinates | null;
  hoveredActivity: CalendarEvent | null;
  multiSelectMode: boolean;
  selectedCells: CellCoordinates[];
  selectedActivities: CalendarEvent[];
}

export interface SelectionActions {
  selectCell: (cell: CellCoordinates) => void;
  selectActivity: (activity: CalendarEvent, cell?: CellCoordinates) => void;
  hoverCell: (cell: CellCoordinates | null) => void;
  hoverActivity: (activity: CalendarEvent | null) => void;
  clearSelection: () => void;
  toggleMultiSelectMode: () => void;
  addToMultiSelection: (cell: CellCoordinates) => void;
  removeFromMultiSelection: (cell: CellCoordinates) => void;
}
