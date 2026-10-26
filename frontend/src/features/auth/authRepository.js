import { api, data } from "@/shared/api/client";

// Repository boundary: swap these calls for a real auth provider later without touching UI.
export const authRepository = {
  /** @returns {Promise<{token: string, user: import('../../shared/types/models').SessionUser}>} */
  demoSession: (payload) => data(api.post("/auth/demo-session", payload)),
  me: () => data(api.get("/auth/me")),
  legal: () => data(api.get("/auth/legal")),
  consent: (terms_version) =>
    data(api.post("/auth/consent", { accept_terms: true, accept_guidelines: true, terms_version })),
  setMode: (mode) => data(api.put("/auth/me/mode", { mode })),
  signOut: () => data(api.post("/auth/sign-out")),
};
