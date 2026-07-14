import styles from './DashboardPage.module.css'
import { useAuthStore } from '@/shared/store/authStore'

export default function DashboardPage() {
  const user = useAuthStore((s) => s.user)

  return (
    <div className={styles.page}>
      <header className={styles.header}>
        <h1 className={styles.greeting}>Welcome back, {user?.full_name ?? 'Farmer'}</h1>
        <p className={styles.sub}>Here's a summary of your plots and activities.</p>
      </header>

      <section className={styles.stats} aria-label="Quick stats">
        <StatCard label="Active Plots" value="-" id="stat-active-plots" />
        <StatCard label="Pending Actions" value="-" id="stat-pending-actions" />
        <StatCard label="Work Orders" value="-" id="stat-work-orders" />
        <StatCard label="Harvests this Season" value="-" id="stat-harvests" />
      </section>

      <section className={styles.placeholder}>
        <p>Plot overview and crop timeline will appear here.</p>
        <p className={styles.hint}>Connect backend to populate data.</p>
      </section>
    </div>
  )
}

function StatCard({ label, value, id }: { label: string; value: string; id: string }) {
  return (
    <div id={id} className={styles.statCard}>
      <div>
        <p className={styles.statLabel}>{label}</p>
        <p className={styles.statValue}>{value}</p>
      </div>
    </div>
  )
}
