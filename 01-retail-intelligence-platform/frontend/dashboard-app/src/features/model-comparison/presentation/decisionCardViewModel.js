const STATUS_LABELS = {
  measurement_leader_not_selected: "Metric leader",
  selected_for_next_integration: "Integration candidate",
  not_production_ready: "Evidence boundary",
};


export function createDecisionCardView(card) {
  return {
    cardId: card.card_id,
    eyebrow: card.eyebrow,
    title: card.title,
    status: card.status,
    statusLabel: STATUS_LABELS[card.status] ?? card.status,
    modelId: card.model_id,
    metricLabel: card.primary_metric.label,
    metricValue: card.primary_metric.value,
    metricUnit: card.primary_metric.unit,
    metricDirection: card.primary_metric.direction,
    summary: card.summary,
    reasons: card.reasons,
    limitation: card.limitation,
  };
}
