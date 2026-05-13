/**
 * Main entry point for the activity calendar React component.
 *
 * This initializes the Streamlit component and renders the Calendar.
 */

import { useEffect } from "react";
import { Streamlit } from "streamlit-component-lib";
import React from "react";
import ReactDOM from "react-dom/client";
import { withStreamlitConnection } from "streamlit-component-lib";

/**
 * App component - wraps Calendar with Streamlit integration.
 */
const App: React.FC = () => {

  useEffect(() => {
    console.log("SET FRAME HEIGHT RUNNING");
    Streamlit.setFrameHeight(800);
  }, []);

  return (
    <div style={{ height: 800, background: "red" }}>
      TEST COMPONENT
    </div>
  );
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
