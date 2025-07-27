import React, { useState, useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { Plus, X, Upload, Calendar, Users, Target } from 'lucide-react';
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
    const [maxAnnotations, setMaxAnnotations] = useState(10);
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
        formData.append('test', true);
        formData.append('test_data', !!testFile);
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
        <main className="bg-orange-50 flex-1 py-8 px-10 box-border overflow-y-auto">
            <form className="w-full max-w-4xl mx-auto space-y-6" onSubmit={handleSubmit}>
                {/* ヘッダー */}
                <div className="bg-white rounded-xl shadow-sm p-8 border border-orange-100">
                    <h2 className="text-3xl font-bold text-gray-800 mb-2 mt-0">新しい依頼の作成</h2>
                    <p className="text-gray-600 mt-0 mb-0">評価タスクの詳細を設定してください</p>
                </div>

                {/* 基本情報 */}
                <div className="bg-white rounded-xl shadow-sm p-8 border border-orange-100">
                    <h2 className="text-xl font-semibold text-gray-800 mb-6 flex items-center">
                        <Target className="w-5 h-5 mr-2 text-orange-500" />
                        基本情報
                    </h2>
                    
                    <div className="mb-6">
                        <label htmlFor="requestName" className="block font-bold mb-2 text-gray-700">
                            依頼名
                        </label>
                        <input
                            id="requestName"
                            type="text"
                            value={title}
                            onChange={(e) => setTitle(e.target.value)}
                            required
                            className="w-full py-2.5 px-3 border border-gray-300 rounded focus:ring-2 focus:ring-orange-500 focus:border-transparent text-base font-inherit box-border"
                        />
                    </div>
                    
                    <div className="mb-6">
                        <label htmlFor="description" className="block font-bold mb-2 text-gray-700">
                            説明
                        </label>
                        <textarea
                            id="description"
                            rows="3"
                            value={description}
                            onChange={(e) => setDescription(e.target.value)}
                            required
                            className="w-full py-2.5 px-3 border border-gray-300 rounded text-base font-inherit box-border resize-none"
                        />
                    </div>
                </div>

                {/* 評価項目 */}
                <div className="bg-white rounded-xl shadow-sm p-8 border border-orange-100">
                    <div className="flex items-center justify-between mb-6">
                        <h2 className="text-xl font-semibold text-gray-800 flex items-center">
                            <Users className="w-5 h-5 mr-2 text-orange-500" />
                            評価項目
                        </h2>
                    </div>

                    <div className="space-y-6">
                        {evaluationItems.map((item, itemIndex) => (
                            <fieldset key={itemIndex} className="border border-gray-300 rounded-lg p-6 mb-6">
                                <div className="flex items-center justify-between mb-4">
                                    <legend className="font-bold px-2 text-gray-800">
                                        評価項目 {itemIndex + 1}
                                    </legend>
                                    <button
                                        type="button"
                                        onClick={() => removeEvaluationItem(itemIndex)}
                                        className="py-1 px-3 border border-red-500 bg-red-50 rounded text-red-700 cursor-pointer font-bold text-sm hover:bg-red-100 transition-colors"
                                    >
                                        項目を削除
                                    </button>
                                </div>

                                <div className="mb-6">
                                    <label htmlFor={`itemName${itemIndex}`} className="block font-bold mb-2 text-gray-700">
                                        項目名
                                    </label>
                                    <input
                                        id={`itemName${itemIndex}`}
                                        type="text"
                                        value={item.name}
                                        onChange={(e) => handleItemNameChange(itemIndex, e.target.value)}
                                        required
                                        className="w-full py-2.5 px-3 border border-gray-300 rounded text-base font-inherit box-border"
                                    />
                                </div>

                                <div className="mb-6">
                                    <div className="flex items-center justify-between mb-3">
                                        <label className="block font-bold mb-2 text-gray-700">
                                            各段階の説明
                                        </label>
                                        <button
                                            type="button"
                                            onClick={() => addLevel(itemIndex)}
                                            className="py-1 px-3 border border-green-500 bg-green-50 rounded text-green-700 cursor-pointer font-bold text-sm hover:bg-green-100 transition-colors"
                                        >
                                            段階を追加
                                        </button>
                                    </div>
                                    
                                    {item.levels.map((level, levelIndex) => (
                                        <div key={levelIndex} className="flex items-center gap-2.5 mt-2">
                                            <span className="font-bold text-gray-700">{level.score}:</span>
                                            <textarea
                                                rows="2"
                                                value={level.description}
                                                onChange={(e) => handleLevelDescChange(itemIndex, levelIndex, e.target.value)}
                                                required
                                                className="flex-1 py-2.5 px-3 border border-gray-300 rounded text-base font-inherit box-border resize-none"
                                            />
                                            <button
                                                type="button"
                                                onClick={() => removeLevel(itemIndex, levelIndex)}
                                                className="w-8 h-8 bg-red-100 text-red-600 rounded-full flex items-center justify-center hover:bg-red-200 transition-colors cursor-pointer border-0 text-lg font-bold"
                                            >
                                                ×
                                            </button>
                                        </div>
                                    ))}
                                </div>
                            </fieldset>
                        ))}
                    </div>

                    <button
                        type="button"
                        onClick={addEvaluationItem}
                        className="py-2 px-4 border border-orange-500 bg-orange-50 rounded text-orange-700 cursor-pointer font-bold hover:bg-orange-100 transition-colors"
                    >
                        評価項目を追加
                    </button>
                </div>

                {/* 設定項目 */}
                <div className="bg-white rounded-xl shadow-sm p-8 border border-orange-100">
                    <h2 className="text-xl font-semibold text-gray-800 mb-6 flex items-center">
                        <Calendar className="w-5 h-5 mr-2 text-orange-500" />
                        詳細設定
                    </h2>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                        <div className="mb-6">
                            <label htmlFor="startDate" className="block font-bold mb-2 text-gray-700">
                                開始日
                            </label>
                            <input
                                id="startDate"
                                type="date"
                                value={startDate}
                                onChange={(e) => setStartDate(e.target.value)}
                                required
                                className="max-w-xs py-2.5 px-3 border border-gray-300 rounded text-base font-inherit box-border"
                            />
                        </div>

                        <div className="mb-6">
                            <label htmlFor="endDate" className="block font-bold mb-2 text-gray-700">
                                終了日
                            </label>
                            <input
                                id="endDate"
                                type="date"
                                value={endDate}
                                onChange={(e) => setEndDate(e.target.value)}
                                required
                                className="max-w-xs py-2.5 px-3 border border-gray-300 rounded text-base font-inherit box-border"
                            />
                        </div>

                        <div className="mb-6">
                            <label htmlFor="maxAnnotations" className="block font-bold mb-2 text-gray-700">
                                一人当たりのデータ数
                            </label>
                            <input
                                id="maxAnnotations"
                                type="number"
                                value={maxAnnotations}
                                onChange={(e) => setMaxAnnotations(e.target.value)}
                                className="max-w-xs py-2.5 px-3 border border-gray-300 rounded text-base font-inherit box-border"
                            />
                        </div>

                        <div className="mb-6">
                            <label htmlFor="threshold" className="block font-bold mb-2 text-gray-700">
                                テストの閾値
                            </label>
                            <input
                                id="threshold"
                                type="text"
                                value={threshold}
                                onChange={(e) => setThreshold(e.target.value)}
                                className="max-w-xs py-2.5 px-3 border border-gray-300 rounded text-base font-inherit box-border"
                            />
                        </div>
                    </div>

                    <div className="mb-6">
                        <label className="flex items-center">
                            <input
                                type="checkbox"
                                checked={isPrivate}
                                onChange={(e) => setIsPrivate(e.target.checked)}
                                className="w-5 h-5 mr-3"
                            />
                            <span className="font-bold text-gray-700">プライベートモード</span>
                        </label>
                    </div>
                </div>

                {/* ファイルアップロード */}
                <div className="bg-white rounded-xl shadow-sm p-8 border border-orange-100">
                    <h2 className="text-xl font-semibold text-gray-800 mb-6 flex items-center">
                        <Upload className="w-5 h-5 mr-2 text-orange-500" />
                        データファイル
                    </h2>

                    <div className="mb-6">
                        <label className="block font-bold mb-2 text-gray-700">
                            テストデータのアップロード (CSV)
                        </label>
                        <input
                            type="file"
                            accept=".csv"
                            onChange={(e) => setTestFile(e.target.files[0])}
                            className="w-full py-2.5 px-3 border border-gray-300 rounded text-base font-inherit box-border"
                        />
                    </div>

                    <div className="mb-6">
                        <label className="block font-bold mb-2 text-gray-700">
                            評価データのアップロード (CSV)
                        </label>
                        <input
                            type="file"
                            accept=".csv"
                            onChange={(e) => setDataFile(e.target.files[0])}
                            className="w-full py-2.5 px-3 border border-gray-300 rounded text-base font-inherit box-border"
                        />
                    </div>
                </div>

                {/* 送信ボタン */}
                <div className="mt-8 text-right">
                    <button
                        type="submit"
                        className="py-3 px-6 bg-orange-500 text-white border-0 rounded-lg text-lg font-bold cursor-pointer hover:bg-orange-600 transition-colors shadow-lg"
                    >
                        送信してタスクを作成
                    </button>
                </div>
            </form>
        </main>
    );
};

export default NewRequestPage;