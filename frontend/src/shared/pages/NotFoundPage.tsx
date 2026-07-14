import styles from './NotFoundPage.module.css'
import { Link } from 'react-router-dom'

export default function NotFoundPage() {
  return (
    <div className={styles.container}>
      <h1 className={styles.code}>404</h1>
      <p className={styles.message}>Page not found</p>
      <Link to="/dashboard" className={styles.link}>Back to Dashboard</Link>
    </div>
  )
}
