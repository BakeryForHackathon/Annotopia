import { useState, useEffect } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import axios from 'axios';
import styles from './TaskDetailPage.module.css';

const TaskDetailPage = () => {
  const { taskId } = useParams();
  const navigate = useNavigate();
  const [taskDetail, setTaskDetail] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // user_idはログイン情報などから取得することを想定。ここでは固定値'3'を使用
  // const userId = '3';

  useEffect(() => {
    const fetchTaskDetail = async () => {
      try {
        const response = await axios.post('/api/task_detail', {
          user_id: userId,
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
  }, [taskId, userId]);

  const handleStartTest = async () => {
    try {
      const response = await axios.post('/api/test_copy', {
        user_id: userId,
        task_id: taskId,
      });

      if (response.data.success) {
        navigate(`/task/${taskId}/test`);
      } else {
        setError('テストの開始に失敗しました。');
      }
    } catch (err) {
      setError('テストの開始中にエラーが発生しました。');
      console.error(err);
    }
  };

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
        <p className={styles.annotationCount}>アノテーション数: {taskDetail.max_annotations_per_user}個</p>
      </div>

      {taskDetail.questions.map((q, index) => (
        <div key={index} className={styles.card}>
          <h2 className={styles.questionTitle}>評価項目{index + 1}: {q.question}</h2>
          <ul className={styles.scaleList}>
            {q.scale_discription.slice().sort((a, b) => b.score - a.score).map((desc, i) => (
              <li key={i}>{desc.description}</li>
            ))}
          </ul>
        </div>
      ))}

      <div className={styles.actions}>
        {!taskDetail.ended ? (
          <button onClick={handleStartTest} className={styles.actionButton}>
            テストを行う
          </button>
        ) : (
          <Link to={`/task/${taskId}/annotate`} className={styles.actionButton}>
            アノテーションを行う
          </Link>
        )}
      </div>
    </main>
  );
};

export default TaskDetailPage;