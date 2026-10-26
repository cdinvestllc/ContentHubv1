export const money = (n) => `$${Number(n).toLocaleString("en-US")}`;

export const budgetLabel = (j) => {
  const suffix = j.budget_type === "fixed" ? "" : j.budget_type === "day" ? " / day" : " / item";
  return `${money(j.budget_min)}–${money(j.budget_max)}${suffix}`;
};

export const shortDate = (iso) => new Date(iso).toLocaleDateString("en-US", { month: "short", day: "numeric" });

export const timeAgo = (iso) => {
  const s = (Date.now() - new Date(iso).getTime()) / 1000;
  if (s < 60) return "just now";
  if (s < 3600) return `${Math.floor(s / 60)}m ago`;
  if (s < 86400) return `${Math.floor(s / 3600)}h ago`;
  return `${Math.floor(s / 86400)}d ago`;
};

export const daysLeft = (iso) => Math.max(0, Math.ceil((new Date(iso).getTime() - Date.now()) / 86400000));
