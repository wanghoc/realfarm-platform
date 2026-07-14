import styles from './OperatorPage.module.css'

/**
 * Operator portal — for farm staff.
 * Provides work order dashboard and evidence upload (scaffolded).
 */
export default function OperatorPage() {
  return (
    <div className={styles.page}>
      <h1 className={styles.title}>Operator Portal</h1>
      <p className={styles.sub}>Manage work orders, evidence, and care logs.</p>

      <div className={styles.grid}>
        <div className={styles.card}>
          <h2 className={styles.cardTitle}>📋 Work Orders</h2>
          <p className={styles.placeholder}>Pending, in-progress, and completed work orders will appear here.</p>
        </div>
        <div className={styles.card}>
          <h2 className={styles.cardTitle}>📷 Evidence Upload</h2>
          <p className={styles.placeholder}>Photo evidence for completed tasks.</p>
        </div>
        <div className={styles.card}>
          <h2 className={styles.cardTitle}>📊 Care Logs</h2>
          <p className={styles.placeholder}>Fertiliser, watering, and inspection history.</p>
        </div>
        <div className={styles.card}>
          <h2 className={styles.cardTitle}>⚠️ Incidents</h2>
          <p className={styles.placeholder}>Crop failures, replacement requests.</p>
        </div>
      </div>
    </div>
  )
}
