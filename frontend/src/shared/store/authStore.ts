/**
 * authStore.ts — Zustand store for authentication state.
 *
 * Storage strategy:
 * - Access token: in-memory only (Zustand state). Lost on page refresh → re-authenticate via refresh token.
 * - Refresh token: localStorage (persists across page reloads).
 * - User info: localStorage (used to avoid blank UI on page reload while refresh is in flight).
 */

import { create } from "zustand";

const REFRESH_TOKEN_KEY = "realfarm_refresh_token";
const USER_KEY = "realfarm_user";

export type UserRole = "player" | "operator" | "admin";

export interface AuthUser {
  id: string;
  email: string;
  full_name: string;
  role: UserRole;
}

interface AuthState {
  /** Short-lived JWT — kept in memory only */
  accessToken: string | null;
  /** Long-lived opaque token — persisted to localStorage */
  refreshToken: string | null;
  /** Current authenticated user */
  user: AuthUser | null;
  /** True when the user has a valid session */
  isAuthenticated: boolean;

  /** Called after a successful login */
  setAuth: (accessToken: string, refreshToken: string, user: AuthUser) => void;
  /** Called by the refresh interceptor — updates tokens, keeps user unchanged */
  setTokens: (accessToken: string, refreshToken: string) => void;
  /** Clear everything and redirect to login */
  logout: () => void;
}

function readUser(): AuthUser | null {
  try {
    const raw = localStorage.getItem(USER_KEY);
    return raw ? (JSON.parse(raw) as AuthUser) : null;
  } catch {
    localStorage.removeItem(USER_KEY);
    return null;
  }
}

export const useAuthStore = create<AuthState>((set) => ({
  // On page load: restore refresh token and user from localStorage.
  // Access token starts null; the app will call /auth/refresh on first 401.
  accessToken: null,
  refreshToken: localStorage.getItem(REFRESH_TOKEN_KEY),
  user: readUser(),
  isAuthenticated: !!localStorage.getItem(REFRESH_TOKEN_KEY),

  setAuth: (accessToken, refreshToken, user) => {
    localStorage.setItem(REFRESH_TOKEN_KEY, refreshToken);
    localStorage.setItem(USER_KEY, JSON.stringify(user));
    set({ accessToken, refreshToken, user, isAuthenticated: true });
  },

  setTokens: (accessToken, refreshToken) => {
    localStorage.setItem(REFRESH_TOKEN_KEY, refreshToken);
    set({ accessToken, refreshToken });
  },

  logout: () => {
    localStorage.removeItem(REFRESH_TOKEN_KEY);
    localStorage.removeItem(USER_KEY);
    set({ accessToken: null, refreshToken: null, user: null, isAuthenticated: false });
  },
}));
