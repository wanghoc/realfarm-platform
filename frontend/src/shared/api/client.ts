/**
 * api/client.ts — Axios instance for the RealFarm API.
 *
 * Features:
 * 1. Attaches JWT access token automatically on every request.
 * 2. On 401: attempts token refresh (single-flight guard) before logging out.
 * 3. After a successful refresh, retries the original failed request.
 *
 * The single-flight guard ensures that when multiple requests fail with 401
 * simultaneously, only ONE call to POST /auth/refresh is made. All other
 * pending requests wait for that single promise to resolve.
 */

import axios, { AxiosError, type InternalAxiosRequestConfig } from "axios";
import { useAuthStore } from "@/shared/store/authStore";

// ── Auth endpoints that must never trigger a refresh (avoid infinite loops) ──
const AUTH_ENDPOINTS = ["/api/v1/auth/login", "/api/v1/auth/refresh"];

// ── Single-flight refresh guard ───────────────────────────────────────────────
type TokenPair = { access_token: string; refresh_token: string };
let refreshPromise: Promise<TokenPair> | null = null;

// ── Axios instance ────────────────────────────────────────────────────────────
export const apiClient = axios.create({
  baseURL: "/api/v1",
  headers: { "Content-Type": "application/json" },
  timeout: 15_000,
});

// ── Request interceptor: attach access token ──────────────────────────────────
apiClient.interceptors.request.use((config: InternalAxiosRequestConfig) => {
  const token = useAuthStore.getState().accessToken;
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// ── Response interceptor: handle 401 with token refresh ──────────────────────
apiClient.interceptors.response.use(
  (response) => response,
  async (error: AxiosError) => {
    const originalRequest = error.config as InternalAxiosRequestConfig & { _retry?: boolean };

    // Only intercept 401 errors that haven't been retried yet
    if (error.response?.status !== 401 || originalRequest._retry) {
      return Promise.reject(error);
    }

    // Never attempt refresh for auth endpoints
    const isAuthEndpoint = AUTH_ENDPOINTS.some(
      (ep) => originalRequest.url?.startsWith(ep) || originalRequest.url === ep.replace("/api/v1", ""),
    );
    if (isAuthEndpoint) {
      useAuthStore.getState().logout();
      return Promise.reject(error);
    }

    const { refreshToken, setTokens, logout } = useAuthStore.getState();
    if (!refreshToken) {
      logout();
      return Promise.reject(error);
    }

    originalRequest._retry = true;

    try {
      // Single-flight: only one refresh call at a time
      if (!refreshPromise) {
        refreshPromise = axios
          .post<TokenPair>("/api/v1/auth/refresh", { refresh_token: refreshToken })
          .then((res) => res.data)
          .finally(() => {
            refreshPromise = null; // Reset guard after completion
          });
      }

      const newTokens = await refreshPromise;
      setTokens(newTokens.access_token, newTokens.refresh_token);

      // Retry the original request with the new access token
      originalRequest.headers.Authorization = `Bearer ${newTokens.access_token}`;
      return apiClient(originalRequest);
    } catch {
      // Refresh also failed — force logout
      logout();
      return Promise.reject(error);
    }
  },
);
