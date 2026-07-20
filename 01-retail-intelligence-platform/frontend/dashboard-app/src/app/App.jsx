import React from "react";

import { DemandDashboard } from "../features/demand-summary/components/DemandDashboard.jsx";
import { ModelComparisonDashboard } from "../features/model-comparison/components/ModelComparisonDashboard.jsx";


export function App() {
  const [view, setView] = React.useState(() => (
    window.location.hash === "#model-comparison" ? "model-comparison" : "demand-insight"
  ));

  React.useEffect(() => {
    const updateView = () => setView(
      window.location.hash === "#model-comparison"
        ? "model-comparison"
        : "demand-insight",
    );
    window.addEventListener("hashchange", updateView);
    return () => window.removeEventListener("hashchange", updateView);
  }, []);

  return view === "model-comparison"
    ? <ModelComparisonDashboard />
    : <DemandDashboard />;
}
