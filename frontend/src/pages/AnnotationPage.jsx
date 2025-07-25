import { useState, useEffect, useCallback } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import axios from 'axios';
import styles from './AnnotationPage.module.css';

const AnnotationPage = () => {
    const { taskId } = useParams();
    const navigate = useNavigate();

    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [annotationData, setAnnotationData] = useState(null);
    const [selectedAnswers, setSelectedAnswers] = useState({});

    const handleGetAnnotationData = useCallback(async () => {
        setLoading(true);
        try {
            const response = await axios.post('http://127.0.0.1:5001/api/get_annotation_data', {
                user_id: 3,
                task_id: taskId
            });
            if (response.data.all_done) {
                alert("このタスクの全てのアノテーションが完了しました！");
                navigate('/order');
            } else {
                setAnnotationData(response.data);
                setSelectedAnswers({});
            }
        } catch (err) {
            setError('アノテーションデータの取得に失敗しました。');
        } finally {
            setLoading(false);
        }
    }, [taskId, navigate]);

    useEffect(() => {
        handleGetAnnotationData();
    }, [handleGetAnnotationData]);

    const handleMakeAnnotation = async (e) => {
        e.preventDefault();
        if (Object.keys(selectedAnswers).length === 0) {
            alert('評価を選択してください。');
            return;
        }
        try {
            const response = await axios.post('http://127.0.0.1:5001/api/make_annotation', {
                user_id: 3,
                task_id: taskId,
                annotation_id: annotationData.annotation_id,
                answers: selectedAnswers
            });
            if (response.data.end) {
                alert("このタスクの全てのアノテーションが完了しました！");
                navigate('/order');
            } else {
                handleGetAnnotationData();
            }
        } catch (err) {
            setError('アノテーション結果の送信に失敗しました。');
        }
    };
    
    const handleAnswerChange = (question, score) => {
        setSelectedAnswers(prev => ({
            ...prev,
            [question]: score
        }));
    };

    if (loading) return <main className={styles.main}>次のデータを準備中...</main>;
    if (error) return <main className={`${styles.main} ${styles.error}`}>{error}</main>;
    if (!annotationData) return <main className={styles.main}>アノテーションデータが見つかりません。</main>;
    
    const progress = parseFloat(annotationData.status);

    return (
        <main className={styles.main}>
            <div className={styles.progressContainer}>
                <div className={styles.progressBar} style={{ width: `${progress}%` }}></div>
                <span className={styles.progressText}>{annotationData.status}</span>
            </div>
            <form onSubmit={handleMakeAnnotation} className={styles.annotationForm}>
                <h1 className={styles.questionNumber}>問{annotationData.data_count + 1}</h1>
                <div className={styles.card}>
                    <h2 className={styles.cardTitle}>評価対象データ</h2>
                    <p className={styles.dataText}>
                        {annotationData.data.split('\n').map((line, index) => (
                            <span key={index}>{line}<br /></span>
                        ))}
                    </p>
                </div>
                {annotationData.questions.map((q, qIndex) => (
                    <div key={qIndex} className={styles.card}>
                        <h2 className={styles.cardTitle}>{q.question}</h2>
                        <div className={styles.radioGroup}>
                            {[...q.scale_discription].sort((a,b) => b.score - a.score).map((level) => (
                                <label key={level.score} className={styles.radioLabel}>
                                    <input
                                        type="radio"
                                        name={`question-${qIndex}`}
                                        value={level.score}
                                        onChange={() => handleAnswerChange(q.question, level.score)}
                                        checked={selectedAnswers[q.question] === level.score}
                                        required
                                    />
                                    {level.description}
                                </label>
                            ))}
                        </div>
                    </div>
                ))}
                <button type="submit" className={styles.submitButton}>送信</button>
            </form>
        </main>
    );
};

export default AnnotationPage;