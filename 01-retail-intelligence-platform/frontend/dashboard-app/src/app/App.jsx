import React from "react";

import { DemandDashboard } from "../features/demand-summary/components/DemandDashboard.jsx";
import { InventoryDecisionDashboard } from "../features/inventory-decision/components/InventoryDecisionDashboard.jsx";
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

  if (view === "model-comparison") return <ModelComparisonDashboard />;
  if (view === "inventory-decision") return <InventoryDecisionDashboard />;
  return <DemandDashboard />;
}
