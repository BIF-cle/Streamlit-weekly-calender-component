/**
 * Main entry point for the activity calendar React component.
 *
 * This initializes the Streamlit component and renders the Calendar.
 */

import React from "react";
import ReactDOM from "react-dom/client";
import { withStreamlitConnection } from "streamlit-component-lib";
import Calendar from "./components/Calendar";
import { CalendarComponentProps } from "./types/activity";

/**
 * App component - wraps Calendar with Streamlit integration.
 */
const App: React.FC = (props: any) => {
  // The props are passed from Streamlit's custom component system
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
