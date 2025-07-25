import { useState, useEffect, useCallback } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import axios from 'axios';
import styles from './TestPage.module.css';

const CreateMasterTestPage = () => {
  const { taskId } = useParams();
  const navigate = useNavigate();

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [testQuestion, setTestQuestion] = useState(null);
  const [selectedAnswer, setSelectedAnswer] = useState(null);

  const fetchNextMasterQuestion = useCallback(async () => {
    setLoading(true);
    try {
      const response = await axios.post('http://127.0.0.1:5001/api/get_master_test_question', {
        task_id: taskId,
      });
      if (response.data.end) {
        // alert("正解データの作成が既に完了しています。");
        navigate('/order');
      } else {
        setTestQuestion(response.data);
        setSelectedAnswer(null);
      }
    } catch (err) {
      setError('テスト問題の取得に失敗しました。');
    } finally {
      setLoading(false);
    }
  }, [taskId, navigate]);

  useEffect(() => {
    fetchNextMasterQuestion();
  }, [fetchNextMasterQuestion]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!selectedAnswer) {
      // alert("評価を選択してください。");
      return;
    }

    try {
      const response = await axios.post('http://127.0.0.1:5001/api/submit_master_answer', {
        task_id: taskId,
        answer: { questionId: testQuestion.question_index, answer: selectedAnswer },
      });

      if (response.data.end) {
        // alert("テストの正解データを保存しました。");
        navigate('/order');
      } else {
        fetchNextMasterQuestion();
      }
    } catch (err) {
      setError('正解データの送信に失敗しました。');
    }
  };

  if (loading) return <main className={styles.main}>問題を準備中...</main>;
  if (error) return <main className={`${styles.main} ${styles.error}`}>{error}</main>;
  if (!testQuestion) return <main className={styles.main}>テストデータが見つかりません。</main>;

  const { question, question_index, status, task_details } = testQuestion;
  const questionInfo = task_details.questions[0];

  return (
    <main className={styles.main}>
        <h1 className={styles.pageTitle}>テスト正解データ作成</h1>
      <div className={styles.progressContainer}>
        {/* バックエンドから受け取ったstatusをそのまま表示 */}
        <div className={styles.progressBar} style={{ width: status }}></div>
        <span className={styles.progressText}>{status}</span>
      </div>

      <form onSubmit={handleSubmit} className={styles.testForm}>
        <h2 className={styles.questionNumber}>問{question_index + 1}</h2>
        <div className={styles.card}>
            <h3 className={styles.cardTitle}>評価対象テキスト</h3>
            <p className={styles.dataText}>
                {question.text.split('\n').map((line, index) => (
                    <span key={index}>{line}<br /></span>
                ))}
            </p>
        </div>

        <div className={styles.card}>
          <h3 className={styles.cardTitle}>{questionInfo.question}</h3>
          <div className={styles.radioGroup}>
             {[...questionInfo.scale_discription].sort((a,b) => b.score - a.score).map((level) => (
                <label key={level.score} className={styles.radioLabel}>
                    <input
                        type="radio" name="evaluation" value={level.score}
                        checked={selectedAnswer === String(level.score)}
                        onChange={(e) => setSelectedAnswer(e.target.value)}
                        required
                    />
                    {level.description}
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
