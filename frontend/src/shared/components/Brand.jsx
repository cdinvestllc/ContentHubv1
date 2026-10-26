import { Link } from "react-router-dom";
import { Layers } from "lucide-react";

export const Logo = ({ to = "/", compact = false }) => (
  <Link to={to} data-testid="brand-logo-link" className="flex items-center gap-2 font-display text-base font-bold tracking-tight">
    <span className="grid h-8 w-8 place-items-center rounded-lg bg-primary text-white shadow-[0_0_24px_-4px_hsl(var(--primary))]">
      <Layers className="h-4 w-4" aria-hidden />
    </span>
    {!compact && <span>Creator<span className="text-gold-ink">Hub</span></span>}
  </Link>
);

export const PageHeader = ({ eyebrow, title, description, actions }) => (
  <header className="mb-6 flex flex-col gap-4 sm:mb-8 sm:flex-row sm:items-end sm:justify-between">
    <div className="space-y-2">
      {eyebrow && <div className="font-mono text-[11px] uppercase tracking-[0.2em] text-muted-foreground">{eyebrow}</div>}
      <h1 className="text-2xl font-bold tracking-tight sm:text-3xl" data-testid="page-title">{title}</h1>
      {description && <p className="max-w-xl text-sm text-muted-foreground">{description}</p>}
    </div>
    {actions && <div className="flex flex-wrap items-center gap-2">{actions}</div>}
  </header>
);
