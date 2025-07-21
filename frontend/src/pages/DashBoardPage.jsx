import { Link } from 'react-router-dom';
import styles from './DashboardPage.module.css';

const DashboardPage = () => {
  return (
    <main className={styles.main}>
      <Link to="/new-request" className={styles.actionButton}>
        新しい依頼
      </Link>
      <div className={styles.listTitle}>発注済み依頼リスト</div>
    </main>
  );
};

export default DashboardPage;