import { useState, useEffect, useCallback } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import axios from 'axios';
import styles from './TestPage.module.css';

const CreateMasterTestPage = () => {
  const { taskId } = useParams();
  const navigate = useNavigate();

  // user_idはログイン情報から取得することを想定。ここではダミーデータとして'3'をセット
  const userId = '3';

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [annotationData, setAnnotationData] = useState(null);
  const [selectedAnswer, setSelectedAnswer] = useState(null);

  const fetchNextAnnotationData = useCallback(async () => {
    setLoading(true);
    try {
      // ===== 解決1: アノテーションデータをバックエンドから取得 =====
      const response = await axios.post('http://127.0.0.1:5001/api/get_test_data', {
        user_id: userId,
        task_id: taskId,
      });

      if (response.data.end) {
        // alert("このタスクのアノテーションは完了しました。");
        navigate('/order'); // 依頼一覧画面へ遷移
      } else {
        setAnnotationData(response.data);
        setSelectedAnswer(null); // 次のデータのために選択をリセット
      }
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
      // ===== 解決2: アノテーション結果をバックエンドに送信 =====
      const response = await axios.post('http://127.0.0.1:5001/api/get_make_data', {
        user_id: userId,
        task_id: taskId,
        test_data_id: annotationData.test_data_id,
        answers: [selectedAnswer], // 配列形式で送信
      });

      if (response.data.end) {
        // alert("このタスクのアノテーションはすべて完了しました。");
        navigate('/order'); // 依頼一覧画面へ遷移
      } else {
        // 次のデータを取得
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
  const questionInfo = questions[0]; // 質問は1つと仮定

  return (
    <main className={styles.main}>
        <h1 className={styles.pageTitle}>アノテーション作業</h1>
      <div className={styles.progressContainer}>
        <div className={styles.progressBar} style={{ width: status }}></div>
        <span className={styles.progressText}>{status}</span>
      </div>

      <form onSubmit={handleSubmit} className={styles.testForm}>
        {/* data_countは0から始まるため、+1して表示 */}
        <h2 className={styles.questionNumber}>問{data_count + 1}</h2>
        <div className={styles.card}>
            <h3 className={styles.cardTitle}>評価対象テキスト</h3>
            <p className={styles.dataText}>
                {/* APIから受け取ったテキストデータを改行で分割して表示 */}
                {data.split('\n').map((line, index) => (
                    <span key={index}>{line}<br /></span>
                ))}
            </p>
        </div>

        <div className={styles.card}>
          <h3 className={styles.cardTitle}>{questionInfo.question}</h3>
          <div className={styles.radioGroup}>
            {/* 評価スケールを降順にソートして表示 */}
            {[...questionInfo.details].sort((a,b) => b.scale - a.scale).map((level) => (
                <label key={level.question_details_id} className={styles.radioLabel}>
                    <input
                        type="radio"
                        name="evaluation"
                        value={level.question_details_id} // 送信するのはquestion_details_id
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