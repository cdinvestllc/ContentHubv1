import { createContext, useCallback, useContext, useEffect, useMemo, useState } from "react";
import { sessionStore } from "@/shared/api/client";
import { authRepository } from "@/features/auth/authRepository";

const SessionContext = createContext(null);

export function SessionProvider({ children }) {
  const [user, setUser] = useState(null);
  const [status, setStatus] = useState(sessionStore.get() ? "loading" : "anon");

  useEffect(() => {
    if (!sessionStore.get()) {
      return;
    }
    authRepository.me()
      .then((u) => { setUser(u); setStatus("ready"); })
      .catch(() => { sessionStore.clear(); setStatus("anon"); });
  }, []);

  const signIn = useCallback(async (payload) => {
    const res = await authRepository.demoSession(payload);
    sessionStore.set(res.token);
    setUser(res.user);
    setStatus("ready");
    return res.user;
  }, []);

  const acceptConsent = useCallback(async (version) => {
    const u = await authRepository.consent(version);
    setUser(u);
    return u;
  }, []);

  const setMode = useCallback(async (mode) => {
    setUser(await authRepository.setMode(mode));
  }, []);

  const signOut = useCallback(async () => {
    try {
      await authRepository.signOut();
    } finally {
      sessionStore.clear();
      setUser(null);
      setStatus("anon");
    }
  }, []);

  // Only ever called with a balance returned by the server.
  const syncBalance = useCallback((balance) => setUser((u) => ({ ...u, token_balance: balance })), []);

  const value = useMemo(
    () => ({ user, status, signIn, acceptConsent, setMode, signOut, syncBalance }),
    [user, status, signIn, acceptConsent, setMode, signOut, syncBalance]
  );
  return <SessionContext.Provider value={value}>{children}</SessionContext.Provider>;
}

export const useSession = () => useContext(SessionContext);
