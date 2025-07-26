import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import styles from './LoginPage.module.css';

// 本番環境と開発環境でAPIエンドポイントを切り替える
const API_URL = 'http://127.0.0.1:5001';

const logoUrl = '/logo.png';

const LoginPage = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

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
    const invalidChars = /['"<>;`]/;
    if (invalidChars.test(username) || invalidChars.test(password)) {
      return '入力に使用できない文字が含まれています。';
    }
    return null;
  };

  const handleLogin = async () => {
    const validationError = validateInput();
    if (validationError) {
      setError(validationError);
      return;
    }
    setError('');

    try {
      const response = await axios.post(`${API_URL}/api/login`, {
        username: username,
        password: password,
      }, {
        withCredentials: true,
      });

      if (response.data.success) {
        navigate('/order', { state: { user: response.data.user } });
      } else {
        setError('ユーザー名またはパスワードが違います。');
      }
    } catch (err) {
      console.error('ログインリクエスト失敗:', err);
      if (err.response && err.response.data && err.response.data.message) {
        setError(err.response.data.message);
      } else {
        setError('ログイン処理中にエラーが発生しました。しばらくしてから再度お試しください。');
      }
    }
  };

  return (
    <div className={styles.background}>
      <div className={styles.centerBox}>
        <img src={logoUrl} alt="Annotopia Logo" className={styles.logo} />
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