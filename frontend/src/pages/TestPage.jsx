import { useState, useEffect, useCallback } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import axios from 'axios';
import styles from './TestPage.module.css';

const TestPage = () => {
  const { taskId } = useParams();
  const navigate = useNavigate();

  // user_idはログイン情報から取得することを想定。ここではダミーデータとして'3'をセット
  const userId = '3';

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [annotationData, setAnnotationData] = useState(null);
  const [selectedAnswer, setSelectedAnswer] = useState(null);

  // 関数名をfetchNextAnnotationDataに変更し、ロジックを統一
  const fetchNextAnnotationData = useCallback(async () => {
    setLoading(true);
    try {
      // CreateMasterTestPage.jsxと全く同じAPIを呼び出す
      const response = await axios.post('http://127.0.0.1:5001/api/get_test_data', {
        user_id: userId,
        task_id: taskId,
      });

      if (response.data.end) {
        // alert("このタスクは既に完了しているか、実施できるものがありません。");
        navigate('/order'); // 完了時は依頼一覧画面へ遷移
      } else {
        setAnnotationData(response.data);
        setSelectedAnswer(null); // 次のデータのために選択をリセット
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
      // 送信するデータ形式とAPIエンドポイントを統一
      const response = await axios.post('http://127.0.0.1:5001/api/get_make_data', {
        user_id: userId,
        task_id: taskId,
        test_data_id: annotationData.test_data_id,
        answers: [selectedAnswer], // 配列形式で送信
      });

      if (response.data.end) {
        // alert("タスクが完了しました。");
        navigate('/order'); // 完了時は依頼一覧画面へ遷移
      } else {
        // 次のデータを取得
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

  // state名をannotationDataに統一し、受け取るデータ構造を反映
  const { data, data_count, status, questions } = annotationData;
  const questionInfo = questions[0]; // 質問は1つと仮定

  return (
    <main className={styles.main}>
        {/* ページの目的に合わせてタイトルを修正 */}
        <h1 className={styles.pageTitle}>適正テスト</h1>
      <div className={styles.progressContainer}>
        <div className={styles.progressBar} style={{ width: status }}></div>
        <span className={styles.progressText}>{status}</span>
      </div>

      <form onSubmit={handleSubmit} className={styles.testForm}>
        {/* data_countを基に問題番号を表示 */}
        <h2 className={styles.questionNumber}>問{data_count + 1}</h2>
        <div className={styles.card}>
            <h3 className={styles.cardTitle}>評価対象テキスト</h3>
            <p className={styles.dataText}>
                {/* テキストの表示ロジックを統一 */}
                {data.split('\n').map((line, index) => (
                    <span key={index}>{line}<br /></span>
                ))}
            </p>
        </div>

        <div className={styles.card}>
          <h3 className={styles.cardTitle}>{questionInfo.question}</h3>
          <div className={styles.radioGroup}>
             {/* 選択肢の表示ロジックを統一 */}
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

export default TestPage;