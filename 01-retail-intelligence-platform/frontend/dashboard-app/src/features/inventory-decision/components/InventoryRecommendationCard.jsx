import React from "react";

import { toRecommendationCardViewModel } from "../presentation/inventoryDecisionViewModel.js";

export function InventoryRecommendationCard({ card }) {
  const view = toRecommendationCardViewModel(card);
  return (
    <article className={`inventory-card risk-${view.riskLabel}`}>
      <header>
        <span>{view.rank}</span>
        <span className="risk-pill">{view.riskLabel}</span>
      </header>
      <div>
        <small>{view.productId}</small>
        <h3>{view.productName}</h3>
      </div>
      <dl>
        <div><dt>Stock</dt><dd>{view.stockLabel}</dd></div>
        <div><dt>Coverage</dt><dd>{view.coverageLabel}</dd></div>
        <div><dt>Priority index</dt><dd>{view.riskScore} / 100</dd></div>
      </dl>
      <div className="inventory-card-action">
        <span>{view.actionLabel}</span>
        <strong>{view.quantityLabel}</strong>
      </div>
      <p>{view.reason}</p>
      <small className="inventory-card-limit">{view.limitation}</small>
    </article>
  );
}
