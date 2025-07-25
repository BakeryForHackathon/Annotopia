import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';
import styles from './ContractPage.module.css';

const ContractPage = () => {
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchTasks = async () => {
      try {
        const response = await axios.post('http://127.0.0.1:5001/api/all_requests', { user_id: 3 });
        setTasks(response.data.tasks);
      } catch (err) {
        setError('データの取得に失敗しました。');
      } finally {
        setLoading(false);
      }
    };
    fetchTasks();
  }, []);

  if (loading) return <div className={styles.main}>読み込み中...</div>;
  if (error) return <div className={`${styles.main} ${styles.error}`}>{error}</div>;

  return (
    <main className={styles.main}>
      <h1 className={styles.title}>依頼リスト</h1>
      <div className={styles.tableContainer}>
        <table className={styles.taskTable}>
          <thead>
            <tr>
              <th>タスク名</th>
              <th>ステータス</th>
              <th>依頼日</th>
              <th>納期</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            {tasks.length > 0 ? (
              tasks.map((task) => (
                <tr key={task.task_id}>
                  <td>{task.title}</td>
                  <td>{task.status}</td>
                  <td>{task.created_at}</td>
                  <td>{task.due_date}</td>
                  <td>
                    <Link to={`/task/${task.task_id}`} className={styles.actionButton}>
                      詳細を見る
                    </Link>
                  </td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan="5">依頼したタスクはありません。</td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </main>
  );
};

export default ContractPage;