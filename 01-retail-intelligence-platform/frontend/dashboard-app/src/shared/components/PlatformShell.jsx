import React from "react";


export function LogoMark({ variant = "demand" }) {
  const variantClass = variant === "comparison" ? " comparison-logo" : "";
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

  return (
    <div className={`app-shell${comparison ? " comparison-shell" : ""}`}>
      <aside
        className={`sidebar${comparison ? " comparison-sidebar" : ""}`}
        aria-label="Primary navigation"
      >
        <a className="brand" href={homeHref} aria-label="Retail Intelligence home">
          <LogoMark variant={variant} />
          <span>
            <strong>Retail</strong>
            <small>Intelligence</small>
          </span>
        </a>
        <nav className="nav-list">
          {navigation.map((item, index) => {
            const active = item.href === activeHref;
            return (
              <a
                className={`nav-item${active ? " active" : ""}`}
                href={item.href}
                aria-current={active ? "page" : undefined}
                key={item.href}
              >
                <span className="nav-index">{String(index + 1).padStart(2, "0")}</span>
                {item.label}
              </a>
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
