import os
import textwrap

os.makedirs('src/api', exist_ok=True)
os.makedirs('src/context', exist_ok=True)
os.makedirs('src/components', exist_ok=True)
os.makedirs('src/pages', exist_ok=True)
os.makedirs('src/styles', exist_ok=True)

files = {}

files['vercel.json'] = """{
  "rewrites": [{ "source": "/(.*)", "destination": "/index.html" }]
}
"""

files['vite.config.js'] = """import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true
      }
    }
  }
})
"""

files['.env.example'] = """VITE_API_URL=http://localhost:8000/api
"""

files['index.html'] = """<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>ArtiHome — Furniture Without the Showroom Tax</title>
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;0,700;1,400;1,600&family=Outfit:wght@300;400;500;600&display=swap" rel="stylesheet" />
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.jsx"></script>
  </body>
</html>
"""

files['src/main.jsx'] = """import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'
import './styles/global.css'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)
"""

files['src/styles/global.css'] = """/* ── TOKENS ── */
:root {
  --bg:      #09090A;
  --surface: #111113;
  --border:  #1E1E22;
  --gold:    #C8A96A;
  --glow:    #E0C07C;
  --dim:     rgba(200,169,106,.18);
  --cream:   #F0E8D5;
  --text:    #9A9084;
  --muted:   #5A544C;
  --green:   #3EB575;
  --serif:   'Cormorant Garamond', Georgia, serif;
  --sans:    'Outfit', sans-serif;
}

/* ── RESET ── */
*,*::before,*::after { box-sizing:border-box; margin:0; padding:0; }
html { scroll-behavior:smooth; font-size:16px; }
body {
  background:var(--bg);
  color:var(--text);
  font-family:var(--sans);
  font-weight:400;
  -webkit-font-smoothing:antialiased;
  overflow-x:hidden;
  letter-spacing:.012em;
}
img { display:block; max-width:100%; }
a { text-decoration:none; color:inherit; }
button { cursor:pointer; font-family:var(--sans); }

/* ── GRAIN OVERLAY ── */
body::before {
  content:'';
  position:fixed; inset:0; z-index:999; pointer-events:none;
  opacity:.045;
  background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='200' height='200'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.68' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='200' height='200' filter='url(%23n)'/%3E%3C/svg%3E");
  background-size:160px 160px;
}

/* ── SCROLLBAR ── */
::-webkit-scrollbar { width:3px; }
::-webkit-scrollbar-track { background:var(--bg); }
::-webkit-scrollbar-thumb { background:var(--gold); border-radius:2px; }

/* ── ANIMATIONS ── */
@keyframes fadeUp   { from{opacity:0;transform:translateY(22px)} to{opacity:1;transform:translateY(0)} }
@keyframes shimmer  { 0%{background-position:-200% center} 100%{background-position:200% center} }
@keyframes pulse    { 0%,100%{opacity:1} 50%{opacity:.3} }
@keyframes floatY   { 0%,100%{transform:translateY(0)} 50%{transform:translateY(-8px)} }
@keyframes slideIn  { from{opacity:0;transform:translateX(-16px)} to{opacity:1;transform:translateX(0)} }

/* ── TYPOGRAPHY HELPERS ── */
.serif { font-family:var(--serif); }
.shimmer-text {
  background: linear-gradient(90deg, var(--gold) 0%, var(--glow) 40%, var(--gold) 60%, var(--glow) 100%);
  background-size:200% auto;
  -webkit-background-clip:text;
  -webkit-text-fill-color:transparent;
  background-clip:text;
  animation:shimmer 3.8s linear infinite;
}

/* ── CORE FORM AND BTN ── */
.btn-primary {
  background:var(--gold); color:#0A0900;
  border:none; padding:.88rem 1.9rem;
  border-radius:7px; font-size:.92rem; font-weight:600;
  transition:all .2s; letter-spacing:.02em;
  display:inline-flex; align-items:center; gap:.5rem; justify-content:center;
}
.btn-primary:hover { background:var(--glow); transform:translateY(-2px); }
.btn-ghost {
  background:transparent; color:var(--gold);
  border:1.5px solid rgba(200,169,106,.3);
  padding:.88rem 1.9rem; border-radius:7px;
  font-size:.92rem; font-weight:500;
  transition:all .2s; display:inline-flex; align-items:center; gap:.5rem; justify-content:center;
}
.btn-ghost:hover { border-color:var(--gold); transform:translateY(-2px); }

/* SCROLL REVEAL CLASS */
.reveal {
  opacity:0; transform:translateY(22px);
  transition:opacity .65s ease, transform .65s ease;
}
.reveal.visible { opacity:1; transform:translateY(0); }
"""

files['src/api/index.js'] = """import axios from 'axios';

const baseURL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

const API = axios.create({
  baseURL
});

API.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

API.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    if (error.response && error.response.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      try {
        const refresh = localStorage.getItem('refresh_token');
        if (!refresh) throw new Error('No refresh token');
        
        const res = await axios.post(`${baseURL}/accounts/token/refresh/`, { refresh });
        localStorage.setItem('access_token', res.data.access);
        
        // Retry original request
        originalRequest.headers.Authorization = `Bearer ${res.data.access}`;
        return axios(originalRequest);
      } catch (err) {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        localStorage.removeItem('user');
        window.location.href = '/login';
        return Promise.reject(err);
      }
    }
    return Promise.reject(error);
  }
);

export const register      = (data)       => API.post('/accounts/register/', data);
export const login         = (data)       => API.post('/accounts/login/', data);
export const logout        = ()           => API.post('/accounts/logout/');
export const getProducts   = (category)   => API.get('/products/', { params: category && category !== 'All' ? { category } : {} });
export const getProduct    = (id)         => API.get(`/products/${id}/`);
export const joinWaitlist  = (data)       => API.post('/waitlist/', data);
export const togglePledge  = (productId)  => API.post(`/waitlist/pledge/${productId}/`);
export const getMyWaitlist = ()           => API.get('/waitlist/mine/');
export const getPledgeCount= (productId)  => API.get(`/waitlist/count/${productId}/`);

export default API;
"""

files['src/context/AuthContext.jsx'] = """import React, { createContext, useState, useEffect } from 'react';
import { login as apiLogin, register as apiRegister, logout as apiLogout } from '../api';

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const storedUser = localStorage.getItem('user');
    if (storedUser) {
      setUser(JSON.parse(storedUser));
    }
    setLoading(false);
  }, []);

  const login = async (email, password) => {
    const { data } = await apiLogin({ email, password });
    localStorage.setItem('access_token', data.tokens.access);
    localStorage.setItem('refresh_token', data.tokens.refresh);
    localStorage.setItem('user', JSON.stringify(data.user));
    setUser(data.user);
  };

  const register = async (payload) => {
    const { data } = await apiRegister(payload);
    localStorage.setItem('access_token', data.tokens.access);
    localStorage.setItem('refresh_token', data.tokens.refresh);
    localStorage.setItem('user', JSON.stringify(data.user));
    setUser(data.user);
  };

  const logout = async () => {
    try {
      await apiLogout();
    } catch(e) {
      console.log('Logout API failed, clearing local storage anyway');
    }
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('user');
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, isLoggedIn: !!user, loading, login, logout, register }}>
      {children}
    </AuthContext.Provider>
  );
};
"""

files['src/App.jsx'] = """import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import ProtectedRoute from './components/ProtectedRoute';
import Navbar from './components/Navbar';
import Home from './pages/Home';
import Login from './pages/Login';
import Register from './pages/Register';
import MyWaitlist from './pages/MyWaitlist';

function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Navbar />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/my-waitlist" element={<ProtectedRoute><MyWaitlist /></ProtectedRoute>} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}

export default App;
"""

files['src/components/ProtectedRoute.jsx'] = """import React, { useContext } from 'react';
import { Navigate, useLocation } from 'react-router-dom';
import { AuthContext } from '../context/AuthContext';

function ProtectedRoute({ children }) {
  const { isLoggedIn, loading } = useContext(AuthContext);
  const location = useLocation();

  if (loading) return <div>Loading...</div>;

  if (!isLoggedIn) {
    return <Navigate to="/login" state={{ from: location.pathname }} />;
  }

  return children;
}

export default ProtectedRoute;
"""

files['src/components/Navbar.css'] = """nav {
  position:fixed; top:0; left:0; right:0; z-index:200;
  display:flex; align-items:center; justify-content:space-between;
  padding:.9rem 5vw;
  transition:background .3s, border .3s, backdrop-filter .3s;
}
nav.scrolled {
  background:rgba(9,9,10,.92);
  backdrop-filter:blur(20px);
  border-bottom:1px solid var(--border);
}
.nav-logo {
  font-family:var(--serif);
  font-size:1.4rem; font-weight:600;
  color:var(--cream); background:none; border:none;
  letter-spacing:-.01em;
}
.nav-logo span { color:var(--gold); }
.nav-cta {
  background:var(--gold); color:#0A0900;
  border:none; padding:.52rem 1.25rem;
  border-radius:6px; font-size:.83rem; font-weight:600;
  transition:background .2s, transform .2s;
  letter-spacing:.02em; display:inline-block;
}
.nav-cta:hover { background:var(--glow); transform:translateY(-1px); }

.nav-links {
  display:flex; align-items:center; gap:1.5rem;
}
.nav-link {
  font-size:.85rem; font-weight:500; color:var(--text); transition:color .2s;
}
.nav-link:hover { color:var(--cream); }
.nav-btn-logout {
  background:transparent; color:var(--muted); border:1px solid var(--border);
  padding:.4rem 1rem; border-radius:6px; font-size:.8rem; transition:all .2s;
}
.nav-btn-logout:hover { border-color:var(--gold); color:var(--gold); }
"""

files['src/components/Navbar.jsx'] = """import React, { useContext, useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { AuthContext } from '../context/AuthContext';
import './Navbar.css';

function Navbar() {
  const { user, isLoggedIn, logout } = useContext(AuthContext);
  const navigate = useNavigate();
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 40);
    window.addEventListener('scroll', onScroll);
    return () => window.removeEventListener('scroll', onScroll);
  }, []);

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  return (
    <nav className={scrolled ? 'scrolled' : ''}>
      <Link to="/" className="nav-logo">
        Arti<span>Home</span>
      </Link>
      
      <div className="nav-links">
        {!isLoggedIn ? (
          <>
            <Link to="/login" className="nav-link">Login</Link>
            <Link to="/register" className="nav-cta">Join Waitlist</Link>
          </>
        ) : (
          <>
            <span className="nav-link" style={{color: 'var(--cream)'}}>Hi, {user?.first_name || 'User'}</span>
            <Link to="/my-waitlist" className="nav-link">My Waitlist</Link>
            <button onClick={handleLogout} className="nav-btn-logout">Logout</button>
          </>
        )}
      </div>
    </nav>
  );
}

export default Navbar;
"""

files['src/pages/Auth.css'] = """.auth-page {
  min-height: 100vh;
  display: flex; align-items: center; justify-content: center;
  padding: 5rem 5vw;
  background: radial-gradient(circle at 50% 50%, rgba(200,169,106,.05) 0%, transparent 60%), var(--bg);
}
.auth-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 12px; padding: 2.5rem; width: 100%; max-width: 440px;
}
.auth-logo {
  font-family: var(--serif); font-size: 1.8rem; font-weight: 600;
  color: var(--cream); text-align: center; margin-bottom: 2rem;
}
.auth-logo span { color: var(--gold); }
.auth-form { display: flex; flex-direction: column; gap: 1.2rem; }
.auth-group { display: flex; flex-direction: column; gap: .4rem; }
.auth-label { font-size: .75rem; font-weight: 600; text-transform: uppercase; letter-spacing: .1em; color: var(--muted); }
.auth-input {
  background: var(--bg); border: 1.5px solid var(--border);
  padding: .85rem 1rem; border-radius: 8px; color: var(--cream); font-size: .95rem; font-family: var(--sans); outline: none; transition: border-color .2s;
}
.auth-input:focus { border-color: var(--gold); }
.row { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; }
.auth-error { color: #E57373; font-size: .85rem; background: rgba(229,115,115,.1); padding: .8rem; border-radius: 8px; }
.auth-link { color: var(--gold); font-size: .85rem; text-align: center; margin-top: 1.5rem; display: block; }
"""

files['src/pages/Login.jsx'] = """import React, { useState, useContext } from 'react';
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
"""

files['src/pages/Register.jsx'] = """import React, { useState, useContext } from 'react';
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
"""

files['src/pages/MyWaitlist.jsx'] = """import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { getMyWaitlist } from '../api';
import './Home.css'; // Reuse container styles

function MyWaitlist() {
  const [entries, setEntries] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getMyWaitlist().then(res => {
      setEntries(res.data);
      setLoading(false);
    }).catch(err => {
      console.error(err);
      setLoading(false);
    });
  }, []);

  return (
    <div style={{paddingTop: '6rem', minHeight: '100vh'}}>
      <section>
        <h2 className="section-title">My Waitlist Entries</h2>
        
        {loading ? (
          <p className="section-sub">Loading your entries...</p>
        ) : entries.length === 0 ? (
          <div style={{marginTop: '2rem'}}>
            <p className="section-sub" style={{marginBottom: '1.5rem'}}>You haven't joined any waitlists yet.</p>
            <Link to="/" className="btn-primary">Browse Products</Link>
          </div>
        ) : (
          <div className="products-grid" style={{marginTop: '2rem'}}>
            {entries.map(entry => (
              <div key={entry.id} className="product-card" style={{border: '1px solid rgba(62,181,117,.3)'}}>
                <div className="product-img">
                  <img src={entry.product.image} alt={entry.product.name} />
                  <span className="product-tag" style={{background:'rgba(62,181,117,.15)', color:'var(--green)', borderColor:'var(--green)'}}>Waitlisted</span>
                </div>
                <div className="product-body">
                  <p className="product-name">{entry.product.name}</p>
                  <p className="product-sub" style={{textTransform:'uppercase', fontSize:'.7rem'}}>{entry.product.category}</p>
                  <div className="product-prices">
                    <span className="price-ah">Rs. {entry.product.ah_price?.toLocaleString()}</span>
                  </div>
                  {entry.requirements && (
                    <div style={{marginTop:'.8rem', fontSize:'.8rem', color:'var(--text)', background:'var(--bg)', padding:'.5rem', borderRadius:'6px'}}>
                      <strong>Req:</strong> {entry.requirements}
                    </div>
                  )}
                  <p style={{fontSize:'.75rem', color:'var(--muted)', marginTop:'.8rem'}}>Joined on {new Date(entry.created_at).toLocaleDateString()}</p>
                </div>
              </div>
            ))}
          </div>
        )}
      </section>
    </div>
  );
}

export default MyWaitlist;
"""

for path, content in files.items():
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
