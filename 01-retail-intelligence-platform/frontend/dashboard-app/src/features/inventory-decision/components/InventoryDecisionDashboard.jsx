import React from "react";

import { useInventoryDecision } from "../hooks/useInventoryDecision.js";
import { PlatformShell } from "../../../shared/components/PlatformShell.jsx";
import { PLATFORM_STAGES } from "../../../shared/navigation/platformNavigation.js";


function InventoryShell({ status, children }) {
  return (
    <PlatformShell
      activeHref="#inventory-decisions"
      activeStageId="inventory-decision"
      homeHref="#demand-insight"
      moduleName="Inventory Decision"
      navigation={PLATFORM_STAGES}
      noteTitle="Human review required"
      noteSubtitle="Inventory Decision · Sprint 3"
      status={status}
      variant="inventory"
    >
      {children}
    </PlatformShell>
  );
}


function LoadingView() {
  return (
    <InventoryShell status="loading">
      <div className="dashboard loading-state" aria-live="polite" aria-busy="true">
        <div className="skeleton comparison-hero-skeleton" />
        <p>Loading validated inventory evidence…</p>
      </div>
    </InventoryShell>
  );
}


function UnavailableView({ message, retry }) {
  return (
    <InventoryShell status="unavailable">
      <section className="state-card" role="alert">
        <span className="state-code">503</span>
        <p className="section-kicker">Evidence unavailable</p>
        <h1>We could not load Inventory Decision.</h1>
        <p>{message}</p>
        <button type="button" onClick={retry}>Try again</button>
        <small>No fallback stock, risk score or suggested quantity is shown.</small>
      </section>
    </InventoryShell>
  );
}


function ConnectedView({ data }) {
  const { summary, freshness, snapshot, demand_signal: demandSignal } = data;
  return (
    <InventoryShell status="connected">
      <div className="dashboard inventory-dashboard">
        <section className="inventory-hero" id="inventory-decisions">
          <div>
            <p className="section-kicker">Observed inventory review</p>
            <h1>Prioritize stock,<br /><em>keep the human decision.</em></h1>
            <p>
              Inventory Decision joins one validated stock snapshot with observed
              demand signals and a versioned review policy. It never places orders.
            </p>
          </div>
          <aside className="experiment-panel" aria-label="Inventory evidence boundary">
            <span>Evidence boundary</span>
            <dl>
              <div><dt>Snapshot</dt><dd>{snapshot.as_of_date}</dd></div>
              <div><dt>Freshness</dt><dd>{freshness.status}</dd></div>
              <div><dt>Signal</dt><dd>{demandSignal.signal_type.replaceAll("_", " ")}</dd></div>
              <div><dt>Status</dt><dd>Learning only</dd></div>
            </dl>
          </aside>
        </section>

        <section className="metric-grid" id="inventory-overview" aria-label="Inventory review summary">
          <article className="metric-card metric-card-accent">
            <span className="metric-label">Review queue</span>
            <strong>{summary.products_requiring_replenishment_review}</strong>
            <small>products require human review</small>
          </article>
          <article className="metric-card">
            <span className="metric-label">Observed stock</span>
            <strong>{summary.stock_on_hand_units}</strong>
            <small>units in the validated snapshot</small>
          </article>
          <article className="metric-card">
            <span className="metric-label">Critical / high</span>
            <strong>{summary.critical_products} / {summary.high_risk_products}</strong>
            <small>priority labels, not probabilities</small>
          </article>
          <article className="metric-card">
            <span className="metric-label">Suggested review</span>
            <strong>{summary.suggested_review_quantity_units}</strong>
            <small>units; no purchase order created</small>
          </article>
        </section>
      </div>
    </InventoryShell>
  );
}


export function InventoryDecisionDashboard() {
  const { status, data, error, retry } = useInventoryDecision();
  if (status === "loading") return <LoadingView />;
  if (status === "unavailable") {
    return <UnavailableView message={error.message} retry={retry} />;
  }
  return <ConnectedView data={data} />;
}
