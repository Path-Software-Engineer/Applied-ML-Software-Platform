import React from "react";

import { InventoryRecommendationCard } from "./InventoryRecommendationCard.jsx";
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
  const {
    summary,
    freshness,
    snapshot,
    demand_signal: demandSignal,
    policy,
    ranking,
    recommendation_cards: cards,
    limitations,
  } = data;
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

        {freshness.status === "stale" && (
          <aside className="freshness-warning" role="status">
            <strong>Historical evidence</strong>
            <span>
              This snapshot is {freshness.age_days} days old. Refresh inventory
              evidence before using any suggested quantity.
            </span>
          </aside>
        )}

        <section className="section-block inventory-section" id="inventory-priority">
          <div className="section-header">
            <div>
              <p className="section-kicker">Review order</p>
              <h2>Priority is explicit and traceable.</h2>
            </div>
            <p>Risk score is a policy index. It is never presented as a stockout probability.</p>
          </div>
          <div className="inventory-table-wrap">
            <table className="inventory-table">
              <caption>Products ranked for inventory review under policy {policy.version}.</caption>
              <thead>
                <tr>
                  <th scope="col">Rank</th>
                  <th scope="col">Product</th>
                  <th scope="col">Stock</th>
                  <th scope="col">Coverage</th>
                  <th scope="col">Reorder point</th>
                  <th scope="col">Suggested</th>
                  <th scope="col">Priority</th>
                </tr>
              </thead>
              <tbody>
                {ranking.map((item) => (
                  <tr key={item.product_id}>
                    <td><span className="rank-chip">{String(item.priority_rank).padStart(2, "0")}</span></td>
                    <th scope="row"><strong>{item.product_name}</strong><small>{item.product_id}</small></th>
                    <td>{item.current_stock_units}</td>
                    <td>{item.coverage_days === null ? "n/a" : `${item.coverage_days.toFixed(2)} d`}</td>
                    <td>{item.reorder_point_units}</td>
                    <td><strong>{item.suggested_quantity_units}</strong></td>
                    <td>
                      <span className={`risk-pill risk-${item.risk_label}`}>{item.risk_label}</span>
                      <span className="risk-meter" aria-label={`${item.risk_score} of 100 priority index`}>
                        <span style={{ width: `${item.risk_score}%` }} />
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </section>

        <section className="section-block inventory-section" id="inventory-recommendations">
          <div className="section-header">
            <div>
              <p className="section-kicker">Recommendation cards</p>
              <h2>Evidence for review, not automatic orders.</h2>
            </div>
            <span className="contract-pill">Contract {data.schema_version}</span>
          </div>
          <div className="inventory-card-grid">
            {cards.map((card) => (
              <InventoryRecommendationCard card={card} key={card.card_id} />
            ))}
          </div>
        </section>

        <section className="section-block policy-trace" id="inventory-policy">
          <div>
            <p className="section-kicker">Policy trace</p>
            <h2>Every number points back to one version.</h2>
          </div>
          <dl>
            <div><dt>Version</dt><dd>{policy.version}</dd></div>
            <div><dt>Lead time</dt><dd>{policy.default_lead_time_days} days</dd></div>
            <div><dt>Safety</dt><dd>{policy.safety_days} day</dd></div>
            <div><dt>Review period</dt><dd>{policy.review_period_days} days</dd></div>
            <div><dt>Rounding</dt><dd>Ceiling to whole units</dd></div>
            <div><dt>Trigger</dt><dd>Stock at or below reorder point</dd></div>
          </dl>
        </section>

        <section className="evidence-limit inventory-limit" id="inventory-limitations">
          <div>
            <p className="section-kicker">Evidence boundary</p>
            <h2>Human review remains mandatory.</h2>
          </div>
          <ul>{limitations.map((limitation) => <li key={limitation}>{limitation}</li>)}</ul>
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
