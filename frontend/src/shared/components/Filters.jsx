import { Search, X } from "lucide-react";
import { Input } from "@/components/ui/input";
import { cn } from "@/lib/utils";
import { useCategories } from "@/shared/hooks/useCategories";

export const SearchField = ({ value, onChange, placeholder, testId = "search-input" }) => (
  <div className="relative w-full">
    <Search className="pointer-events-none absolute left-3.5 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" aria-hidden />
    <Input
      type="search"
      aria-label={placeholder}
      value={value}
      onChange={(e) => onChange(e.target.value)}
      placeholder={placeholder}
      data-testid={testId}
      className="h-12 rounded-full bg-card pl-10 pr-10 text-sm"
    />
    {value && (
      <button type="button" aria-label="Clear search" onClick={() => onChange("")} data-testid={`${testId}-clear`}
        className="absolute right-3 top-1/2 -translate-y-1/2 rounded-full p-1 text-muted-foreground hover:text-foreground">
        <X className="h-4 w-4" />
      </button>
    )}
  </div>
);

export const CategoryChips = ({ value, onChange }) => {
  const cats = useCategories();
  const all = [{ slug: "", label: "All" }, ...cats];
  return (
    <div className="-mx-4 flex gap-2 overflow-x-auto px-4 pb-1 scrollbar-none sm:mx-0 sm:flex-wrap sm:px-0" role="group" aria-label="Filter by category">
      {all.map((c) => (
        <button
          key={c.slug || "all"}
          type="button"
          aria-pressed={value === c.slug}
          onClick={() => onChange(c.slug)}
          data-testid={`category-chip-${c.slug || "all"}`}
          className={cn(
            "whitespace-nowrap rounded-full border px-4 py-2 text-xs font-semibold transition-colors duration-200",
            value === c.slug ? "border-primary bg-primary text-white" : "border-border bg-card text-muted-foreground hover:border-primary/60 hover:text-foreground"
          )}
        >
          {c.label}
        </button>
      ))}
    </div>
  );
};
