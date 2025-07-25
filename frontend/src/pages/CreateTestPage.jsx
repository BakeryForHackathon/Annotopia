import { Link, useLocation } from 'react-router-dom';
import styles from './CreateTestPage.module.css';

const CreateTestPage = () => {
  const location = useLocation();
  const taskId = location.state?.taskId;

  if (!taskId) {
    return (
        <main className={styles.main}>
            <div className={styles.container}>
                <h1 className={styles.message}>エラー: タスクIDが見つかりません。</h1>
                <Link to="/order" className={styles.actionButton}>依頼ページに戻る</Link>
            </div>
        </main>
    )
  }

  return (
    <main className={styles.main}>
      <div className={styles.container}>
        <h1 className={styles.message}>タスクの作成が完了しました！</h1>
        <p className={styles.subMessage}>次のステップとして、受注者が受けるテストの「正解」を作成してください。</p>
        <Link to={`/task/${taskId}/create-master-test`} className={styles.actionButton}>
          テストの正解を作成する
        </Link>
      </div>
    </main>
  );
};

export default CreateTestPage;
