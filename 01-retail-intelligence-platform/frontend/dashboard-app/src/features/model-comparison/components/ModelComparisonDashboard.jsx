import React from "react";

import { DecisionCard } from "./DecisionCard.jsx";
import { useModelComparison } from "../hooks/useModelComparison.js";
import { PlatformShell } from "../../../shared/components/PlatformShell.jsx";
import { PLATFORM_STAGES } from "../../../shared/navigation/platformNavigation.js";


const metricFormatter = new Intl.NumberFormat("en-US", {
  minimumFractionDigits: 2,
  maximumFractionDigits: 2,
});


function ModelComparisonShell({ status, children }) {
  return (
    <PlatformShell
      activeHref="#model-comparison"
      activeStageId="model-comparison"
      homeHref="#demand-insight"
      moduleName="Model Comparison"
      navigation={PLATFORM_STAGES}
      noteTitle="Learning evidence"
      noteSubtitle="Model Comparison · Sprint 2"
      status={status}
      variant="comparison"
    >
      {children}
    </PlatformShell>
  );
}


function LoadingView() {
  return (
    <ModelComparisonShell status="loading">
      <div className="dashboard loading-state" aria-live="polite" aria-busy="true">
        <div className="skeleton comparison-hero-skeleton" />
        <div className="skeleton comparison-table-skeleton" />
        <p>Loading validated comparison evidence…</p>
      </div>
    </ModelComparisonShell>
  );
}


function UnavailableView({ message, retry }) {
  return (
    <ModelComparisonShell status="unavailable">
      <section className="state-card" role="alert">
        <span className="state-code">503</span>
        <p className="section-kicker">Evidence unavailable</p>
        <h1>We could not load the model comparison.</h1>
        <p>{message}</p>
        <button type="button" onClick={retry}>Try again</button>
        <small>No fallback metrics or model decision are shown.</small>
      </section>
    </ModelComparisonShell>
  );
}


function CandidateTable({ candidates }) {
  return (
    <div className="comparison-table-wrap">
      <table className="comparison-table">
        <caption>Four candidates evaluated on the same chronological holdout.</caption>
        <thead>
          <tr>
            <th scope="col">Rank</th>
            <th scope="col">Candidate</th>
            <th scope="col">MAE</th>
            <th scope="col">RMSE</th>
            <th scope="col">R² context</th>
            <th scope="col">Baseline improvement</th>
          </tr>
        </thead>
        <tbody>
          {candidates.map((candidate) => (
            <tr key={candidate.model_id}>
              <td><span className="rank-chip">{String(candidate.mae_rank).padStart(2, "0")}</span></td>
              <th scope="row">
                <strong>{candidate.model_name}</strong>
                <small>{candidate.model_family.replaceAll("_", " ")}</small>
              </th>
              <td>{metricFormatter.format(candidate.mae_units)} <small>units</small></td>
              <td>{metricFormatter.format(candidate.rmse_units)} <small>units</small></td>
              <td>{metricFormatter.format(candidate.r2_contextual)}</td>
              <td>{metricFormatter.format(candidate.mae_improvement_vs_baseline_percent)}%</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}


function ConnectedView({ data }) {
  const { experiment, candidates, decision, decision_cards: cards, limitations } = data;
  return (
    <ModelComparisonShell status="connected">
      <div className="dashboard comparison-dashboard">
        <section className="comparison-hero" id="model-comparison">
          <div>
            <p className="section-kicker">Classical model review</p>
            <h1>Choose with evidence,<br /><em>not a leaderboard alone.</em></h1>
            <p>
              Four candidates share one dataset, feature contract and fixed
              chronological holdout. Metrics remain learning evidence only.
            </p>
          </div>
          <aside className="experiment-panel" aria-label="Experiment boundary">
            <span>Experiment boundary</span>
            <dl>
              <div><dt>Train</dt><dd>{experiment.train_rows} rows</dd></div>
              <div><dt>Test</dt><dd>{experiment.test_rows} rows</dd></div>
              <div><dt>Target</dt><dd>{experiment.target}</dd></div>
              <div><dt>Status</dt><dd>Learning only</dd></div>
            </dl>
          </aside>
        </section>

        <section className="selection-strip" aria-label="Current technical decision">
          <div>
            <span>Observed metric leader</span>
            <strong>{decision.measurement_leader.model_name}</strong>
            <small>MAE {metricFormatter.format(decision.measurement_leader.mae_units)} units</small>
          </div>
          <i aria-hidden="true">→</i>
          <div className="selection-strip-selected">
            <span>Selected for next integration</span>
            <strong>{decision.selected_candidate.model_name}</strong>
            <small>Within {decision.practical_equivalence_units} MAE units of the leader</small>
          </div>
        </section>

        <section className="section-block comparison-section" id="comparison-candidates">
          <div className="section-header">
            <div>
              <p className="section-kicker">Comparable evidence</p>
              <h2>One contract. Four candidates.</h2>
            </div>
            <span className="contract-pill">Contract {data.schema_version}</span>
          </div>
          <CandidateTable candidates={candidates} />
        </section>

        <section className="section-block comparison-section" id="comparison-rationale">
          <div className="section-header">
            <div>
              <p className="section-kicker">Decision rationale</p>
              <h2>Why Random Forest moves forward.</h2>
            </div>
          </div>
          <div className="rationale-grid">
            {decision.rationale.map((reason, index) => (
              <article key={reason}>
                <span>{String(index + 1).padStart(2, "0")}</span>
                <p>{reason}</p>
              </article>
            ))}
          </div>
        </section>

        <section
          className="section-block comparison-section"
          id="comparison-decisions"
          aria-labelledby="decision-cards-title"
        >
          <div className="section-header">
            <div>
              <p className="section-kicker">Decision cards</p>
              <h2 id="decision-cards-title">Read the decision from three angles.</h2>
            </div>
            <p>
              These cards arrive through the API. The browser formats their
              values but does not rank candidates or apply selection policy.
            </p>
          </div>
          <div className="decision-card-grid">
            {cards.map((card, index) => (
              <DecisionCard card={card} index={index} key={card.card_id} />
            ))}
          </div>
        </section>

        <section
          className="evidence-limit"
          id="comparison-boundary"
          aria-labelledby="evidence-limit-title"
        >
          <div>
            <p className="section-kicker">Evidence boundary</p>
            <h2 id="evidence-limit-title">Not production ready.</h2>
          </div>
          <ul>
            {limitations.map((limitation) => <li key={limitation}>{limitation}</li>)}
          </ul>
        </section>
      </div>
    </ModelComparisonShell>
  );
}


export function ModelComparisonDashboard() {
  const { status, data, error, retry } = useModelComparison();

  if (status === "loading") return <LoadingView />;
  if (status === "unavailable") {
    return <UnavailableView message={error.message} retry={retry} />;
  }
  return <ConnectedView data={data} />;
}
