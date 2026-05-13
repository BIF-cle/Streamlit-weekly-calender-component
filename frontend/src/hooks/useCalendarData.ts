/**
 * useCalendarData hook for processing and organizing events.
 *
 * This hook handles:
 * - Building the calendar grid structure
 * - Organizing events by time slot and day
 * - Computing day columns and time slots
 * - Managing week navigation
 * - Detecting which week(s) contain events
 */

import { useMemo } from "react";
import dayjs from "dayjs";
import { CalendarEvent, CalendarState, DayColumn, TimeSlot, WeekInfo } from "../types/activity";
import { CalendarConfig } from "../types/activity";

interface UseCalendarDataProps {
  events: CalendarEvent[];
  config: CalendarConfig;
  selectedCellRow?: number | null;
  selectedCellColumn?: number | null;
  weeks?: WeekInfo[];
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

/**
 * Extract date portion from ISO string (handles both date and datetime formats).
 */
function getDateFromStart(start: string): string {
  return start.substring(0, 10);
}

/**
 * Detect which week the events belong to, or use provided weeks.
 * Returns the start date of the week to display.
 */
function detectDisplayWeek(events: CalendarEvent[], weeks?: WeekInfo[]): string {
  // If weeks are provided, use the first one
  if (weeks && weeks.length > 0) {
    return weeks[0].start_date;
  }

  // If we have events, find the earliest event date and get its week start
  if (events.length > 0) {
    const earliestEvent = events.reduce((min, event) => {
      const eventDate = getDateFromStart(event.start);
      const minDate = getDateFromStart(min.start);
      return eventDate < minDate ? event : min;
    });

    const eventDate = getDateFromStart(earliestEvent.start);
    const eventDayjs = dayjs(eventDate);
    const weekStart = getWeekStart(eventDayjs);
    return weekStart.format("YYYY-MM-DD");
  }

  // Fall back to current week
  const now = dayjs();
  const weekStart = getWeekStart(now);
  return weekStart.format("YYYY-MM-DD");
}

export function useCalendarData({
  events,
  config,
  selectedCellRow,
  selectedCellColumn,
  weeks,
}: UseCalendarDataProps): CalendarState {
  return useMemo(() => {
    const startHour = config.startHour;
    const endHour = config.endHour;

    // Detect which week to display
    const weekStartStr = detectDisplayWeek(events, weeks);
    const weekStart = dayjs(weekStartStr).startOf("day");
    const weekEnd = weekStart.add(6, "days");

    // Build day columns (Monday - Sunday)
    const days: DayColumn[] = Array.from({ length: 7 }, (_, i) => {
      const date = weekStart.add(i, "day");
      const dateStr = date.format("YYYY-MM-DD");

      // Get events for this day
      const dayEvents = events.filter(
        (e) => getDateFromStart(e.start) === dateStr
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

        // Get all events for this hour (across all days in this week)
        const eventsForSlot = events.filter((e) => {
          try {
            const eventHour = new Date(e.start).getHours();
            return eventHour === hour;
          } catch {
            return false;
          }
        });

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

        // Get activities for this specific cell (day + hour)
        const cellActivities = day.activities.filter((activity) => {
          try {
            const activityHour = new Date(activity.start).getHours();
            return activityHour === timeSlot.hour;
          } catch {
            return false;
          }
        });

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
  }, [events, config, selectedCellRow, selectedCellColumn, weeks]);
}
