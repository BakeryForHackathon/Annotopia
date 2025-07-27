import { useLocation, useNavigate, useParams } from 'react-router-dom';
import styles from './TestResultPage.module.css';

const TestResultPage = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { taskId } = useParams();
  const qwkList = location.state?.qwkList;
  console.log("QWK List:", qwkList);
  if (!qwkList || !Array.isArray(qwkList)) {
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
        <p className={styles.subTitle}>各評価項目の一致率と判定結果</p>
        <ul className={styles.resultList}>
          {qwkList.map((item, index) => (
            <li key={index} className={styles.resultItem}>
              <strong>{item.question}:</strong> 一致率 {Math.round(item.qwk * 100)}% - {item.clear ? "合格" : "不合格"}
            </li>
          ))}
        </ul>
        <button onClick={handleReturn} className={styles.button}>
          依頼画面に戻る
        </button>
      </div>
    </main>
  );
};

export default TestResultPage;
