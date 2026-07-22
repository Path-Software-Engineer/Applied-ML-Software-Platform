import React from "react";

import { DemandDashboard } from "../features/demand-summary/components/DemandDashboard.jsx";
import { ModelComparisonDashboard } from "../features/model-comparison/components/ModelComparisonDashboard.jsx";
import { resolvePlatformView } from "../shared/navigation/platformNavigation.js";


export function App() {
  const [view, setView] = React.useState(() => (
    resolvePlatformView(window.location.hash)
  ));

  React.useEffect(() => {
    const updateView = () => setView(resolvePlatformView(window.location.hash));
    window.addEventListener("hashchange", updateView);
    return () => window.removeEventListener("hashchange", updateView);
  }, []);

  return view === "model-comparison"
    ? <ModelComparisonDashboard />
    : <DemandDashboard />;
}
