import { useState, useEffect, useCallback, useContext } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import axios from 'axios';
import styles from './TestPage.module.css';
import { ApiContext, UserContext } from '../App';

const TestPage = () => {
  const { taskId } = useParams();
  const navigate = useNavigate();
  const API_URL = useContext(ApiContext);
  const { userId } = useContext(UserContext);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [annotationData, setAnnotationData] = useState(null);
  const [selectedAnswer, setSelectedAnswer] = useState(null);

  const fetchNextAnnotationData = useCallback(async () => {
    setLoading(true);
    try {
      const response = await axios.post(`${API_URL}/api/get_test_data`, {
        user_id: userId,
        task_id: taskId,
      });

      if (response.data.end) {
        // alert("このタスクは既に完了しているか、実施できるものがありません。");
        navigate('/contract');
      } else {
        setAnnotationData(response.data);
        setSelectedAnswer(null);
      }
    } catch (err) {
      console.error(err);
      setError('データの取得に失敗しました。');
    } finally {
      setLoading(false);
    }
  }, [taskId, userId, navigate]);

  useEffect(() => {
    fetchNextAnnotationData();
  }, [fetchNextAnnotationData]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!selectedAnswer) {
      // alert("評価を選択してください。");
      return;
    }

    try {
      const response = await axios.post(`${API_URL}/api/get_make_data`, {
        user_id: userId,
        task_id: taskId,
        test_data_id: annotationData.test_data_id,
        answers: [selectedAnswer],
      });

      if (response.data.end) {
        const qwk_data = await axios.post(`${API_URL}/api/get_qwk`, {
          user_id: userId,
          task_id: taskId,
        });

        // qwk = [{"question": question_map[group_id], "qwk": qwk, "clear": flag}, ...]
        const qwk = qwk_data.data.qwk_data
        navigate(`/task/${taskId}/result`, { state: qwk });
      } else {
        fetchNextAnnotationData();
      }
    } catch (err) {
      console.error(err);
      setError('回答の送信に失敗しました。');
    }
  };

  if (loading) return <main className={styles.main}>データを準備中...</main>;
  if (error) return <main className={`${styles.main} ${styles.error}`}>{error}</main>;
  if (!annotationData) return <main className={styles.main}>データが見つかりません。</main>;

  const { data, data_count, status, questions } = annotationData;
  const questionInfo = questions[0];

  return (
    <main className={styles.main}>
        <h1 className={styles.pageTitle}>適正テスト</h1>
      <div className={styles.progressContainer}>
        <div className={styles.progressBar} style={{ width: status }}></div>
        <span className={styles.progressText}>{status}</span>
      </div>

      <form onSubmit={handleSubmit} className={styles.testForm}>
        <h2 className={styles.questionNumber}>問{data_count + 1}</h2>
        <div className={styles.card}>
            <h3 className={styles.cardTitle}>評価対象テキスト</h3>
            <p className={styles.dataText}>
                {data.split('\n').map((line, index) => (
                    <span key={index}>{line}<br /></span>
                ))}
            </p>
        </div>

        <div className={styles.card}>
          <h3 className={styles.cardTitle}>{questionInfo.question}</h3>
          <div className={styles.radioGroup}>
            {[...questionInfo.details].sort((a,b) => b.scale - a.scale).map((level) => (
                <label key={level.question_details_id} className={styles.radioLabel}>
                    <input
                        type="radio"
                        name="evaluation"
                        value={level.question_details_id}
                        checked={selectedAnswer === String(level.question_details_id)}
                        onChange={(e) => setSelectedAnswer(e.target.value)}
                        required
                    />
                    {level.scale_description}
                </label>
            ))}
          </div>
        </div>
        <button type="submit" className={styles.submitButton}>送信</button>
      </form>
    </main>
  );
};

export default TestPage;