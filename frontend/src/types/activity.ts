/**
 * Frontend type definitions for calendar events and interactions.
 *
 * This module defines TypeScript interfaces that match the Python
 * type system for type-safe communication between frontend and backend.
 */

export interface CalendarEvent {
  id: string;
  start: string; // ISO date string
  end?: string; // ISO date string
  title: string;
  color?: string; // Hex color code
  category?: string;
  playerId?: string;
  playerName?: string;
  metadata?: Record<string, any>;
  raw?: any; // Original domain object
}

export interface CellCoordinates {
  row: number;
  column: number;
  date?: string;
}

export interface CellSelectionEvent {
  event: "cell_selected";
  cell: CellCoordinates;
}

export interface ActivitySelectionEvent {
  event: "activity_selected";
  cell: CellCoordinates;
  calendarEvent: CalendarEvent;
  raw?: any;
}

export type SelectionEvent = CellSelectionEvent | ActivitySelectionEvent;

export interface ThemeConfig {
  backgroundColor?: string;
  gridColor?: string;
  textColor?: string;
  borderRadius?: number;
  selectionColor?: string;
  foregroundColor?: string;
  accentColor?: string;
}

export interface CalendarConfig {
  startHour: number;
  endHour: number;
  selectable: boolean;
  showTimeLabels: boolean;
  compactMode: boolean;
  enableActivityPopover: boolean;
}

export interface CalendarComponentProps {
  events: CalendarEvent[];
  theme: ThemeConfig;
  config: CalendarConfig;
  version?: string;
}

export interface DayColumn {
  date: string;
  dayOfWeek: number; // 0 = Monday, 6 = Sunday
  dayName: string;
  dayNumber: number;
  activities: CalendarEvent[];
}

export interface TimeSlot {
  hour: number;
  time: string;
  activities: CalendarEvent[];
}

/**
 * Represents a single cell in the calendar grid.
 *
 * A cell is at the intersection of a time slot and a day column.
 */
export interface CalendarCell {
  row: number; // Time slot row
  column: number; // Day column
  date: string; // ISO date
  hour: number;
  dayOfWeek: number;
  activities: CalendarEvent[];
  isSelected: boolean;
  hasActivity: boolean;
}

/**
 * Calendar state for rendering.
 *
 * This is computed from events and includes spatial information
 * needed for rendering the grid.
 */
export interface CalendarState {
  weekStart: string; // Monday in ISO format
  weekEnd: string; // Sunday in ISO format
  days: DayColumn[];
  timeSlots: TimeSlot[];
  cells: CalendarCell[][];
  selectedCell: CellCoordinates | null;
  selectedActivity: CalendarEvent | null;
  hoveredCell: CellCoordinates | null;
}
