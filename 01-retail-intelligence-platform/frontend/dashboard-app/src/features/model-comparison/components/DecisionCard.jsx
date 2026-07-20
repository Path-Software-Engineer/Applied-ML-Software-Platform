import React from "react";

import { createDecisionCardView } from "../presentation/decisionCardViewModel.js";


const metricFormatter = new Intl.NumberFormat("en-US", {
  maximumFractionDigits: 4,
});


export function DecisionCard({ card, index }) {
  const view = createDecisionCardView(card);
  const titleId = `decision-card-${view.cardId}-title`;
  const limitationId = `decision-card-${view.cardId}-limitation`;

  return (
    <article
      className={`decision-card decision-card-${view.cardId}`}
      aria-labelledby={titleId}
      aria-describedby={limitationId}
    >
      <header>
        <span className="decision-card-index">{String(index + 1).padStart(2, "0")}</span>
        <span className="decision-card-status" role="status">
          {view.statusLabel}
        </span>
      </header>
      <p className="decision-card-eyebrow">{view.eyebrow}</p>
      <h3 id={titleId}>{view.title}</h3>
      <div className="decision-card-metric">
        <span>{view.metricLabel}</span>
        <data value={view.metricValue}>{metricFormatter.format(view.metricValue)}</data>
        <small>{view.metricUnit}</small>
      </div>
      <p className="decision-card-summary">{view.summary}</p>
      <ul aria-label={`Reasons for ${view.title}`}>
        {view.reasons.map((reason) => <li key={reason}>{reason}</li>)}
      </ul>
      <p className="decision-card-limitation" id={limitationId}>
        <strong>Limit</strong>
        {view.limitation}
      </p>
    </article>
  );
}
