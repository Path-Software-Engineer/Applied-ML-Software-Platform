import React from "react";

import {
  DEMAND_FIGURES,
  getDemandFigureUrl,
} from "../api/demandSummaryApi.js";
import { useDemandSummary } from "../hooks/useDemandSummary.js";


const numberFormatter = new Intl.NumberFormat("en-US", {
  maximumFractionDigits: 2,
});


function LogoMark() {
  return (
    <span className="logo-mark" aria-hidden="true">
      <span />
      <span />
      <span />
    </span>
  );
}


function AppShell({ children }) {
  return (
    <div className="app-shell">
      <aside className="sidebar" aria-label="Primary navigation">
        <a className="brand" href="#top" aria-label="Retail Intelligence home">
          <LogoMark />
          <span>
            <strong>Retail</strong>
            <small>Intelligence</small>
          </span>
        </a>

        <nav className="nav-list">
          <a className="nav-item active" href="#overview" aria-current="page">
            <span className="nav-index">01</span>
            Overview
          </a>
          <a className="nav-item" href="#leaders">
            <span className="nav-index">02</span>
            Leaders
          </a>
          <a className="nav-item" href="#insights">
            <span className="nav-index">03</span>
            Insight cards
          </a>
          <a className="nav-item" href="#visuals">
            <span className="nav-index">04</span>
            Visual report
          </a>
        </nav>

        <div className="sidebar-note">
          <span className="status-dot" />
          <div>
            <strong>Observed evidence</strong>
            <small>Demand Insight · Sprint 1</small>
          </div>
        </div>
      </aside>
      <main className="main-content" id="top">{children}</main>
    </div>
  );
}


function Header({ status }) {
  const isConnected = status === "connected";

  return (
    <header className="topbar">
      <div>
        <span className="eyebrow">Retail Intelligence Platform</span>
        <span className="breadcrumb">/ Demand Insight</span>
      </div>
      <div className={`topbar-status topbar-status-${status}`} role="status">
        <span className="status-dot" />
        {isConnected ? "API connected" : status === "loading" ? "Connecting" : "API unavailable"}
      </div>
    </header>
  );
}


function LoadingState() {
  return (
    <AppShell>
      <Header status="loading" />
      <div className="dashboard loading-state" aria-live="polite" aria-busy="true">
        <div className="skeleton hero-skeleton" />
        <div className="metric-grid">
          {Array.from({ length: 4 }, (_, index) => (
            <div className="skeleton metric-skeleton" key={index} />
          ))}
        </div>
        <p>Loading validated demand evidence…</p>
      </div>
    </AppShell>
  );
}


function ErrorState({ message, onRetry }) {
  return (
    <AppShell>
      <Header status="unavailable" />
      <section className="state-card" role="alert">
        <span className="state-code">503</span>
        <p className="section-kicker">Evidence unavailable</p>
        <h1>We could not load the demand summary.</h1>
        <p>{message}</p>
        <button type="button" onClick={onRetry}>Try again</button>
        <small>No fallback business values are shown when evidence is unavailable.</small>
      </section>
    </AppShell>
  );
}


function MetricCard({ label, value, detail, accent }) {
  return (
    <article className={`metric-card ${accent ? "metric-card-accent" : ""}`}>
      <span className="metric-label">{label}</span>
      <strong>{value}</strong>
      <small>{detail}</small>
    </article>
  );
}


function LeaderCard({ label, leader }) {
  return (
    <article className="leader-card">
      <div>
        <span className="leader-label">{label}</span>
        <h3>{leader.name}</h3>
      </div>
      <strong>
        {numberFormatter.format(leader.value)}
        <small>{leader.unit}</small>
      </strong>
    </article>
  );
}


function InsightCard({ card, index }) {
  return (
    <article className="insight-card">
      <div className="insight-heading">
        <span>{String(index + 1).padStart(2, "0")}</span>
        <p>{card.title}</p>
      </div>
      <h3>{card.metric}</h3>
      <p className="insight-copy">{card.insight}</p>
      <div className="recommendation">
        <span>Next lens</span>
        <p>{card.recommendation}</p>
      </div>
      <p className="limitation">{card.limitation}</p>
    </article>
  );
}


function FigureCard({ figure }) {
  return (
    <figure className="figure-card">
      <div className="figure-frame">
        <img
          src={getDemandFigureUrl(figure.figureId)}
          alt={figure.description}
          loading="lazy"
        />
      </div>
      <figcaption>
        <span>{figure.title}</span>
        <p>{figure.description}</p>
      </figcaption>
    </figure>
  );
}


function DashboardContent({ data }) {
  const { period, sales_summary: sales, baseline, leaders, insight_cards: cards } = data;
  return (
    <AppShell>
      <Header status="connected" />
      <div className="dashboard">
        <section className="hero" id="overview">
          <div className="hero-copy">
            <p className="section-kicker">Demand overview</p>
            <h1>Demand clarity,<br /><em>without the guesswork.</em></h1>
            <p>
              A concise view of observed retail performance, assembled from
              validated analytical evidence—not forecasts.
            </p>
          </div>
          <div className="period-card">
            <span>Observed window</span>
            <strong>{period.start_date}</strong>
            <i />
            <strong>{period.end_date}</strong>
            <small>{period.observed_days} trading days · {sales.sales_count} records</small>
          </div>
        </section>

        <section className="metric-grid" aria-label="Demand summary metrics">
          <MetricCard label="Units sold" value={numberFormatter.format(sales.total_units_sold)} detail="Observed demand volume" accent />
          <MetricCard label="Revenue" value={numberFormatter.format(sales.total_revenue)} detail="Observed economic value" />
          <MetricCard label="Mean baseline" value={numberFormatter.format(baseline.mean_units_prediction)} detail="Units per sale reference" />
          <MetricCard label="Baseline MAE" value={numberFormatter.format(baseline.mae)} detail="Average error in units" />
        </section>

        <section className="section-block" id="leaders">
          <div className="section-header">
            <div>
              <p className="section-kicker">Leading signals</p>
              <h2>Volume and value tell different stories.</h2>
            </div>
            <p>Leaders are reported separately to keep demand and revenue comparable, not interchangeable.</p>
          </div>
          <div className="leader-grid">
            <LeaderCard label="Top product · demand" leader={leaders.product_by_units} />
            <LeaderCard label="Top product · revenue" leader={leaders.product_by_revenue} />
            <LeaderCard label="Top day · demand" leader={leaders.date_by_units} />
            <LeaderCard label="Top day · revenue" leader={leaders.date_by_revenue} />
          </div>
        </section>

        <section className="section-block" id="insights">
          <div className="section-header">
            <div>
              <p className="section-kicker">Insight cards</p>
              <h2>Evidence with context.</h2>
            </div>
            <span className="contract-pill">Contract {data.schema_version}</span>
          </div>
          <div className="insight-grid">
            {cards.map((card, index) => (
              <InsightCard card={card} index={index} key={card.card_id} />
            ))}
          </div>
        </section>

        <section className="section-block" id="visuals">
          <div className="section-header">
            <div>
              <p className="section-kicker">Visual report</p>
              <h2>See the evidence behind the cards.</h2>
            </div>
            <p>
              Generated figures remain analytical artifacts. The dashboard
              presents them without recalculating or redefining their meaning.
            </p>
          </div>
          <div className="figure-grid">
            {DEMAND_FIGURES.map((figure) => (
              <FigureCard figure={figure} key={figure.figureId} />
            ))}
          </div>
        </section>

        <footer>
          <LogoMark />
          <p>{data.limitations[0]}</p>
          <span>Demand Insight · Sprint 1</span>
        </footer>
      </div>
    </AppShell>
  );
}


export function DemandDashboard() {
  const { status, data, error, retry } = useDemandSummary();

  if (status === "loading") return <LoadingState />;
  if (status === "error") return <ErrorState message={error.message} onRetry={retry} />;
  return <DashboardContent data={data} />;
}
