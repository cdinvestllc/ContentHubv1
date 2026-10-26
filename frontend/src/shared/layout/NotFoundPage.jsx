import { NotFoundPageInner } from "@/shared/layout/ModeHome";

export default function NotFoundPage({ inApp = false }) {
  if (inApp) return <NotFoundPageInner inApp />;
  return <div className="mx-auto max-w-3xl px-6"><NotFoundPageInner /></div>;
}
