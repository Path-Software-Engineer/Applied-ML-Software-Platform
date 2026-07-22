export const PLATFORM_STAGES = Object.freeze([
  Object.freeze({
    id: "demand-insight",
    href: "#demand-insight",
    label: "Demand insight",
    sections: Object.freeze([
      Object.freeze({ href: "#overview", label: "Overview" }),
      Object.freeze({ href: "#leaders", label: "Leaders" }),
      Object.freeze({ href: "#insights", label: "Insight cards" }),
      Object.freeze({ href: "#visuals", label: "Visual report" }),
    ]),
  }),
  Object.freeze({
    id: "model-comparison",
    href: "#model-comparison",
    label: "Model comparison",
    sections: Object.freeze([
      Object.freeze({ href: "#model-comparison", label: "Overview" }),
      Object.freeze({ href: "#comparison-candidates", label: "Candidates" }),
      Object.freeze({ href: "#comparison-rationale", label: "Decision rationale" }),
      Object.freeze({ href: "#comparison-decisions", label: "Decision cards" }),
      Object.freeze({ href: "#comparison-boundary", label: "Evidence boundary" }),
    ]),
  }),
]);


const modelComparisonHashes = new Set(
  PLATFORM_STAGES.find((stage) => stage.id === "model-comparison")
    .sections
    .map((section) => section.href),
);


export function resolvePlatformView(hash) {
  return modelComparisonHashes.has(hash)
    ? "model-comparison"
    : "demand-insight";
}
