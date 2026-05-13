/**
 * Main entry point for the activity calendar React component.
 *
 * This initializes the Streamlit component and renders the Calendar.
 */

import { useEffect, useState } from "react";
import { Streamlit } from "streamlit-component-lib";
import React from "react";
import ReactDOM from "react-dom/client";
import { withStreamlitConnection } from "streamlit-component-lib";
import Calendar from "./components/Calendar";
import { CalendarComponentProps } from "./types/activity";

/**
 * Error fallback component - displays error message to Streamlit
 */
const ErrorFallback: React.FC<{ error: Error; componentKey?: string }> = ({
  error,
  componentKey,
}) => {
  return (
    <div
      style={{
        padding: "20px",
        backgroundColor: "#ffebee",
        border: "1px solid #ef5350",
        borderRadius: "4px",
        fontFamily: "monospace",
        fontSize: "12px",
        color: "#c62828",
      }}
    >
      <div style={{ fontWeight: "bold", marginBottom: "8px" }}>
        ❌ Calendar component error
      </div>
      <div style={{ whiteSpace: "pre-wrap", wordBreak: "break-word" }}>
        {error.message}
      </div>
      {error.stack && (
        <div style={{ marginTop: "8px", fontSize: "11px", opacity: 0.8 }}>
          {error.stack}
        </div>
      )}
    </div>
  );
};

/**
 * App component - wraps Calendar with Streamlit integration and error handling.
 */
const App: React.FC = (props: any) => {
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    const resize = () => {
      Streamlit.setFrameHeight(document.body.scrollHeight);
    };

    resize();

    const observer = new ResizeObserver(resize);
    observer.observe(document.body);

    return () => observer.disconnect();
  }, []);

  // Setup error handler
  useEffect(() => {
    const handleError = (event: ErrorEvent) => {
      console.error("Uncaught error:", event.error);
      setError(event.error);
    };

    window.addEventListener("error", handleError);
    return () => window.removeEventListener("error", handleError);
  }, []);

  if (error) {
    return <ErrorFallback error={error} />;
  }

  try {
    const componentProps: CalendarComponentProps = props.args?.props || {
      events: [],
      theme: {},
      config: {
        startHour: 6,
        endHour: 22,
        selectable: true,
        showTimeLabels: true,
        compactMode: false,
        enableActivityPopover: true,
      },
    };

    return <Calendar {...componentProps} />;
  } catch (err) {
    const error = err instanceof Error ? err : new Error(String(err));
    return <ErrorFallback error={error} />;
  }
};

// Wrap with Streamlit connection for component library
const AppWithStreamlit = withStreamlitConnection(App);

// Render
const root = ReactDOM.createRoot(document.getElementById("root")!);
root.render(
  <React.StrictMode>
    <AppWithStreamlit />
  </React.StrictMode>
);
