import { Routes, Route, Navigate } from 'react-router-dom'
import { useAuthStore } from '@/shared/store/authStore'
import LoginPage from '@/features/auth/pages/LoginPage'
import DashboardPage from '@/features/dashboard/pages/DashboardPage'
import PlotsPage from '@/features/plots/pages/PlotsPage'
import FarmPage from '@/features/farm/pages/FarmPage'
import OperatorPage from '@/features/operator/pages/OperatorPage'
import NotFoundPage from '@/shared/pages/NotFoundPage'
import ProtectedRoute from '@/shared/components/ProtectedRoute'
import AppLayout from '@/shared/layouts/AppLayout'

export default function App() {
  const isAuthenticated = useAuthStore((s) => s.isAuthenticated)

  return (
    <Routes>
      {/* Public routes */}
      <Route
        path="/login"
        element={isAuthenticated ? <Navigate to="/dashboard" replace /> : <LoginPage />}
      />

      {/* Protected routes — wrapped inside AppLayout sidebar shell */}
      <Route element={<ProtectedRoute />}>
        <Route element={<AppLayout />}>
          <Route path="/dashboard" element={<DashboardPage />} />
          <Route path="/plots" element={<PlotsPage />} />
          <Route path="/farm/:plotId" element={<FarmPage />} />
          <Route path="/operator" element={<OperatorPage />} />
        </Route>
      </Route>

      {/* Redirects */}
      <Route path="/" element={<Navigate to="/dashboard" replace />} />
      <Route path="*" element={<NotFoundPage />} />
    </Routes>
  )
}
