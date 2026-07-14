import { useParams } from 'react-router-dom'
import styles from './FarmPage.module.css'

/**
 * FarmPage hosts the digital farm view and customer-safe plot activity.
 * Transactional truth must always come from the API, not the rendered scene.
 */
export default function FarmPage() {
  const { plotId } = useParams<{ plotId: string }>()

  return (
    <div className={styles.page}>
      <h1 className={styles.title}>Farm View - Plot {plotId}</h1>

      <div className={styles.layout}>
        <div className={styles.gamePanel} id="farm-game-canvas-container">
          <p className={styles.gamePlaceholder}>Phaser 3 digital twin scene will mount here.</p>
        </div>

        <aside className={styles.sidePanel}>
          <section className={styles.section}>
            <h2 className={styles.sectionTitle}>Plot Status</h2>
            <p className={styles.placeholder}>Growth stage, health summary...</p>
          </section>

          <section className={styles.section}>
            <h2 className={styles.sectionTitle}>Request Action</h2>
            <p className={styles.placeholder}>Watering, inspection, nutrient check...</p>
          </section>

          <section className={styles.section}>
            <h2 className={styles.sectionTitle}>Activity Timeline</h2>
            <p className={styles.placeholder}>Care logs, work orders, snapshots...</p>
          </section>
        </aside>
      </div>
    </div>
  )
}
