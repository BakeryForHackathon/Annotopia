import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import axios from 'axios';
import styles from './TestPage.module.css'; // スタイルは受注者用と共通でOK

const CreateMasterTestPage = () => {
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
        const response = await axios.post('/api/get_test', { task_id: taskId });
        setTestData(response.data);
      } catch (err) {
        setError('テストの読み込みに失敗しました。');
      } finally {
        setLoading(false);
      }
    };
    fetchTest();
  }, [taskId]);

  const submitMasterAnswersToServer = async (finalAnswers) => {
    try {
      await axios.post('/api/submit_master_answers', {
        task_id: taskId,
        answers: finalAnswers,
      });
    //   alert("テストの正解データを保存しました。");
      navigate('/order'); // 保存後は依頼一覧ページなどに戻る
    } catch (err) {
      setError('正解データの送信に失敗しました。');
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
      submitMasterAnswersToServer(newAnswers);
    } else {
      setCurrentQuestionIndex(currentQuestionIndex + 1);
      setSelectedAnswer(null);
    }
  };

  if (loading) return <main className={styles.main}>テストを準備中...</main>;
  if (error) return <main className={`${styles.main} ${styles.error}`}>{error}</main>;
  if (!testData || !testData.test_info) return <main className={styles.main}>テストデータが見つかりません。</main>;
  
  const progress = ((currentQuestionIndex + 1) / testData.test_info.total_questions) * 100;
  const questionInfo = testData.task_detail.questions[0];
  const currentTestQuestion = testData.test_info.questions[currentQuestionIndex];

  return (
    <main className={styles.main}>
       <h1 className={styles.pageTitle}>テスト正解データ作成</h1>
      <div className={styles.progressContainer}>
        <div className={styles.progressBar} style={{ width: `${progress}%` }}></div>
        <span className={styles.progressText}>{Math.round(progress)}%</span>
      </div>

      <form onSubmit={handleSubmit} className={styles.testForm}>
        <h2 className={styles.questionNumber}>問{currentQuestionIndex + 1}</h2>
        <div className={styles.card}>
            <h3 className={styles.cardTitle}>原文 (英語)</h3>
            <p>{currentTestQuestion.source_text}</p>
        </div>
        <div className={styles.card}>
            <h3 className={styles.cardTitle}>機械翻訳 (日本語)</h3>
            <p>{currentTestQuestion.translated_text}</p>
        </div>
        
        <div className={styles.card}>
          <h3 className={styles.cardTitle}>{questionInfo.question}</h3>
          <div className={styles.radioGroup}>
            {questionInfo.scale_discription.slice().reverse().map((desc, index) => {
              const value = 3 - index;
              return (
                <label key={value} className={styles.radioLabel}>
                  <input type="radio" name="evaluation" value={value}
                    checked={selectedAnswer === String(value)}
                    onChange={(e) => setSelectedAnswer(e.target.value)}
                    required />
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

export default CreateMasterTestPage;
