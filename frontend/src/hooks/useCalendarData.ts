/**
 * useCalendarData hook for processing and organizing events.
 *
 * This hook handles:
 * - Building the calendar grid structure
 * - Organizing events by time slot and day
 * - Computing day columns and time slots
 * - Managing week navigation
 */

import { useMemo } from "react";
import dayjs from "dayjs";
import { CalendarEvent, CalendarState, DayColumn, TimeSlot } from "../types/activity";
import { CalendarConfig } from "../types/activity";

interface UseCalendarDataProps {
  events: CalendarEvent[];
  config: CalendarConfig;
  selectedCellRow?: number | null;
  selectedCellColumn?: number | null;
}

/**
 * Compute the ISO week start (Monday) for a given date.
 */
function getWeekStart(date: dayjs.Dayjs): dayjs.Dayjs {
  const day = date.day();
  // Convert dayjs day (0=Sunday) to ISO standard (0=Monday)
  const isoDay = day === 0 ? 6 : day - 1;
  return date.subtract(isoDay, "day").startOf("day");
}

/**
 * Format time for display.
 */
function formatTime(hour: number): string {
  return `${String(hour).padStart(2, "0")}:00`;
}

/**
 * Get day name for a date.
 */
function getDayName(date: dayjs.Dayjs): string {
  return date.format("ddd");
}

export function useCalendarData({
  events,
  config,
  selectedCellRow,
  selectedCellColumn,
}: UseCalendarDataProps): CalendarState {
  return useMemo(() => {
    const startHour = config.startHour;
    const endHour = config.endHour;

    // Get current week
    const now = dayjs();
    const weekStart = getWeekStart(now);
    const weekEnd = weekStart.add(6, "days");

    // Build day columns (Monday - Sunday)
    const days: DayColumn[] = Array.from({ length: 7 }, (_, i) => {
      const date = weekStart.add(i, "day");
      const dateStr = date.format("YYYY-MM-DD");

      // Get events for this day
      const dayEvents = events.filter(
        (e) => e.start.substring(0, 10) === dateStr
      );

      return {
        date: dateStr,
        dayOfWeek: i,
        dayName: getDayName(date),
        dayNumber: date.date(),
        activities: dayEvents,
      };
    });

    // Build time slots
    const timeSlots: TimeSlot[] = Array.from(
      { length: endHour - startHour + 1 },
      (_, i) => {
        const hour = startHour + i;
        const eventsForSlot = events.filter(
          (e) => new Date(e.start).getHours() === hour
        );

        return {
          hour,
          time: formatTime(hour),
          activities: eventsForSlot,
        };
      }
    );

    // Build grid cells
    const cellGrid = Array.from({ length: timeSlots.length }, (_, rowIdx) => {
      return Array.from({ length: 7 }, (_, colIdx) => {
        const day = days[colIdx];
        const timeSlot = timeSlots[rowIdx];

        // Get activities for this cell
        const cellActivities = day.activities;

        const isSelected =
          selectedCellRow === rowIdx && selectedCellColumn === colIdx;

        return {
          row: rowIdx,
          column: colIdx,
          date: day.date,
          hour: timeSlot.hour,
          dayOfWeek: colIdx,
          activities: cellActivities,
          isSelected,
          hasActivity: cellActivities.length > 0,
        };
      });
    });

    return {
      weekStart: weekStart.format("YYYY-MM-DD"),
      weekEnd: weekEnd.format("YYYY-MM-DD"),
      days,
      timeSlots,
      cells: cellGrid,
      selectedCell:
        selectedCellRow != null && selectedCellColumn != null
          ? {
              row: selectedCellRow,
              column: selectedCellColumn,
              date: days[selectedCellColumn].date,
            }
          : null,
      selectedActivity: null,
      hoveredCell: null,
    };
  }, [events, config, selectedCellRow, selectedCellColumn]);
}
