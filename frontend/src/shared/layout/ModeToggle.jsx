import { useNavigate } from "react-router-dom";
import { toast } from "sonner";
import { cn } from "@/lib/utils";
import { useSession } from "@/shared/session/SessionProvider";
import { errorMessage } from "@/shared/api/client";
import { NAV } from "@/shared/layout/navConfig";

const MODES = [
  { value: "hiring", label: "Hiring" },
  { value: "working", label: "Working" },
];

export const ModeToggle = ({ className }) => {
  const { user, setMode } = useSession();
  const navigate = useNavigate();

  const change = async (mode) => {
    if (mode === user.mode) return;
    try {
      await setMode(mode);
      navigate(NAV[mode][0].to);
      toast.success(mode === "hiring" ? "Hiring mode: find and book talent" : "Working mode: find gigs and manage tasks");
    } catch (e) {
      toast.error(errorMessage(e));
    }
  };

  return (
    <div role="radiogroup" aria-label="App mode" className={cn("relative grid grid-cols-2 rounded-full border border-border bg-muted p-1", className)}>
      <span
        aria-hidden
        className={cn(
          "absolute inset-y-1 left-1 w-[calc(50%-4px)] rounded-full transition-transform duration-300",
          user.mode === "hiring" ? "translate-x-0 bg-primary" : "translate-x-full bg-success"
        )}
      />
      {MODES.map((m) => (
        <button
          key={m.value}
          role="radio"
          aria-checked={user.mode === m.value}
          onClick={() => change(m.value)}
          data-testid={`mode-toggle-${m.value}`}
          className={cn(
            "relative z-10 rounded-full px-4 py-1.5 text-xs font-bold transition-colors duration-200",
            user.mode === m.value ? (m.value === "hiring" ? "text-white" : "text-obsidian") : "text-muted-foreground hover:text-foreground"
          )}
        >
          {m.label}
        </button>
      ))}
    </div>
  );
};
