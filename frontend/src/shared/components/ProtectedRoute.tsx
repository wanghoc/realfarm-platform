import { Navigate, Outlet } from 'react-router-dom'
import { useAuthStore } from '@/shared/store/authStore'

/**
 * Wraps routes that require the user to be authenticated.
 * Redirects to /login if no valid session is present.
 */
export default function ProtectedRoute() {
  const isAuthenticated = useAuthStore((s) => s.isAuthenticated)

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />
  }

  return <Outlet />
}
