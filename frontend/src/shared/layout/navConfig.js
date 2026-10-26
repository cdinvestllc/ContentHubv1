import { Bookmark, Briefcase, Coins, Compass, Inbox, KanbanSquare, ShieldCheck, Flame } from "lucide-react";

// Four mobile tabs per mode. The mode is a UI preference; server capabilities gate actions.
export const NAV = {
  hiring: [
    { to: "/app/discover", label: "Discover", icon: Compass, id: "discover" },
    { to: "/app/shortlist", label: "Shortlist", icon: Bookmark, id: "shortlist" },
    { to: "/app/my-jobs", label: "My Jobs", icon: Briefcase, id: "my-jobs" },
    { to: "/app/inbox", label: "Inbox", icon: Inbox, id: "inbox" },
  ],
  working: [
    { to: "/app/jobs", label: "Job Board", icon: Flame, id: "jobs" },
    { to: "/app/workspace", label: "Workspace", icon: KanbanSquare, id: "workspace" },
    { to: "/app/inbox", label: "Inbox", icon: Inbox, id: "inbox" },
    { to: "/app/wallet", label: "Tokens", icon: Coins, id: "wallet" },
  ],
};

export const SECONDARY_NAV = [
  { to: "/app/workspace", label: "Workspace", icon: KanbanSquare, id: "workspace" },
  { to: "/app/wallet", label: "Token wallet", icon: Coins, id: "wallet" },
  { to: "/app/settings", label: "Privacy & settings", icon: ShieldCheck, id: "settings" },
];
