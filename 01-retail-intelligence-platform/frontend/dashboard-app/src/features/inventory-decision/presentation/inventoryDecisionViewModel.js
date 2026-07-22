const integerFormatter = new Intl.NumberFormat("en-US", { maximumFractionDigits: 0 });
const decimalFormatter = new Intl.NumberFormat("en-US", {
  minimumFractionDigits: 1,
  maximumFractionDigits: 2,
});

export function formatCoverage(value) {
  return value === null ? "No observed coverage" : `${decimalFormatter.format(value)} days`;
}

export function formatAction(code) {
  return {
    replenish_now: "Replenish now",
    replenish_soon: "Replenish soon",
    review: "Review conditions",
    monitor: "Monitor",
  }[code] ?? "Review";
}

export function toRecommendationCardViewModel(card) {
  return {
    id: card.card_id,
    rank: String(card.priority_rank).padStart(2, "0"),
    productName: card.product.product_name,
    productId: card.product.product_id,
    riskLabel: card.risk.label,
    riskScore: decimalFormatter.format(card.risk.score),
    actionLabel: formatAction(card.action.code),
    quantityLabel: `${integerFormatter.format(card.action.suggested_quantity_units)} units`,
    stockLabel: `${integerFormatter.format(card.evidence.current_stock_units)} units`,
    coverageLabel: formatCoverage(card.evidence.coverage_days),
    reason: card.reason,
    limitation: card.limitation,
  };
}
