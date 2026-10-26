import { useState } from "react";
import { Link, NavLink, Outlet, useNavigate } from "react-router-dom";
import { Coins, LogOut, Plus, Settings } from "lucide-react";
import { Button } from "@/components/ui/button";
import {
  DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuLabel, DropdownMenuSeparator, DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { cn } from "@/lib/utils";
import { useSession } from "@/shared/session/SessionProvider";
import { Logo } from "@/shared/components/Brand";
import { DemoBadge } from "@/shared/components/DemoBadge";
import { ThemeToggle } from "@/shared/theme/ThemeToggle";
import { ModeToggle } from "@/shared/layout/ModeToggle";
import { NAV, SECONDARY_NAV } from "@/shared/layout/navConfig";
import { CreateJobDialog } from "@/features/jobs/CreateJobDialog";

const navClass = ({ isActive }) =>
  cn(
    "flex items-center gap-3 rounded-xl px-3 py-2.5 text-sm font-medium transition-colors duration-200",
    isActive ? "bg-primary/15 text-brand-ink" : "text-muted-foreground hover:bg-accent hover:text-foreground"
  );

const Sidebar = () => {
  const { user } = useSession();
  const primary = NAV[user.mode];
  const secondary = SECONDARY_NAV.filter((s) => !primary.some((p) => p.to === s.to));
  return (
    <aside className="sticky top-0 hidden h-screen w-64 shrink-0 flex-col border-r border-border bg-card/40 p-5 md:flex" data-testid="desktop-sidebar">
      <Logo to="/app" />
      <ModeToggle className="mt-6" />
      <nav aria-label="Main" className="mt-6 space-y-1">
        {primary.map(({ to, label, icon: Icon, id }) => (
          <NavLink key={id} to={to} className={navClass} data-testid={`sidebar-nav-${id}`}><Icon className="h-4 w-4" />{label}</NavLink>
        ))}
      </nav>
      <div className="mt-6 border-t border-border pt-4 font-mono text-[10px] uppercase tracking-[0.2em] text-muted-foreground">More</div>
      <nav aria-label="Secondary" className="mt-2 space-y-1">
        {secondary.map(({ to, label, icon: Icon, id }) => (
          <NavLink key={id} to={to} className={navClass} data-testid={`sidebar-nav-${id}`}><Icon className="h-4 w-4" />{label}</NavLink>
        ))}
      </nav>
      <div className="mt-auto rounded-xl border border-gold/30 bg-gold/5 p-3 text-xs text-muted-foreground">
        <DemoBadge>Prototype</DemoBadge>
        <p className="mt-2">All people, brands and messages are sample data. No payments or emails are sent.</p>
      </div>
    </aside>
  );
};

const UserMenu = () => {
  const { user, signOut } = useSession();
  const navigate = useNavigate();
  const out = async () => { await signOut(); navigate("/"); };
  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <button aria-label="Account menu" data-testid="user-menu-button" className="grid h-9 w-9 place-items-center rounded-full bg-primary font-display text-sm font-bold text-white">
          {user.display_name.slice(0, 1).toUpperCase()}
        </button>
      </DropdownMenuTrigger>
      <DropdownMenuContent align="end" className="w-56">
        <DropdownMenuLabel className="truncate">{user.display_name}<div className="truncate text-xs font-normal text-muted-foreground">{user.email}</div></DropdownMenuLabel>
        <DropdownMenuSeparator />
        <DropdownMenuItem onClick={() => navigate("/app/wallet")} data-testid="user-menu-wallet"><Coins className="mr-2 h-4 w-4" /> Token wallet</DropdownMenuItem>
        <DropdownMenuItem onClick={() => navigate("/app/settings")} data-testid="user-menu-settings"><Settings className="mr-2 h-4 w-4" /> Privacy & settings</DropdownMenuItem>
        <DropdownMenuSeparator />
        <DropdownMenuItem onClick={out} data-testid="user-menu-sign-out"><LogOut className="mr-2 h-4 w-4" /> Sign out</DropdownMenuItem>
      </DropdownMenuContent>
    </DropdownMenu>
  );
};

const TopBar = ({ onCreateJob }) => {
  const { user } = useSession();
  return (
    <header className="glass sticky top-0 z-30 flex items-center gap-2 border-b border-border px-4 py-3 sm:px-6">
      <div className="md:hidden"><Logo to="/app" compact /></div>
      <ModeToggle className="md:hidden" />
      <div className="ml-auto flex items-center gap-1.5 sm:gap-2">
        {user.mode === "hiring" && (
          <Button size="sm" onClick={onCreateJob} data-testid="topbar-create-job-button" className="hidden rounded-full sm:inline-flex">
            <Plus className="mr-1 h-4 w-4" /> Post a job
          </Button>
        )}
        <Link to="/app/wallet" data-testid="topbar-token-balance" aria-label={`${user.token_balance} Tokens`}
          className="flex items-center gap-1.5 rounded-full border border-gold/40 bg-gold/10 px-3 py-1.5 font-mono text-xs font-semibold text-gold-ink transition-colors hover:bg-gold/20">
          <Coins className="h-3.5 w-3.5" /> {user.token_balance}
        </Link>
        <ThemeToggle />
        <UserMenu />
      </div>
    </header>
  );
};

const BottomNav = () => {
  const { user } = useSession();
  return (
    <nav aria-label="Main" data-testid="mobile-bottom-nav" className="glass pb-safe fixed inset-x-0 bottom-0 z-40 grid grid-cols-4 border-t border-border px-2 pt-2 md:hidden">
      {NAV[user.mode].map(({ to, label, icon: Icon, id }) => (
        <NavLink key={id} to={to} data-testid={`bottom-tab-${id}`}
          className={({ isActive }) => cn("flex flex-col items-center gap-1 rounded-xl py-1.5 text-[11px] font-semibold transition-colors", isActive ? "text-brand-ink" : "text-muted-foreground")}>
          <Icon className="h-5 w-5" />{label}
        </NavLink>
      ))}
    </nav>
  );
};

export default function AppShell() {
  const [createOpen, setCreateOpen] = useState(false);
  const navigate = useNavigate();
  return (
    <div className="flex min-h-screen">
      <Sidebar />
      <div className="flex min-w-0 flex-1 flex-col">
        <TopBar onCreateJob={() => setCreateOpen(true)} />
        <main className="mx-auto w-full max-w-6xl flex-1 px-4 pb-28 pt-6 sm:px-6 md:pb-12 lg:px-10">
          <Outlet context={{ openCreateJob: () => setCreateOpen(true) }} />
        </main>
      </div>
      <BottomNav />
      <CreateJobDialog open={createOpen} onOpenChange={setCreateOpen} onCreated={(job) => navigate(`/app/jobs/${job.id}`)} />
    </div>
  );
}
