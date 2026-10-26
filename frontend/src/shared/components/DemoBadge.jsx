import { FlaskConical } from "lucide-react";
import { cn } from "@/lib/utils";

const TONES = {
  gold: "border-gold/40 bg-gold/10 text-gold-ink",
  purple: "border-primary/40 bg-primary/10 text-brand-ink",
  orange: "border-warning/40 bg-warning/10 text-warning-ink",
};

export const DemoBadge = ({ children = "Demo data", tone = "gold", className, testId = "demo-badge" }) => (
  <span
    data-testid={testId}
    className={cn("inline-flex items-center gap-1 whitespace-nowrap rounded-full border px-2 py-0.5 font-mono text-[10px] font-medium uppercase tracking-[0.14em]", TONES[tone], className)}
  >
    <FlaskConical className="h-3 w-3" aria-hidden />
    {children}
  </span>
);
