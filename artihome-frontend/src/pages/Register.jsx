import React, { useState, useContext } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { AuthContext } from '../context/AuthContext';
import './Auth.css';

function Register() {
  const { register } = useContext(AuthContext);
  const [form, setForm] = useState({
    first_name: '', last_name: '', email: '', phone: '', city: '', password: '', confirm_password: ''
  });
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    if(form.password !== form.confirm_password) {
      return setError('Passwords do not match');
    }
    try {
      await register(form);
      navigate('/');
    } catch (err) {
      const msgs = err.response?.data;
      if (typeof msgs === 'object') {
        setError(Object.values(msgs).flat().join(', '));
      } else {
        setError('Registration failed.');
      }
    }
  };

  const handleChange = e => setForm({...form, [e.target.name]: e.target.value});

  return (
    <div className="auth-page">
      <div className="auth-card">
        <div className="auth-logo">Arti<span>Home</span></div>
        {error && <div className="auth-error">{error}</div>}
        <form className="auth-form" onSubmit={handleSubmit}>
          <div className="row">
            <div className="auth-group">
              <label className="auth-label">First Name</label>
              <input name="first_name" required className="auth-input" value={form.first_name} onChange={handleChange} />
            </div>
            <div className="auth-group">
              <label className="auth-label">Last Name</label>
              <input name="last_name" required className="auth-input" value={form.last_name} onChange={handleChange} />
            </div>
          </div>
          <div className="auth-group">
            <label className="auth-label">Email</label>
            <input name="email" type="email" required className="auth-input" value={form.email} onChange={handleChange} />
          </div>
          <div className="row">
            <div className="auth-group">
              <label className="auth-label">Phone</label>
              <input name="phone" required className="auth-input" value={form.phone} onChange={handleChange} />
            </div>
            <div className="auth-group">
              <label className="auth-label">City</label>
              <input name="city" required className="auth-input" value={form.city} onChange={handleChange} />
            </div>
          </div>
          <div className="auth-group">
            <label className="auth-label">Password</label>
            <input name="password" type="password" required minLength={8} className="auth-input" value={form.password} onChange={handleChange} />
          </div>
          <div className="auth-group">
            <label className="auth-label">Confirm Password</label>
            <input name="confirm_password" type="password" required minLength={8} className="auth-input" value={form.confirm_password} onChange={handleChange} />
          </div>
          <button type="submit" className="btn-primary" style={{width: '100%', marginTop:'.5rem'}}>Create Account</button>
        </form>
        <Link to="/login" className="auth-link">Already have an account? Log in</Link>
      </div>
    </div>
  );
}

export default Register;
