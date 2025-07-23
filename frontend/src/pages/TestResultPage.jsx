import { useLocation, useNavigate, useParams } from 'react-router-dom';
import styles from './TestResultPage.module.css';

const TestResultPage = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { taskId } = useParams();
  const result = location.state?.result;

  if (!result) {
    return (
      <main className={styles.main}>
        <div className={styles.card}>
          <p>結果データがありません。</p>
          <button onClick={() => navigate(`/task/${taskId}`)} className={styles.button}>
            タスク詳細に戻る
          </button>
        </div>
      </main>
    );
  }

  const handleReturn = () => {
    navigate(`/task/${taskId}`);
  };

  return (
    <main className={styles.main}>
      <div className={styles.card}>
        <p className={styles.subTitle}>依頼者との一致率...</p>
        <h1 className={styles.score}>{result.score}%</h1>
        <p className={styles.message}>
          {result.passed ? "合格です。" : "不合格です。"}
        </p>
        <button onClick={handleReturn} className={styles.button}>
          依頼画面に戻る
        </button>
      </div>
    </main>
  );
};

export default TestResultPage;
