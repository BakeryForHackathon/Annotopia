import { useState, useEffect, useContext } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';
import styles from './ContractPage.module.css';
import { ApiContext, UserContext } from '../App';

const ContractPage = () => {
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const API_URL = useContext(ApiContext);
  const { userId } = useContext(UserContext);

  useEffect(() => {
    const fetchTasks = async () => {
      try {
        const response = await axios.post(`${API_URL}/api/all_requests`, { user_id: userId });
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
              <th>説明</th>
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
                  <td>{task.description}</td>
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
                <td colSpan="5">依頼されたタスクはありません。</td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </main>
  );
};

export default ContractPage;