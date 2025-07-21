const DashboardPage = () => {
  return (
    <div style={styles.pageContainer}>
      {/* ヘッダー */}
      <header style={styles.header}>
        <div style={styles.logoContainer}>
            <img src="/public/favicon.ico" alt="ANNOTOPIA Logo" style={styles.logo} />
            <span style={styles.logoText}>ANNOTOPIA</span>
        </div>
      </header>

      <div style={styles.container}>
        {/* 左サイドバー */}
        <aside style={styles.sidebar}>
          <nav>
            <ul style={styles.menuList}>
              <li style={styles.menuItem}>依頼する</li>
              <li style={styles.menuItem}>依頼リスト</li>
              <li style={styles.menuItem}>プロフィール</li>
            </ul>
          </nav>
        </aside>

        {/* メイン画面 */}
        <main style={styles.main}>
          {/*
            メインコンテンツのエリアです。
            「新しい依頼」や「発注済み依頼リスト」などのコンテンツがここに表示されます。
            PDFの2ページ目に基づき、項目をカードとして配置します。
          */}
          <h1 style={styles.heading}>ダッシュボード</h1>
          <section style={styles.cardSection}>
            <div style={styles.card}>新しい依頼</div>
            <div style={styles.card}>発注済み依頼リスト</div>
          </section>
        </main>
      </div>
    </div>
  );
};

const styles = {
  pageContainer: {
    display: 'flex',
    flexDirection: 'column',
    minHeight: '100vh',
    fontFamily: 'sans-serif',
    backgroundColor: '#FFDAB9', // 全体の背景色
  },
  header: {
    padding: '15px 30px',
    backgroundColor: '#fff',
    boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
    display: 'flex',
    alignItems: 'center',
    zIndex: 10,
  },
  logoContainer: {
    display: 'flex',
    alignItems: 'center',
  },
  logo: {
    height: '40px',
    marginRight: '15px',
  },
  logoText: {
    fontSize: '1.8rem',
    fontWeight: 'bold',
    color: '#333',
  },
  container: {
    display: 'flex',
    flex: 1,
  },
  sidebar: {
    width: '240px',
    backgroundColor: '#fff',
    padding: '20px',
    boxShadow: '2px 0 5px rgba(0,0,0,0.1)',
  },
  menuList: {
    listStyle: 'none',
    padding: 0,
    margin: 0,
  },
  menuItem: {
    marginBottom: '18px',
    cursor: 'pointer',
    fontWeight: 'bold',
    color: '#333',
    fontSize: '1.1rem',
    padding: '10px 15px',
    borderRadius: '5px',
    transition: 'background-color 0.2s',
  },
  main: {
    flex: 1,
    padding: '40px',
    backgroundColor: '#f9f9f9',
  },
  heading: {
    fontSize: '1.8rem',
    marginBottom: '1.5rem',
    color: '#333',
  },
  cardSection: {
    display: 'grid',
    // 2列で表示
    gridTemplateColumns: 'repeat(2, 1fr)',
    gap: '20px',
  },
  card: {
    backgroundColor: '#ffffff',
    padding: '30px',
    borderRadius: '8px',
    boxShadow: '0 1px 5px rgba(0,0,0,0.1)',
    textAlign: 'center',
    fontWeight: 'bold',
    fontSize: '1.1rem',
    cursor: 'pointer',
  },
};

export default DashboardPage;