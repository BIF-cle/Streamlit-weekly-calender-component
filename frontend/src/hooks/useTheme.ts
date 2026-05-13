/**
 * useTheme hook for applying theme configuration.
 *
 * Maps theme config to CSS variables that style the calendar.
 */

import { useEffect, useMemo } from "react";
import { ThemeConfig } from "../types/activity";

/**
 * Hook for applying theme configuration as CSS variables.
 *
 * Converts safe theme properties into CSS custom properties that can be
 * used throughout the component styling.
 */
export function useTheme(theme: ThemeConfig): void {
  const cssVariables = useMemo(() => {
    return {
      "--bg-color": theme.backgroundColor || "#ffffff",
      "--grid-color": theme.gridColor || "#e0e0e0",
      "--text-color": theme.textColor || "#333333",
      "--border-radius": `${theme.borderRadius || 4}px`,
      "--selection-color": theme.selectionColor || "#4CAF50",
      "--foreground-color": theme.foregroundColor || "#f5f5f5",
      "--accent-color": theme.accentColor || "#2196F3",
    } as Record<string, string>;
  }, [theme]);

  useEffect(() => {
    // Apply CSS variables to document root
    Object.entries(cssVariables).forEach(([key, value]) => {
      document.documentElement.style.setProperty(key, value);
    });
  }, [cssVariables]);
}

/**
 * Get CSS variable value for use in styled components.
 */
export function getCSSVariable(name: string): string {
  return `var(${name})`;
}

/**
 * Predefined color palette for activity categories.
 */
export const categoryColors: Record<string, string> = {
  strengthening: "#4CAF50",
  flexibility: "#2196F3",
  balance: "#FF9800",
  cardio: "#E91E63",
  neurological: "#9C27B0",
  stretching: "#00BCD4",
  mobility: "#8BC34A",
  functional: "#FFEB3B",
  general: "#9E9E9E",
  medical: "#FF5252",
};

/**
 * Get color for activity category (with fallback to color property).
 */
export function getActivityColor(activity: any): string {
  // Use explicit color if provided
  if (activity.color) {
    return activity.color;
  }

  // Try category mapping
  if (activity.category && categoryColors[activity.category]) {
    return categoryColors[activity.category];
  }

  // Default color
  return categoryColors.general;
}
