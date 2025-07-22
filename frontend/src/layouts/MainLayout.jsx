import { Outlet, NavLink } from 'react-router-dom';
import styles from './MainLayout.module.css';

const MainLayout = () => {
  return (
    <div className={styles.pageContainer}>
      <header className={styles.header}>
        <div className={styles.logoContainer}>
          <img src="/favicon.ico" alt="ANNOTOPIA Logo" className={styles.logo} />
          <span className={styles.logoText}>ANNOTOPIA</span>
        </div>
      </header>

      <div className={styles.container}>
        <aside className={styles.sidebar}>
          <nav>
            <ul className={styles.menuList}>
              <li>
                <NavLink
                  to="/order"
                  className={({ isActive }) =>
                    isActive ? styles.activeMenuLink : styles.menuLink
                  }
                >
                  依頼する
                </NavLink>
              </li>
              <li>
                <NavLink
                  to="/contract"
                  className={({ isActive }) =>
                    isActive ? styles.activeMenuLink : styles.menuLink
                  }
                >
                  依頼リスト
                </NavLink>
              </li>
              <li>
                <NavLink
                  to="/profile"
                  className={({ isActive }) =>
                    isActive ? styles.activeMenuLink : styles.menuLink
                  }
                >
                  プロフィール
                </NavLink>
              </li>
            </ul>
          </nav>
        </aside>

        <Outlet />
      </div>
    </div>
  );
};

export default MainLayout;
