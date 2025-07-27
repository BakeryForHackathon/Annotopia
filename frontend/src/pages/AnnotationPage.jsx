import { useState, useEffect, useCallback, useContext } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import axios from 'axios';
import styles from './TestPage.module.css';
import { ApiContext, UserContext } from '../App';

const AnnotationPage = () => {
    const { taskId } = useParams();
    const navigate = useNavigate();
    const { userId } = useContext(UserContext);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [annotationData, setAnnotationData] = useState(null);
    const [selectedAnswerId, setSelectedAnswerId] = useState(null);
    const API_URL = useContext(ApiContext);
    console.log("userId:", userId, "taskId:", taskId); // ここを入れてログ確認

    const handleGetAnnotationData = useCallback(async () => {
        setLoading(true);
        try {
            const statusResponse = await axios.post(`${API_URL}/api/is_annotation_ended`, {
                user_id: userId,
                task_id: taskId,
            });
            console.log("statusResponse:", statusResponse.data); // ステータスレスポンスのログ確認

            if (statusResponse.data.end) {
                // alert("このタスクのノルマは既に完了しています。");
                navigate('/contract');
                return; // ここで処理を中断
            }

            const dataResponse = await axios.post(`${API_URL}/api/get_annotation_data`, {
                user_id: userId,
                task_id: taskId
            });
            console.log("dataResponse:", dataResponse.data); // アノテーションデータのレスポンスログ確認

            if (dataResponse.data.end) {
                // alert("このタスクの全てのアノテーションが完了しました！");
                navigate('/contract');
            } else {
                setAnnotationData(dataResponse.data);
                setSelectedAnswerId(null);
            }
        } catch (err) {
            console.log("userId:", userId, "taskId:", taskId); // ここを入れてログ確認

            setError('アノテーションデータの取得中にエラーが発生しました。');
            console.error(err);
        } finally {
            setLoading(false);
        }
    }, [taskId, userId, navigate]);

    useEffect(() => {
        handleGetAnnotationData();
    }, [handleGetAnnotationData]);

    const handleMakeAnnotationData = async (e) => {
        e.preventDefault();
        if (!selectedAnswerId) {
            // alert('評価を選択してください。');
            return;
        }
        try {
            const response = await axios.post(`${API_URL}/api/make_annotation_data`, {
                user_id: userId,
                task_id: taskId,
                annotation_data_id: annotationData.annotation_data_id,
                answers: [selectedAnswerId]
            });

            if (response.data.end) {
                // alert("アノテーションのノルマが完了しました！");
                navigate('/contract');
            } else {
                handleGetAnnotationData();
            }
        } catch (err) {
            setError('アノテーション結果の送信中にエラーが発生しました。');
            console.error(err);
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
