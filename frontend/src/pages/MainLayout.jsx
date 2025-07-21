import { Outlet, Link } from 'react-router-dom';
import styles from './MainLayout.module.css';

const MainLayout = () => {
  return (
    <div className={styles.pageContainer}>
      {/* ヘッダー */}
      <header className={styles.header}>
        <div className={styles.logoContainer}>
          <img src="/favicon.ico" alt="ANNOTOPIA Logo" className={styles.logo} />
          <span className={styles.logoText}>ANNOTOPIA</span>
        </div>
      </header>

      {/* サイドバーとメインコンテンツ */}
      <div className={styles.container}>
        {/* 左サイドバー */}
        <aside className={styles.sidebar}>
          <nav>
            <ul className={styles.menuList}>
              <Link to="/dashboard" className={styles.menuLink}><li className={styles.menuItem}>依頼する</li></Link>
              <Link to="/dashboard" className={styles.menuLink}><li className={styles.menuItem}>依頼リスト</li></Link>
              <Link to="/dashboard" className={styles.menuLink}><li className={styles.menuItem}>プロフィール</li></Link>
            </ul>
          </nav>
        </aside>

        {/* ★ここに子ページのコンテンツが表示される */}
        <Outlet />
      </div>
    </div>
  );
};

export default MainLayout;