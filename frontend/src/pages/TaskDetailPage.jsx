import { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom'; // useNavigateをLinkに変更
import axios from 'axios';
import styles from './TaskDetailPage.module.css';

const TaskDetailPage = () => {
  const { taskId } = useParams();
  // const navigate = useNavigate(); // Linkコンポーネントを使うため不要に
  const [taskDetail, setTaskDetail] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchTaskDetail = async () => {
      try {
        const response = await axios.post('/api/task_detail', {
          user_id: 3,
          task_id: taskId,
        });
        setTaskDetail(response.data);
      } catch (err) {
        setError('タスク詳細の取得に失敗しました。');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchTaskDetail();
  }, [taskId]);

  // handleStartTestはLinkコンポーネントに置き換えたため不要に
  // const handleStartTest = () => {
  //   navigate(`/task/${taskId}/test`);
  // };

  if (loading) return <main className={styles.main}>読み込み中...</main>;
  if (error) return <main className={`${styles.main} ${styles.error}`}>{error}</main>;
  if (!taskDetail) return <main className={styles.main}>タスクが見つかりません。</main>;

  return (
    <main className={styles.main}>
      <div className={styles.header}>
        <h1 className={styles.title}>{taskDetail.title}</h1>
        <p className={styles.period}>期間: {taskDetail.start_day} ~ {taskDetail.end_day}</p>
      </div>

      <div className={styles.card}>
        <p className={styles.description}>{taskDetail.description}</p>
        <p className={styles.annotationCount}>アノテーション数 {taskDetail.max_annotations_per_user}個</p>
      </div>

      {taskDetail.questions.map((q, index) => (
        <div key={index} className={styles.card}>
          <h2 className={styles.questionTitle}>評価項目{index + 1}: {q.question}</h2>
          <ul className={styles.scaleList}>
            {/* この部分は文字列の配列を正しく表示できます */}
            {q.scale_discription.slice().map((desc, i) => (
              <li key={i}>{desc.description}</li>
            ))}
          </ul>
        </div>
      ))}

      <div className={styles.actions}>
        {/* ボタンをLinkコンポーネントに変更し、出し分けを明確に */}
        {!taskDetail.test_ended ? (
          <Link to={`/task/${taskId}/test`} className={styles.actionButton}>
            テストを行う
          </Link>
        ) : (
          <Link to={`/task/${taskId}/annotate`} className={styles.actionButton}>
            annotateを行う
          </Link>
        )}
      </div>
    </main>
  );
};

export default TaskDetailPage;
