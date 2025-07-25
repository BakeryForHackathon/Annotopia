// AnnotationPage.jsx

import { useState, useEffect, useCallback } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import axios from 'axios';
import styles from './TestPage.module.css'; // スタイルは共通

const AnnotationPage = () => {
    const { taskId } = useParams();
    const navigate = useNavigate();

    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [annotationData, setAnnotationData] = useState(null);
    const [selectedAnswerId, setSelectedAnswerId] = useState(null);

    // --- フロント: handleGetAnnotationData ---
    const handleGetAnnotationData = useCallback(async () => {
        setLoading(true);
        try {
            const response = await axios.post('http://127.0.0.1:5001/api/get_annotation_data', {
                user_id: 3, // 本来はログイン情報から
                task_id: taskId
            });

            if (response.data.success) {
                if (response.data.end) {
                    // alert("このタスクの全てのアノテーションが完了しました！");
                    navigate('/order'); // 適切な完了後ページへ
                } else {
                    setAnnotationData(response.data);
                    setSelectedAnswerId(null); // 次の問題のためにリセット
                }
            } else {
                setError(response.data.message || 'アノテーションデータの取得に失敗しました。');
            }
        } catch (err) {
            setError('アノテーションデータの取得中にエラーが発生しました。');
        } finally {
            setLoading(false);
        }
    }, [taskId, navigate]);

    useEffect(() => {
        handleGetAnnotationData();
    }, [handleGetAnnotationData]);

    // --- フロント: handleMakeAnnotationData ---
    const handleMakeAnnotationData = async (e) => {
        e.preventDefault();
        if (!selectedAnswerId) {
            // alert('評価を選択してください。');
            return;
        }
        try {
            const response = await axios.post('http://127.0.0.1:5001/api/make_annotation_data', {
                user_id: 3, // 本来はログイン情報から
                task_id: taskId,
                annotation_data_id: annotationData.annotation_data_id,
                answers: [selectedAnswerId] // 配列形式で送信
            });

            if (response.data.success) {
                if (response.data.end) {
                    // alert("アノテーションのノルマが完了しました！");
                    navigate('/order'); // 適切な完了後ページへ
                } else {
                    // 次のデータを取得
                    handleGetAnnotationData();
                }
            } else {
                 setError(response.data.message || 'アノテーション結果の送信に失敗しました。');
            }
        } catch (err) {
            setError('アノテーション結果の送信中にエラーが発生しました。');
        }
    };
    
    if (loading) return <main className={styles.main}>次のデータを準備中...</main>;
    if (error) return <main className={`${styles.main} ${styles.error}`}>{error}</main>;
    if (!annotationData) return <main className={styles.main}>アノテーションデータが見つかりません。</main>;
    
    const questionInfo = annotationData.questions[0];

    return (
        <main className={styles.main}>
            <h1 className={styles.pageTitle}>アノテーション作業</h1>
            <div className={styles.progressContainer}>
                <div className={styles.progressBar} style={{ width: annotationData.status }}></div>
                <span className={styles.progressText}>{annotationData.status}</span>
            </div>
            <form onSubmit={handleMakeAnnotationData} className={styles.testForm}>
                <h2 className={styles.questionNumber}>問{annotationData.data_count + 1}</h2>
                
                <div className={styles.card}>
                    <h3 className={styles.cardTitle}>評価対象データ</h3>
                    <p className={styles.dataText}>
                        {annotationData.data.split('\n').map((line, index) => (
                            <span key={index}>{line}<br /></span>
                        ))}
                    </p>
                </div>

                <div className={styles.card}>
                    <h3 className={styles.cardTitle}>{questionInfo.question}</h3>
                    <div className={styles.radioGroup}>
                        {questionInfo.details.sort((a,b) => b.scale - a.scale).map((detail) => (
                            <label key={detail.question_details_id} className={styles.radioLabel}>
                                <input
                                    type="radio"
                                    name="annotation"
                                    value={detail.question_details_id}
                                    onChange={(e) => setSelectedAnswerId(Number(e.target.value))}
                                    checked={selectedAnswerId === detail.question_details_id}
                                    required
                                />
                                {detail.scale_description}
                            </label>
                        ))}
                    </div>
                </div>
                
                <button type="submit" className={styles.submitButton}>送信</button>
            </form>
        </main>
    );
};

export default AnnotationPage;