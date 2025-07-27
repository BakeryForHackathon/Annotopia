import { useState, useEffect, useCallback, useContext } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import axios from 'axios';
import styles from './TestPage.module.css';
import { ApiContext, UserContext } from '../App';

const CreateMasterTestPage = () => {
  const { taskId } = useParams();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [annotationData, setAnnotationData] = useState(null);
  const [selectedAnswer, setSelectedAnswer] = useState(null);
  const API_URL = useContext(ApiContext);
  const { userId } = useContext(UserContext);

  const fetchNextAnnotationData = useCallback(async () => {
    setLoading(true);
    try {
      const response = await axios.post(`${API_URL}/api/get_test_data`, {
        user_id: userId,
        task_id: taskId,
      });

      // if (response.data.end) {
      //   // alert("このタスクのアノテーションは完了しました。");
      //   navigate('/order');
      // } else {
      //   setAnnotationData(response.data);
      //   setSelectedAnswer(null);
      // }
        setAnnotationData(response.data);
        setSelectedAnswer(null);
    } catch (err) {
      console.error(err);
      setError('アノテーションデータの取得に失敗しました。');
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
        // alert("このタスクのアノテーションはすべて完了しました。");
        navigate('/order');
      } else {
        fetchNextAnnotationData();
      }
    } catch (err) {
      console.error(err);
      setError('アノテーション結果の送信に失敗しました。');
    }
  };

  if (loading) return <main className={styles.main}>データを準備中...</main>;
  if (error) return <main className={`${styles.main} ${styles.error}`}>{error}</main>;
  if (!annotationData) return <main className={styles.main}>アノテーションデータが見つかりません。</main>;

  const { data, data_count, status, questions } = annotationData;
  const questionInfo = questions[0];

  console.log("Annotation Data:", annotationData);

  return (
    <main className={styles.main}>
        <h1 className={styles.pageTitle}>アノテーション作業</h1>
      <div className={styles.progressContainer}>
        <div className={styles.progressBar} style={{ width: status }}></div>
        <span className={styles.progressText}>{status}</span>
      </div>

      <form onSubmit={handleSubmit} className={styles.testForm}>
        <h2 className={styles.questionNumber}>問{data_count + 1}</h2>
        <div className={styles.card}>
          <h3 className={styles.cardTitle}>評価対象テキスト</h3>
          <div className={styles.dataText}>
            {data.replace(/\\n/g, '\n').split('\n').map((line, index) => (
              <div key={index}>{line || '\u00A0'}</div>
            ))}
          </div>
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

export default CreateMasterTestPage;