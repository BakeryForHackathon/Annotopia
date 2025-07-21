import { useState } from 'react';
import { useNavigate } from 'react-router-dom'; // 画面遷移のためにインポート
import axios from 'axios'; // axiosをインポート
import styles from './LoginPage.module.css';

const logoUrl = '/public/logo.png';

const LoginPage = () => {
  // 入力値を管理するためのState
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate(); // useNavigateフックを使用

  // ログインボタンが押されたときの処理
  const handleLogin = async () => {
    // ユーザー名かパスワードが空の場合は何もしない
    if (!username || !password) {
      alert('ユーザー名とパスワードを入力してください。');
      return;
    }

    try {
      // バックエンドの/api/loginエンドポイントにPOSTリクエストを送信
      const response = await axios.post('http://127.0.0.1:5001/api/login', {
        username: username,
        password: password,
      });

      // レスポンスのJSONから成功したか確認
      if (response.data.success) {
        // ログイン成功
        alert('ログインに成功しました！');
        // 次の画面（例: /dashboard）に遷移。stateでユーザー情報を渡す
        navigate('/dashboard', { state: { user: response.data.user } });
      } else {
        // ログイン失敗
        alert('ユーザー名またはパスワードが違います。');
      }
    } catch (error) {
      // ネットワークエラーなど
      console.error('ログインリクエストに失敗しました:', error);
      alert('ログイン処理中にエラーが発生しました。');
    }
  };

  return (
    <div className={styles.background}>
      <div className={styles.centerBox}>
        <img src={logoUrl} alt="Annotopia Logo" className={styles.logo} />
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
          {/* ボタンクリックでhandleLoginを呼び出す */}
          <button className={styles.loginButton} onClick={handleLogin}>
            Log in
          </button>
        </div>
      </div>
    </div>
  );
};

export default LoginPage;