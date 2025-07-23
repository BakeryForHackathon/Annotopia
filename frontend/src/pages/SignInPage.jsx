import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import styles from './SignInPage.module.css';

const logoUrl = '/logo.png';

const SignInPage = () => {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();

  const handleSignIn = async (e) => {
    e.preventDefault();
    setError('');

    if (!username || !email || !password) {
      setError('すべてのフィールドを入力してください。');
      return;
    }
    if (!/\S+@\S+\.\S+/.test(email)) {
      setError('有効なメールアドレスを入力してください。');
      return;
    }

    setIsLoading(true);

    // console.log('Submitting registration for:', { username, email });
    
    setTimeout(() => {
      try {
        alert('登録が完了しました。ログインページに移動します。');
        navigate('/');
      } catch (apiError) {
        setError('登録に失敗しました。時間をおいて再度お試しください。');
      } finally {
        setIsLoading(false);
      }
    }, 1500);
  };

  return (
    <div className={styles.background}>
      <div className={styles.centerBox}>
        <img src={logoUrl} alt="ANNOTOPIA Logo" className={styles.logo} />
        <h1 className={styles.title}>アカウント登録</h1>
        <form className={styles.form} onSubmit={handleSignIn}>
          <input
            type="text"
            className={styles.input}
            placeholder="ユーザー名"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            disabled={isLoading}
          />
          <input
            type="email"
            className={styles.input}
            placeholder="メールアドレス"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
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
            className={styles.signInButton}
            disabled={isLoading}
          >
            {isLoading ? '登録中...' : '登録する'}
          </button>
        </form>
        <p className={styles.loginLink}>
          すでにアカウントをお持ちですか？ <Link to="/">ログイン</Link>
        </p>
      </div>
    </div>
  );
};

export default SignInPage;
