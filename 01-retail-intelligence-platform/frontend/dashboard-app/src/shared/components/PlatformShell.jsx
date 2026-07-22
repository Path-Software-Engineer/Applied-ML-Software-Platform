import React from "react";


export function LogoMark({ variant = "demand" }) {
  const variantClass = variant === "comparison"
    ? " comparison-logo"
    : variant === "inventory"
      ? " inventory-logo"
      : "";
  return (
    <span className={`logo-mark${variantClass}`} aria-hidden="true">
      <span />
      <span />
      <span />
    </span>
  );
}


function PlatformHeader({ moduleName, status }) {
  const statusLabel = status === "connected"
    ? "API connected"
    : status === "loading"
      ? "Connecting"
      : "API unavailable";

  return (
    <header className="topbar">
      <div>
        <span className="eyebrow">Retail Intelligence Platform</span>
        <span className="breadcrumb">/ {moduleName}</span>
      </div>
      <div className={`topbar-status topbar-status-${status}`} role="status">
        <span className="status-dot" />
        {statusLabel}
      </div>
    </header>
  );
}


export function PlatformShell({
  activeHref,
  activeStageId,
  children,
  homeHref,
  mainId,
  moduleName,
  navigation,
  noteSubtitle,
  noteTitle,
  status,
  variant = "demand",
}) {
  const comparison = variant === "comparison";
  const inventory = variant === "inventory";
  const shellClass = comparison
    ? " comparison-shell"
    : inventory
      ? " inventory-shell"
      : "";
  const sidebarClass = comparison
    ? " comparison-sidebar"
    : inventory
      ? " inventory-sidebar"
      : "";
  const [expandedStageId, setExpandedStageId] = React.useState(activeStageId);
  const [currentHref, setCurrentHref] = React.useState(() => (
    window.location.hash || activeHref
  ));

  React.useEffect(() => {
    setExpandedStageId(activeStageId);
  }, [activeStageId]);

  React.useEffect(() => {
    const updateCurrentHref = () => setCurrentHref(window.location.hash || activeHref);
    window.addEventListener("hashchange", updateCurrentHref);
    return () => window.removeEventListener("hashchange", updateCurrentHref);
  }, [activeHref]);

  const selectStage = (stage) => {
    if (stage.id !== activeStageId) {
      setExpandedStageId(stage.id);
      window.location.hash = stage.href;
      return;
    }
    setExpandedStageId(expandedStageId === stage.id ? null : stage.id);
  };

  return (
    <div className={`app-shell${shellClass}`}>
      <aside
        className={`sidebar${sidebarClass}`}
        aria-label="Primary navigation"
      >
        <a className="brand" href={homeHref} aria-label="Retail Intelligence home">
          <LogoMark variant={variant} />
          <span>
            <strong>Retail</strong>
            <small>Intelligence</small>
          </span>
        </a>
        <nav className="nav-list" aria-label="Platform stages">
          {navigation.map((stage, stageIndex) => {
            const active = stage.id === activeStageId;
            const expanded = stage.id === expandedStageId;
            const panelId = `stage-panel-${stage.id}`;
            return (
              <section
                className={`nav-stage${active ? " active" : ""}`}
                key={stage.id}
              >
                <button
                  className="nav-stage-trigger"
                  type="button"
                  aria-controls={panelId}
                  aria-current={active ? "page" : undefined}
                  aria-expanded={expanded}
                  onClick={() => selectStage(stage)}
                >
                  <span className="nav-stage-index">
                    {String(stageIndex + 1).padStart(2, "0")}
                  </span>
                  <span>{stage.label}</span>
                  <span className="nav-stage-chevron" aria-hidden="true" />
                </button>
                {expanded && (
                  <div className="nav-stage-panel" id={panelId}>
                    {stage.sections.map((section, sectionIndex) => {
                      const sectionActive = (
                        active
                        && (currentHref === section.href
                          || (currentHref === stage.href && section.href === activeHref))
                      );
                      return (
                        <a
                          className={`nav-subitem${sectionActive ? " active" : ""}`}
                          href={section.href}
                          aria-current={sectionActive ? "location" : undefined}
                          key={section.href}
                        >
                          <span className="nav-subindex">
                            {String(sectionIndex + 1).padStart(2, "0")}
                          </span>
                          {section.label}
                        </a>
                      );
                    })}
                  </div>
                )}
              </section>
            );
          })}
        </nav>
        <div className="sidebar-note">
          <span className="status-dot" />
          <div>
            <strong>{noteTitle}</strong>
            <small>{noteSubtitle}</small>
          </div>
        </div>
      </aside>
      <main className="main-content" id={mainId}>
        <PlatformHeader moduleName={moduleName} status={status} />
        {children}
      </main>
    </div>
  );
}
