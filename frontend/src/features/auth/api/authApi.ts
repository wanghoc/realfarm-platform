/**
 * authApi.ts — API calls for the auth feature.
 *
 * Matches the backend schemas in backend/app/modules/auth/api/router.py
 */

import { apiClient } from "@/shared/api/client";
import { useAuthStore, type AuthUser } from "@/shared/store/authStore";

// ── Types ─────────────────────────────────────────────────────────────────────

export interface LoginRequest {
  email: string;
  password: string;
}

export interface LoginResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
  user: AuthUser;
}

export interface RefreshResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
}

// ── API functions ─────────────────────────────────────────────────────────────

export async function loginRequest(credentials: LoginRequest): Promise<LoginResponse> {
  const response = await apiClient.post<LoginResponse>("/auth/login", credentials);
  return response.data;
}

export async function refreshTokenRequest(refreshToken: string): Promise<RefreshResponse> {
  const response = await apiClient.post<RefreshResponse>("/auth/refresh", {
    refresh_token: refreshToken,
  });
  return response.data;
}

// ── React hook ────────────────────────────────────────────────────────────────

export function useLogin() {
  const { setAuth } = useAuthStore();

  return async (credentials: LoginRequest): Promise<LoginResponse> => {
    const data = await loginRequest(credentials);
    setAuth(data.access_token, data.refresh_token, data.user);
    return data;
  };
}
