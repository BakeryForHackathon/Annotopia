import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import axios from 'axios';
import styles from './TestPage.module.css';

const TestPage = () => {
  const { taskId } = useParams();
  const navigate = useNavigate();
  const [testData, setTestData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [selectedAnswer, setSelectedAnswer] = useState(null);
  const [answers, setAnswers] = useState([]);

  useEffect(() => {
    const fetchTest = async () => {
      try {
        const response = await axios.post('http://127.0.0.1:5001/api/get_test', { task_id: taskId });
        setTestData(response.data);
      } catch (err) {
        setError('テストの読み込みに失敗しました。');
      } finally {
        setLoading(false);
      }
    };
    fetchTest();
  }, [taskId]);

  const submitTestToServer = async (finalAnswers) => {
    try {
      const response = await axios.post('http://127.0.0.1:5001/api/submit_test', {
        user_id: 3,
        task_id: taskId,
        answers: finalAnswers,
      });
      navigate(`/task/${taskId}/result`, { state: { result: response.data } });
    } catch (err) {
      setError('テスト結果の送信に失敗しました。');
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!selectedAnswer) {
      alert("評価を選択してください。");
      return;
    }

    const newAnswers = [...answers, { questionId: currentQuestionIndex, answer: selectedAnswer }];
    setAnswers(newAnswers);
    const isLastQuestion = currentQuestionIndex === testData.test_info.questions.length - 1;

    if (isLastQuestion) {
      submitTestToServer(newAnswers);
    } else {
      setCurrentQuestionIndex(currentQuestionIndex + 1);
      setSelectedAnswer(null);
    }
  };

  if (loading) return <main className={styles.main}>テストを準備中...</main>;
  if (error) return <main className={`${styles.main} ${styles.error}`}>{error}</main>;
  if (!testData) return <main className={styles.main}>テストが見つかりません。</main>;

  const progress = ((currentQuestionIndex + 1) / testData.test_info.total_questions) * 100;
  const questionInfo = testData.task_detail.questions[0];
  const currentTestQuestion = testData.test_info.questions[currentQuestionIndex];

  return (
    <main className={styles.main}>
      <div className={styles.progressContainer}>
        <div className={styles.progressBar} style={{ width: `${progress}%` }}></div>
        <span className={styles.progressText}>{Math.round(progress)}%</span>
      </div>

      <form onSubmit={handleSubmit} className={styles.testForm}>
        <h1 className={styles.questionNumber}>問{currentQuestionIndex + 1}</h1>
        <div className={styles.card}>
            <h2 className={styles.cardTitle}>原文 (英語)</h2>
            <p>{currentTestQuestion.source_text}</p>
        </div>
        <div className={styles.card}>
            <h2 className={styles.cardTitle}>機械翻訳 (日本語)</h2>
            <p>{currentTestQuestion.translated_text}</p>
        </div>

        <div className={styles.card}>
          <h2 className={styles.cardTitle}>{questionInfo.question}</h2>
          <div className={styles.radioGroup}>
            {questionInfo.scale_discription.slice().reverse().map((desc, index) => {
              const value = 3 - index;
              return (
                <label key={value} className={styles.radioLabel}>
                  <input
                    type="radio"
                    name="evaluation"
                    value={value}
                    checked={selectedAnswer === String(value)}
                    onChange={(e) => setSelectedAnswer(e.target.value)}
                    required
                  />
                  {desc}
                </label>
              );
            })}
          </div>
        </div>
        <button type="submit" className={styles.submitButton}>送信</button>
      </form>
    </main>
  );
};

export default TestPage;
