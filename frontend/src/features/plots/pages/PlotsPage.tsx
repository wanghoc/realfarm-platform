import styles from './PlotsPage.module.css'

export default function PlotsPage() {
  return (
    <div className={styles.page}>
      <h1 className={styles.title}>My Plots</h1>
      <p className={styles.sub}>View and manage plots you are leasing.</p>

      <div className={styles.placeholder}>
        <p>🌱 Plot cards will appear here once leases are activated.</p>
        <p className={styles.hint}>Connect the <code>/api/v1/plots</code> endpoint to populate data.</p>
      </div>
    </div>
  )
}
