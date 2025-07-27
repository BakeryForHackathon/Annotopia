import { useEffect, useRef, useState } from 'react';
import { Outlet, NavLink, useLocation } from 'react-router-dom';
import styles from './MainLayout.module.css';

const MainLayout = () => {
  const location = useLocation();
  const menuListRef = useRef(null);
  const [indicatorStyle, setIndicatorStyle] = useState({ opacity: 0 });

  let activeBasePath = '';
  if (
    location.pathname.startsWith('/order') ||
    location.pathname.startsWith('/new-request')
  ) {
    activeBasePath = '/order';
  } else if (
    location.pathname.startsWith('/contract') ||
    location.pathname.startsWith('/task')
  ) {
    activeBasePath = '/contract';
  }

  useEffect(() => {
    if (activeBasePath) {
      const activeLink = menuListRef.current?.querySelector(
        `a[href="${activeBasePath}"]`
      );
      if (activeLink) {
        const listItem = activeLink.parentElement;
        setIndicatorStyle({
          opacity: 1,
          top: listItem.offsetTop,
          height: listItem.offsetHeight,
        });
      }
    } else {
      setIndicatorStyle({ opacity: 0 });
    }
  }, [activeBasePath]);

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
            <ul className={styles.menuList} ref={menuListRef}>
              <div className={styles.activeIndicator} style={indicatorStyle} />
              <li>
                <NavLink
                  to="/order"
                  className={
                    activeBasePath === '/order'
                      ? styles.activeMenuLink
                      : styles.menuLink
                  }
                >
                  依頼する
                </NavLink>
              </li>
              <li>
                <NavLink
                  to="/contract"
                  className={
                    activeBasePath === '/contract'
                      ? styles.activeMenuLink
                      : styles.menuLink
                  }
                >
                  依頼リスト
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