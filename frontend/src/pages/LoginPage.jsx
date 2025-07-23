import { useState, useEffect, useCallback } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import axios from 'axios';
import styles from './LoginPage.module.css';

const api = axios.create({
  baseURL: 'http://127.0.0.1:5001/api',
  withCredentials: true,
});

const logoUrl = '/logo.png';

const LoginPage = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [csrfToken, setCsrfToken] = useState('');
  const navigate = useNavigate();

  const fetchCsrfToken = useCallback(async () => {
    try {
      const { data } = await api.get('/csrf-token');
      setCsrfToken(data.csrfToken);
    } catch (err) {
      console.error('Failed to fetch CSRF token:', err);
      setError('ページの読み込みに失敗しました。リフレッシュしてください。');
    }
  }, []);

  useEffect(() => {
    fetchCsrfToken();
  }, [fetchCsrfToken]);

  /**
   * Hashes a password using PBKDF2 with SHA-256, matching the Python backend.
   * @param {string} password - The password to hash.
   * @param {string} salt - The salt to use for hashing.
   * @returns {Promise<string>} The hex-encoded hashed password.
   */
  const hashPassword = async (password, salt) => {
    const encoder = new TextEncoder();
    const passwordBuffer = encoder.encode(password);
    const saltBuffer = encoder.encode(salt);

    const key = await window.crypto.subtle.importKey(
      'raw',
      passwordBuffer,
      { name: 'PBKDF2' },
      false,
      ['deriveBits']
    );

    const derivedBits = await window.crypto.subtle.deriveBits(
      {
        name: 'PBKDF2',
        salt: saltBuffer,
        iterations: 10000,
        hash: 'SHA-256',
      },
      key,
      256
    );

    const hashArray = Array.from(new Uint8Array(derivedBits));
    const hashHex = hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
    return hashHex;
  };

  const handleLogin = async (e) => {
    e.preventDefault();
    setError('');

    if (!username || !password) {
      setError('ユーザー名とパスワードを入力してください。');
      return;
    }

    if (!csrfToken) {
      setError('CSRFトークンが取得できませんでした。ページをリフレッシュしてください。');
      return;
    }

    setIsLoading(true);

    try {
      const saltResponse = await api.post('/get-salt', { username });
      const { salt } = saltResponse.data;

      if (!salt) {
        throw new Error('ソルトの取得に失敗しました。');
      }

      const hashedPassword = await hashPassword(password, salt);

      const loginPayload = {
        username,
        password: hashedPassword,
        csrfToken,
        userAgent: navigator.userAgent,
        timestamp: new Date().toISOString(),
      };

      const { data } = await api.post('/login', loginPayload);

      if (data.success) {
        localStorage.setItem('accessToken', data.token);
        localStorage.setItem('refreshToken', data.refreshToken);
        api.defaults.headers.common['Authorization'] = `Bearer ${data.token}`;
        navigate('/dashboard', { state: { user: data.user } });
      } else {
        setError(data.message || 'ログインに失敗しました。');
      }
    } catch (err) {
      console.error('Login request failed:', err);
      if (err.response && err.response.data && err.response.data.message) {
        setError(err.response.data.message);
      } else {
        setError('ログイン処理中にエラーが発生しました。');
      }
    } finally {
      setIsLoading(false);
      fetchCsrfToken();
    }
  };

  return (
    <div className={styles.background}>
      <div className={styles.centerBox}>
        <img src={logoUrl} alt="Annotopia Logo" className={styles.logo} />
        <h1 className={styles.title}>ログイン</h1>
        <form className={styles.form} onSubmit={handleLogin}>
          <input
            type="text"
            className={styles.input}
            placeholder="ユーザー名"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            disabled={isLoading}
          />
          <input
            type="password"
            className={styles.input}
            placeholder="パスワード"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            disabled={isLoading}
          />
          {error && <p className={styles.error}>{error}</p>}
          <button
            type="submit"
            className={styles.loginButton}
            disabled={isLoading}
          >
            {isLoading ? 'ログイン中...' : 'Log in'}
          </button>
        </form>
        <p className={styles.signInLink}>
          アカウントをお持ちでないですか？ <Link to="/signin">新規登録</Link>
        </p>
      </div>
    </div>
  );
};

export default LoginPage;
