import commonStyles from './OrderPage.module.css'; // mainの基本スタイルを共通で利用
import formStyles from './NewRequestPage.module.css';   // このページ固有のフォームスタイル

const NewRequestPage = () => {
  return (
    <main className={commonStyles.main}>
      <form className={formStyles.formContainer}>
        {/* === ページタイトル === */}
        <h2 className={formStyles.title}>機械翻訳の評価</h2>
        <p className={formStyles.description}>英日翻訳の正確さを3段階で評価してください</p>

        {/* === 基本情報 === */}
        <div className={formStyles.formGroup}>
          <label htmlFor="requestName">依頼名</label>
          <input id="requestName" type="text" defaultValue="機械翻訳の評価" />
        </div>
        <div className={formStyles.formGroup}>
          <label htmlFor="description">説明</label>
          <textarea id="description" rows="3" defaultValue="英日翻訳の正確さを3段階で評価してください"></textarea>
        </div>
        <div className={formStyles.formGroup}>
          <label htmlFor="itemCount">評価項目の個数</label>
          <input id="itemCount" type="number" defaultValue="1" className={formStyles.shortInput} />
        </div>

        {/* === 評価項目1 === */}
        <fieldset className={formStyles.fieldset}>
          <legend>評価項目1</legend>
          <div className={formStyles.formGroup}>
            <label htmlFor="itemName1">項目名</label>
            <input id="itemName1" type="text" defaultValue="正確さ" />
          </div>
          <div className={formStyles.formGroup}>
            <label htmlFor="levels1">段階</label>
            <input id="levels1" type="number" defaultValue="3" className={formStyles.shortInput} />
          </div>
          <div className={formStyles.formGroup}>
            <label>各段階の説明</label>
            <div className={formStyles.levelDescription}>
              <span>3:</span>
              <textarea rows="2" defaultValue="原文の意味を完全に伝えており、情報の欠落や誤訳がまったくない。"></textarea>
            </div>
            <div className={formStyles.levelDescription}>
              <span>2:</span>
              <textarea rows="2" defaultValue="原文の意味の半分以上は伝えているが、重要な情報の抜けや軽微な誤訳がある。"></textarea>
            </div>
            <div className={formStyles.levelDescription}>
              <span>1:</span>
              <textarea rows="2" defaultValue="原文の意味をほとんどまたは全く伝えていない。意味が通らないか、全く異なる内容になっている。"></textarea>
            </div>
          </div>
        </fieldset>
        
        {/* === 設定項目 === */}
        <div className={formStyles.formGroup}>
          <label>プライベートモード</label>
          <input type="checkbox" className={formStyles.toggle} />
        </div>
        <div className={formStyles.formGroup}>
          <label>期間</label>
          <div className={formStyles.dateRange}>
            <input type="text" defaultValue="2025/8/1" />
            <span>〜</span>
            <input type="text" defaultValue="2025/8/7" />
          </div>
        </div>
        <div className={formStyles.formGroup}>
            <label>テストの有無</label>
            <input type="checkbox" className={formStyles.toggle} />
        </div>
        <div className={formStyles.formGroup}>
          <label htmlFor="testThreshold">テストの閾値</label>
          <input id="testThreshold" type="text" defaultValue="0.5" className={formStyles.shortInput} />
        </div>

        {/* === データアップロード === */}
        <div className={formStyles.formGroup}>
          <label>テストデータのアップロード</label>
          <button type="button" className={formStyles.uploadButton}>ファイルを選択</button>
        </div>
        <div className={formStyles.formGroup}>
          <label>評価データのアップロード</label>
          <button type="button" className={formStyles.uploadButton}>ファイルを選択</button>
        </div>
        
        {/* === 送信ボタン === */}
        <div className={formStyles.submitContainer}>
          <button type="submit" className={formStyles.submitButton}>送信</button>
        </div>
      </form>
    </main>
  );
};

export default NewRequestPage;