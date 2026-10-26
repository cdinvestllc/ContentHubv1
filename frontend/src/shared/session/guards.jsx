import { Navigate, useLocation } from "react-router-dom";
import { useSession } from "@/shared/session/SessionProvider";
import { FullPageLoader } from "@/shared/components/StateViews";

// UX guards only. Every API route re-checks session, consent and capability on the server.
export function RequireSession({ children }) {
  const { status } = useSession();
  const location = useLocation();
  if (status === "loading") return <FullPageLoader />;
  if (status === "anon") return <Navigate to="/auth" replace state={{ from: location.pathname }} />;
  return children;
}

export function RequireConsent({ children }) {
  const { status, user } = useSession();
  if (status === "loading") return <FullPageLoader />;
  if (status === "anon") return <Navigate to="/auth" replace />;
  if (!user.consent) return <Navigate to="/consent" replace />;
  return children;
}
