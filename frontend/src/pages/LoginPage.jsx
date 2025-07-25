import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import styles from './LoginPage.module.css';

// 本番環境と開発環境でAPIエンドポイントを切り替える
const API_URL = 'https://myapp-backend-oyx2.onrender.com';

const logoUrl = '/logo.png';

const LoginPage = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState(''); // エラーメッセージ表示用のState
  const navigate = useNavigate();

  // 入力値のバリデーションを行う関数
  const validateInput = () => {
    if (!username || !password) {
      return 'ユーザー名とパスワードを入力してください。';
    }
    if (username.length < 4) {
      return 'ユーザー名は4文字以上で入力してください。';
    }
    if (password.length < 8) {
      return 'パスワードは8文字以上で入力してください。';
    }
    // 簡易的なXSS/SQLインジェクション対策 (サーバーサイドでの対策が本命)
    const invalidChars = /['"<>;`]/;
    if (invalidChars.test(username) || invalidChars.test(password)) {
      return '入力に使用できない文字が含まれています。';
    }
    return null; // 問題なければnullを返す
  };

  const handleLogin = async () => {
    // 1. クライアントサイドでのバリデーションを実行
    const validationError = validateInput();
    if (validationError) {
      setError(validationError);
      return;
    }
    setError(''); // バリデーションが通ったらエラーメッセージをクリア

    try {
      // 2. Cookieベースのセッション管理のため `withCredentials: true` を設定
      const response = await axios.post(`${API_URL}/api/login`, {
        username: username,
        password: password,
      }, {
        withCredentials: true, // セッションCookieの送受信に必要
      });

      if (response.data.success) {
        alert('ログインに成功しました！');
        // 3. セッション管理はCookieに任せ、ページ遷移のみ行う
        // 遷移先のページで必要な一時的な情報はstateで渡す
        navigate('/order', { state: { user: response.data.user } });
      } else {
        // サーバーが認証失敗を返した場合
        setError('ユーザー名またはパスワードが違います。');
      }
    } catch (err) {
      // ネットワークエラーやサーバーエラー
      console.error('ログインリクエスト失敗:', err);
      setError('ログイン処理中にエラーが発生しました。しばらくしてから再度お試しください。');
    }
  };

  return (
    <div className={styles.background}>
      <div className={styles.centerBox}>
        <img src={logoUrl} alt="Annotopia Logo" className={styles.logo} />
        {/* エラーメッセージがある場合に表示 */}
        {error && <p className={styles.errorMessage}>{error}</p>}
        <div className={styles.form}>
          <input
            type="text"
            className={styles.input}
            placeholder="ユーザー名"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
          <input
            type="password"
            className={styles.input}
            placeholder="パスワード"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
          <button className={styles.loginButton} onClick={handleLogin}>
            Log in
          </button>
        </div>
      </div>
    </div>
  );
};

export default LoginPage;