import { Link, Navigate } from "react-router-dom";
import { Compass } from "lucide-react";
import { Button } from "@/components/ui/button";
import { useSession } from "@/shared/session/SessionProvider";
import { NAV } from "@/shared/layout/navConfig";

export default function ModeHome() {
  const { user } = useSession();
  return <Navigate to={NAV[user.mode][0].to} replace />;
}

export function NotFoundPageInner({ inApp }) {
  return (
    <div className="flex flex-col items-start gap-4 py-16" data-testid="not-found-page">
      <span className="font-mono text-xs uppercase tracking-[0.2em] text-muted-foreground">404</span>
      <h1 className="text-3xl font-bold">This page isn't in the prototype</h1>
      <Button asChild data-testid="not-found-home-link"><Link to={inApp ? "/app" : "/"}><Compass className="mr-2 h-4 w-4" />Back to safety</Link></Button>
    </div>
  );
}
