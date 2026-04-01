import React, { useState, useContext } from 'react';
import { useNavigate, useLocation, Link } from 'react-router-dom';
import { AuthContext } from '../context/AuthContext';
import './Auth.css';

function Login() {
  const { login } = useContext(AuthContext);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();
  const location = useLocation();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await login(email, password);
      const from = location.state?.from || '/';
      navigate(from, { replace: true });
    } catch (err) {
      setError(err.response?.data?.detail || 'Login failed. Check your credentials.');
    }
  };

  return (
    <div className="auth-page">
      <div className="auth-card">
        <div className="auth-logo">Arti<span>Home</span></div>
        {error && <div className="auth-error">{error}</div>}
        <form className="auth-form" onSubmit={handleSubmit}>
          <div className="auth-group">
            <label className="auth-label">Email</label>
            <input type="email" required className="auth-input" value={email} onChange={e => setEmail(e.target.value)} />
          </div>
          <div className="auth-group">
            <label className="auth-label">Password</label>
            <input type="password" required className="auth-input" value={password} onChange={e => setPassword(e.target.value)} />
          </div>
          <button type="submit" className="btn-primary" style={{width: '100%', marginTop:'.5rem'}}>Log In</button>
        </form>
        <Link to="/register" className="auth-link">Don't have an account? Create one</Link>
      </div>
    </div>
  );
}

export default Login;
