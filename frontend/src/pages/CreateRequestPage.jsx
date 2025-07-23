import React, { useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import styles from './CreateRequestPage.module.css';
import { useAuth } from '../hooks/useAuth';

const CreateRequestPage = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { logout } = useAuth();
  const user = location.state?.user;

  useEffect(() => {
    if (!user) {
      navigate('/');
    }
  }, [user, navigate]);

  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [file, setFile] = useState(null);
  const [error, setError] = useState('');
  const [successMessage, setSuccessMessage] = useState('');

  const handleFileChange = (e) => {
    setFile(e.target.files[0] || null);
  };

  if (!user) return null;

  const handleSubmit = (e) => {
    e.preventDefault();
    setError('');
    setSuccessMessage('');

    if (!title || !description || !file) {
      setError('すべてのフィールドを入力し、ファイルを添付してください。');
      return;
    }

    // console.log({ title, description, fileName: file.name });
    setSuccessMessage('依頼が正常に送信されました。');
    
    setTimeout(() => {
        navigate('/dashboard', { state: { user } });
    }, 2000);
  };

  const handleCancel = () => {
    navigate('/dashboard', { state: { user } });
  };

  return (
    <div className={styles.background}>
    <div className={styles.pageContainer}>
      <header className={styles.header}>
        <div className={styles.logoContainer}>
          <img src="/logo.png" alt="ANNOTOPIA Logo" className={styles.logo} />
          <span className={styles.logoText}>ANNOTOPIA</span>
        </div>
        <div className={styles.userMenu}>
          <span className={styles.username}>こんにちは、{user?.username}さん</span>
          <button onClick={logout} className={styles.logoutButton}>ログアウト</button>
        </div>
      </header>

      <main className={styles.main}>
        <h1 className={styles.heading}>新しい依頼の作成</h1>
        <p className={styles.subheading}>アノテーションを依頼したい内容を入力してください。</p>

        <form className={styles.form} onSubmit={handleSubmit}>
          {/* Form groups... */}
          <div className={styles.formGroup}>
            <label htmlFor="title" className={styles.label}>依頼タイトル</label>
            <input
              type="text"
              id="title"
              className={styles.input}
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              placeholder="例：道路標識のバウンディングボックス作成"
            />
          </div>

          <div className={styles.formGroup}>
            <label htmlFor="description" className={styles.label}>作業内容の詳細</label>
            <textarea
              id="description"
              className={styles.textarea}
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              placeholder="作業の詳細な手順や注意点を記入してください。"
            />
          </div>

          <div className={styles.formGroup}>
            <label className={styles.label}>対象ファイルのアップロード</label>
            <input
              type="file"
              id="file-upload"
              onChange={handleFileChange}
              style={{ display: 'none' }}
            />
            <label htmlFor="file-upload" className={styles.fileDropzone}>
              <p>クリックまたはドラッグ＆ドロップでファイルを選択</p>
              {file && <p className={styles.fileName}>選択中のファイル: {file.name}</p>}
            </label>
          </div>

          {error && <p className={styles.error}>{error}</p>}
          {successMessage && <p className={styles.success}>{successMessage}</p>}

          <div className={styles.buttonGroup}>
            <button type="button" className={styles.cancelButton} onClick={handleCancel}>
              キャンセル
            </button>
            <button type="submit" className={styles.submitButton}>
              依頼を送信する
            </button>
          </div>
        </form>
      </main>
    </div>
    </div>
  );
};

export default CreateRequestPage;