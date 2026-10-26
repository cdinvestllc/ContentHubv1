// Typed contracts shared by repositories and the FastAPI backend (backend/features/*.py).
// The app is JavaScript today; these interfaces document the shapes and are referenced via JSDoc.

export type Mode = "hiring" | "working";
export type Capability = "hire" | "work";

export interface Consent { terms_version: string; guidelines_version: string; accepted_at: string; }

/** Server-owned. Capabilities and token_balance are never accepted from the client. */
export interface SessionUser {
  id: string; email: string; display_name: string; capabilities: Capability[];
  mode: Mode; consent: Consent | null; token_balance: number; is_demo: true;
}

export interface Category { slug: string; label: string; }

export interface PortfolioItem {
  id: string; title: string; client: string; cover: string; views: string;
  duration: string; format: "9:16"; tools: string[];
}

export interface Talent {
  id: string; name: string; handle: string; avatar: string; headline: string; category: string;
  skills: string[]; location: string; timezone: string; day_rate: number; project_rate_from: number;
  rating: number; reviews_count: number; completed_projects: number; response_time: string;
  availability: string; verified: boolean; languages: string[]; bio: string;
  portfolio: PortfolioItem[];
  services: { name: string; price: number; turnaround: string }[];
  reviews: { author: string; company: string; rating: number; text: string }[];
  is_shortlisted: boolean; contact_unlocked: boolean;
  /** Only present after a server-verified Token unlock. */
  contact?: { email: string; calendar: string } | null;
}

export interface Job {
  id: string; title: string; brand: string; category: string; budget_min: number; budget_max: number;
  budget_type: "fixed" | "day" | "per item"; deadline: string; location: string; urgency: "hot" | "standard";
  boosted: boolean; description: string; deliverables: string[]; skills: string[]; posted_at: string;
  applicants_count: number; is_owner: boolean; has_applied: boolean; is_demo?: boolean;
}

export interface Thread { id: string; counterpart: string; avatar: string | null; subject: string; unread: number; updated_at: string; }
export interface Message { id: string; thread_id: string; sender: "me" | "them"; body: string; created_at: string; simulated?: boolean; }

export type TaskStatus = "todo" | "in_progress" | "review" | "done";
export interface Task { id: string; project: string; title: string; status: TaskStatus; due: string; }

export interface LedgerEntry { id: string; amount: number; kind: "grant" | "spend" | "topup"; label: string; created_at: string; }
export interface Wallet {
  balance: number; ledger: LedgerEntry[];
  bundles: { id: string; label: string; tokens: number; display_price: string }[];
  prices: { unlock_contact: number; boost_job: number };
}

export interface PrivacySettings {
  public_profile: boolean; show_rates: boolean; allow_direct_messages: boolean;
  incognito_browsing: boolean; show_in_search: boolean;
}
