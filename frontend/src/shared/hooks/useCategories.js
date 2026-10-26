import { useEffect, useState } from "react";
import { api, data } from "@/shared/api/client";

let cache = null;

/** @returns {import('../types/models').Category[]} */
export function useCategories() {
  const [cats, setCats] = useState(cache || []);
  useEffect(() => {
    if (cache) {
      return;
    }
    data(api.get("/categories")).then((c) => { cache = c; setCats(c); }).catch(() => {});
  }, []);
  return cats;
}

export const categoryLabel = (cats, slug) => cats.find((c) => c.slug === slug)?.label || slug;
