import { useCallback, useEffect, useState } from "react";
import { errorMessage } from "@/shared/api/client";

export function useResource(loader, deps) {
  const [state, setState] = useState({ data: null, loading: true, error: null });

  // eslint-disable-next-line react-hooks/exhaustive-deps
  const load = useCallback(async () => {
    setState((s) => ({ ...s, loading: true, error: null }));
    try {
      setState({ data: await loader(), loading: false, error: null });
    } catch (e) {
      setState({ data: null, loading: false, error: errorMessage(e) });
    }
  }, deps);

  useEffect(() => {
    load();
  }, [load]);

  const setData = useCallback((fn) => setState((s) => ({ ...s, data: typeof fn === "function" ? fn(s.data) : fn })), []);
  return { ...state, reload: load, setData };
}

export function useDebounced(value, delay = 300) {
  const [debounced, setDebounced] = useState(value);
  useEffect(() => {
    const t = setTimeout(() => setDebounced(value), delay);
    return () => clearTimeout(t);
  }, [value, delay]);
  return debounced;
}
