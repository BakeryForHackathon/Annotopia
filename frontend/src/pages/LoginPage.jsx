import { useState, useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import CryptoJS from 'crypto-js';
import axios from 'axios';
import styles from './LoginPage.module.css';
import { ApiContext, UserContext } from '../App';

const logoUrl = '/logo.png';

const LoginPage = () => {
  const [username, setUsername] = useState('');
  const [usernameHash, setUsernameHash] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();
  const API_URL = useContext(ApiContext);
  const { setUserId } = useContext(UserContext);

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


  function handleChange(e) {
    const value = e.target.value;
    setUsername(value);

    const hash = CryptoJS.SHA256(value).toString(CryptoJS.enc.Hex);
    setUsernameHash(hash);
  }

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
        setUserId(response.data.user.id);
        navigate('/order');
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
            onChange={(e) => handleChange(e)}
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