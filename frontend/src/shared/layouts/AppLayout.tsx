import { NavLink, Outlet } from 'react-router-dom'
import { useAuthStore } from '@/shared/store/authStore'
import styles from './AppLayout.module.css'

const NAV_ITEMS = [
  { to: '/dashboard', icon: '🏠', label: 'Dashboard' },
  { to: '/plots', icon: '🌱', label: 'My Plots' },
  { to: '/operator', icon: '🛠', label: 'Operator' },
]

export default function AppLayout() {
  const { user, logout } = useAuthStore()

  return (
    <div className={styles.shell}>
      <aside className={styles.sidebar}>
        <div className={styles.brand}>
          <span className={styles.brandIcon}>🌱</span>
          <span className={styles.brandName}>RealFarm</span>
        </div>

        <nav className={styles.nav} aria-label="Main navigation">
          {NAV_ITEMS.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              className={({ isActive }) =>
                [styles.navItem, isActive ? styles.navItemActive : ''].join(' ')
              }
            >
              <span className={styles.navIcon} aria-hidden="true">{item.icon}</span>
              <span>{item.label}</span>
            </NavLink>
          ))}
        </nav>

        <div className={styles.userSection}>
          <div className={styles.userInfo}>
            <span className={styles.userAvatar} aria-hidden="true">👤</span>
            <div>
              <p className={styles.userName}>{user?.full_name ?? 'Unknown'}</p>
              <p className={styles.userRole}>{user?.role}</p>
            </div>
          </div>
          <button
            id="sidebar-logout-btn"
            className={styles.logoutBtn}
            onClick={logout}
          >
            Sign out
          </button>
        </div>
      </aside>

      <main className={styles.content}>
        <Outlet />
      </main>
    </div>
  )
}
