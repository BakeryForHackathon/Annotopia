import React, { useState, useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import commonStyles from './OrderPage.module.css';
import formStyles from './NewRequestPage.module.css';
import { ApiContext, UserContext } from '../App';

const NewRequestPage = () => {
    const navigate = useNavigate();
    const API_URL = useContext(ApiContext);
    const { userId } = useContext(UserContext);

    // --- フォームの各入力値を管理するState ---
    const [title, setTitle] = useState('機械翻訳の評価');
    const [description, setDescription] = useState('英日翻訳の正確さを3段階で評価してください');
    const [evaluationItems, setEvaluationItems] = useState([
        {
            name: '正確さ',
            levels: [
                { score: 3, description: '原文の意味を完全に伝えており、情報の欠落や誤訳がまったくない。' },
                { score: 2, description: '原文の意味の半分以上は伝えているが、重要な情報の抜けや軽微な誤訳がある。' },
                { score: 1, description: '原文の意味をほとんどまたは全く伝えていない。意味が通らないか、全く異なる内容になっている。' },
            ],
        },
    ]);
    const [startDate, setStartDate] = useState(new Date().toISOString().slice(0, 10));
    const [endDate, setEndDate] = useState('2025-08-07');
    const [maxAnnotations, setMaxAnnotations] = useState(100);
    const [threshold, setThreshold] = useState(0.5);
    const [isPrivate, setIsPrivate] = useState(true);
    const [testFile, setTestFile] = useState(null);
    const [dataFile, setDataFile] = useState(null);

    const handleItemNameChange = (itemIndex, value) => {
        const newItems = [...evaluationItems];
        newItems[itemIndex].name = value;
        setEvaluationItems(newItems);
    };

    const handleLevelDescChange = (itemIndex, levelIndex, value) => {
        const newItems = [...evaluationItems];
        newItems[itemIndex].levels[levelIndex].description = value;
        setEvaluationItems(newItems);
    };

    const addEvaluationItem = () => {
        setEvaluationItems([
            ...evaluationItems,
            { name: '', levels: [{ score: 1, description: '' }] },
        ]);
    };

    const removeEvaluationItem = (index) => {
        const newItems = evaluationItems.filter((_, i) => i !== index);
        setEvaluationItems(newItems);
    };

    const addLevel = (itemIndex) => {
        const newItems = [...evaluationItems];
        const currentLevels = newItems[itemIndex].levels;
        const newScore = currentLevels.length > 0 ? Math.max(...currentLevels.map(l => l.score)) + 1 : 1;
        newItems[itemIndex].levels.unshift({ score: newScore, description: '' });
        setEvaluationItems(newItems);
    };

    const removeLevel = (itemIndex, levelIndex) => {
        const newItems = [...evaluationItems];
        newItems[itemIndex].levels = newItems[itemIndex].levels.filter((_, i) => i !== levelIndex);
        setEvaluationItems(newItems);
    };

    const handleSubmit = async (event) => {
        event.preventDefault();
        const questionsPayload = evaluationItems.map(item => {
            const sortedLevels = [...item.levels].sort((a, b) => a.score - b.score);
            return {
                question: item.name,
                scale_discription: sortedLevels.map(level => level.description)
            };
        });
        const formData = new FormData();
        formData.append('user_id', userId);
        formData.append('title', title);
        formData.append('description', description);
        formData.append('question_count', questionsPayload.length);
        formData.append('questions', JSON.stringify(questionsPayload));
        formData.append('private', isPrivate);
        formData.append('start_day', startDate.replace(/-/g, '/'));
        formData.append('end_day', endDate.replace(/-/g, '/'));
        formData.append('max_annotations_per_user', maxAnnotations);
        formData.append('test', !!testFile);
        formData.append('threshold', threshold);
        if (testFile) {
            formData.append('test_data', testFile);
        }
        if (dataFile) {
            formData.append('data', dataFile);
        }
        try {
            const response = await axios.post(`${API_URL}/api/upload_task`, formData, {});

            if (response.data.success) {
                console.log('タスク作成成功:', response.data);
                navigate('/new-request/create-test', { state: { taskId: response.data.task_id } });
            } else {
                console.error('タスク作成失敗:', response.data);
            }
        } catch (error) {
            console.error('フォーム送信エラー:', error);
        }
    };

    return (
        <main className={commonStyles.main}>
            <form className={formStyles.formContainer} onSubmit={handleSubmit}>
                <h2 className={formStyles.title}>新しい依頼の作成</h2>
                <div className={formStyles.formGroup}>
                    <label htmlFor="requestName">依頼名</label>
                    <input id="requestName" type="text" value={title} onChange={(e) => setTitle(e.target.value)} required />
                </div>
                <div className={formStyles.formGroup}>
                    <label htmlFor="description">説明</label>
                    <textarea id="description" rows="3" value={description} onChange={(e) => setDescription(e.target.value)} required></textarea>
                </div>
                {evaluationItems.map((item, itemIndex) => (
                    <fieldset key={itemIndex} className={formStyles.fieldset}>
                        <legend>評価項目 {itemIndex + 1}</legend>
                        <button type="button" onClick={() => removeEvaluationItem(itemIndex)} className={formStyles.removeButton}>項目を削除</button>
                        <div className={formStyles.formGroup}>
                            <label htmlFor={`itemName${itemIndex}`}>項目名</label>
                            <input id={`itemName${itemIndex}`} type="text" value={item.name} onChange={(e) => handleItemNameChange(itemIndex, e.target.value)} required />
                        </div>
                        <div className={formStyles.formGroup}>
                            <label>各段階の説明</label>
                            <button type="button" onClick={() => addLevel(itemIndex)} className={formStyles.addButton}>段階を追加</button>
                            {item.levels.map((level, levelIndex) => (
                                <div key={levelIndex} className={formStyles.levelDescription}>
                                    <span>{level.score}:</span>
                                    <textarea rows="2" value={level.description} onChange={(e) => handleLevelDescChange(itemIndex, levelIndex, e.target.value)} required></textarea>
                                    <button type="button" onClick={() => removeLevel(itemIndex, levelIndex)} className={formStyles.removeSmallButton}>×</button>
                                </div>
                            ))}
                        </div>
                    </fieldset>
                ))}
                <button type="button" onClick={addEvaluationItem} className={formStyles.addButton}>評価項目を追加</button>
                <div className={formStyles.formGroup}>
                    <label htmlFor="startDate">開始日</label>
                    <input id="startDate" type="date" value={startDate} onChange={(e) => setStartDate(e.target.value)} required className={formStyles.shortInput} />
                </div>
                <div className={formStyles.formGroup}>
                    <label htmlFor="endDate">終了日</label>
                    <input id="endDate" type="date" value={endDate} onChange={(e) => setEndDate(e.target.value)} required className={formStyles.shortInput} />
                </div>
                <div className={formStyles.formGroup}>
                    <label htmlFor="maxAnnotations">一人当たりのデータ数</label>
                    <input id="maxAnnotations" type="number" value={maxAnnotations} onChange={(e) => setMaxAnnotations(e.target.value)} className={formStyles.shortInput} />
                </div>
                <div className={formStyles.formGroup}>
                    <label htmlFor="threshold">テストの閾値</label>
                    <input id="threshold" type="text" value={threshold} onChange={(e) => setThreshold(e.target.value)} className={formStyles.shortInput} />
                </div>
                <div className={formStyles.formGroup}>
                    <label>
                        <input type="checkbox" checked={isPrivate} onChange={(e) => setIsPrivate(e.target.checked)} />
                        プライベートモード
                    </label>
                </div>
                <div className={formStyles.formGroup}>
                    <label>テストデータのアップロード (CSV)</label>
                    <input type="file" accept=".csv" onChange={(e) => setTestFile(e.target.files[0])} />
                </div>
                <div className={formStyles.formGroup}>
                    <label>評価データのアップロード (CSV)</label>
                    <input type="file" accept=".csv" onChange={(e) => setDataFile(e.target.files[0])} />
                </div>
                <div className={formStyles.submitContainer}>
                    <button type="submit" className={formStyles.submitButton}>送信してタスクを作成</button>
                </div>
            </form>
        </main>
    );
};

export default NewRequestPage;
