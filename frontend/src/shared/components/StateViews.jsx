import { AlertTriangle, Inbox, Loader2, RotateCw } from "lucide-react";
import { Skeleton } from "@/components/ui/skeleton";
import { Button } from "@/components/ui/button";

export const LoadingGrid = ({ count = 8, variant = "portrait", testId = "loading-state" }) => (
  <div
    data-testid={testId}
    aria-busy="true"
    className={variant === "portrait" ? "grid grid-cols-2 gap-3 sm:grid-cols-3 xl:grid-cols-4" : "space-y-3"}
  >
    <span className="sr-only" role="status">Loading…</span>
    {Array.from({ length: count }).map((_, i) => (
      <Skeleton key={i} className={variant === "portrait" ? "aspect-[9/16] rounded-2xl" : "h-28 rounded-2xl"} />
    ))}
  </div>
);

export const EmptyState = ({ icon: Icon = Inbox, title, body, action, testId = "empty-state" }) => (
  <div data-testid={testId} className="flex flex-col items-start gap-3 rounded-2xl border border-dashed border-border p-8 sm:p-10">
    <span className="grid h-11 w-11 place-items-center rounded-xl bg-accent text-brand-ink"><Icon className="h-5 w-5" /></span>
    <h3 className="text-lg font-semibold">{title}</h3>
    {body && <p className="max-w-md text-sm text-muted-foreground">{body}</p>}
    {action}
  </div>
);

export const ErrorState = ({ message, onRetry, testId = "error-state" }) => (
  <div role="alert" data-testid={testId} className="flex flex-col items-start gap-3 rounded-2xl border border-destructive/40 bg-destructive/5 p-6">
    <div className="flex items-center gap-2 font-semibold text-destructive"><AlertTriangle className="h-4 w-4" /> Couldn't load this</div>
    <p className="text-sm text-muted-foreground">{message}</p>
    {onRetry && (
      <Button variant="outline" size="sm" onClick={onRetry} data-testid={`${testId}-retry-button`}>
        <RotateCw className="mr-2 h-3.5 w-3.5" /> Try again
      </Button>
    )}
  </div>
);

export const FullPageLoader = () => (
  <div className="grid min-h-screen place-items-center" data-testid="full-page-loader" role="status">
    <Loader2 className="h-6 w-6 animate-spin text-brand-ink" />
    <span className="sr-only">Loading</span>
  </div>
);
