import { useState, useEffect, useCallback } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import axios from 'axios';
import styles from './TestPage.module.css';

const TestPage = () => {
  const { taskId } = useParams();
  const navigate = useNavigate();

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [testQuestion, setTestQuestion] = useState(null);
  const [selectedAnswer, setSelectedAnswer] = useState(null);

  const fetchNextQuestion = useCallback(async () => {
    setLoading(true);
    try {
      const response = await axios.post('/api/get_test_question', {
        user_id: 3,
        task_id: taskId,
      });
      if (response.data.end) {
        // This case should ideally be handled after submitting the last answer
        // alert("テストが既に完了しているか、問題がありません。");
        navigate(`/task/${taskId}`);
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
    fetchNextQuestion();
  }, [fetchNextQuestion]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!selectedAnswer) {
      // alert("評価を選択してください。");
      return;
    }

    // 
    try {
      const response = await axios.post('/api/submit_test_answer', {
        user_id: 3, // ユーザーの入力が入るように修正
        task_id: taskId,
        answer: { questionId: testQuestion.question_index, answer: selectedAnswer },
      });

      if (response.data.end) {
        // api get_qwk
        const qwk_data = await axios.post('/api/get_qwk', {
          user_id: 3, // ユーザーの入力が入るように修正
          task_id: taskId,
        });

        // qwk = [{"question": question_map[group_id], "qwk": qwk, "clear": flag}, ...]
        const qwk = qwk_data.data.qwk_data
        navigate(`/task/${taskId}/result`, { state: { qwk: qwk } });
      } else {
        fetchNextQuestion();
      }
    } catch (err) {
      setError('テスト回答の送信に失敗しました。');
    }
  };

  if (loading) return <main className={styles.main}>問題を準備中...</main>;
  if (error) return <main className={`${styles.main} ${styles.error}`}>{error}</main>;
  if (!testQuestion) return <main className={styles.main}>テストデータが見つかりません。</main>;

  const { question, question_index, status, task_details } = testQuestion;
  const questionInfo = task_details.questions[0];

  return (
    <main className={styles.main}>
        <h1 className={styles.pageTitle}>適性テスト</h1>
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

export default TestPage;
