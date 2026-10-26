import axios from "axios";

const TOKEN_KEY = "crh_demo_session";

// Demo-only: opaque session token in localStorage. Production should use an httpOnly, Secure, SameSite cookie.
export const sessionStore = {
  get: () => localStorage.getItem(TOKEN_KEY),
  set: (token) => localStorage.setItem(TOKEN_KEY, token),
  clear: () => localStorage.removeItem(TOKEN_KEY),
};

export const api = axios.create({ baseURL: `${process.env.REACT_APP_BACKEND_URL}/api` });

api.interceptors.request.use((config) => {
  const token = sessionStore.get();
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

api.interceptors.response.use(
  (res) => res,
  (error) => {
    const isAuthCall = error.config?.url?.startsWith("/auth/");
    if (error.response?.status === 401 && sessionStore.get() && !isAuthCall) {
      sessionStore.clear();
      window.location.assign("/auth");
    }
    if (error.response?.data?.detail === "consent_required") window.location.assign("/consent");
    return Promise.reject(error);
  }
);

export const errorMessage = (e) => {
  const detail = e?.response?.data?.detail;
  if (typeof detail === "string") return detail;
  if (Array.isArray(detail)) return detail.map((d) => d.msg).join(", ");
  if (e?.message === "Network Error") return "Can't reach the server. Check your connection and retry.";
  return e?.message || "Something went wrong";
};

export const data = (promise) => promise.then((r) => r.data);
