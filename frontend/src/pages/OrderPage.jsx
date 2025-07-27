import { useState, useEffect, useContext } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';
import styles from './OrderPage.module.css';
import { ApiContext, UserContext } from '../App';

const OrderPage = () => {
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const API_URL = useContext(ApiContext);
  const { userId } = useContext(UserContext);

  useEffect(() => {
    if (!userId) {
      setLoading(false);
      return;
    }
    const fetchTasks = async () => {
      setLoading(true);
      try {
        const response = await axios.post(`${API_URL}/api/requests`, {
          user_id: userId,
        });


        setTasks(response.data.tasks);
      } catch (err) {
        setError('依頼リストの取得に失敗しました。');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchTasks();
  }, [userId]);

  const handleSendTaskId = async (taskId) => {
    try {
      const response = await axios.post(`${API_URL}/api/finalize_task`, {
        task_id: taskId,
      });
      alert('完了処理が送信されました。');
      // 必要に応じて再読み込み
      // fetchTasks(); ← useEffect外に移動して呼べるようにしてもOK
    } catch (err) {
      console.error('タスク送信に失敗:', err);
      alert('タスクの送信に失敗しました。');
    }
  };


  const renderTaskList = () => {
    if (loading) {
      return <tbody><tr><td colSpan="5" className={styles.loading}>読み込み中...</td></tr></tbody>;
    }
    if (error) {
      return <tbody><tr><td colSpan="5" className={styles.error}>{error}</td></tr></tbody>;
    }
    if (tasks.length === 0) {
      return <tbody><tr><td colSpan="5" className={styles.noTasks}>発注済みの依頼はありません。</td></tr></tbody>;
    }
    return (
      <tbody>
        {tasks.map((task) => (
          <tr key={task.task_id}>
            <td>{task.title}</td>
            <td>{task.status}</td>
            <td>{task.created_at}</td>
            <td>{task.due_date}</td>
            <td>
              {task.status === '100%' && (
                <button
                  className={styles.finalizeButton}
                  onClick={() => handleSendTaskId(task.task_id)}
                >
                  完了処理を送信
                </button>
              )}
            </td>
          </tr>
        ))}
      </tbody>
    );
  };

  return (
    <main className={styles.main}>
      <Link to="/new-request" className={styles.actionButton}>
        新しい依頼
      </Link>
      <div className={styles.listTitle}>発注済み依頼リスト</div>
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
          {renderTaskList()}
        </table>
      </div>
    </main>
  );
};

export default OrderPage;
