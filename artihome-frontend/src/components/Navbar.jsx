import React, { useContext, useEffect, useState } from 'react';
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
        <img src="/logo-sofa.svg" alt="ArtiHome" className="nav-logo-img" />
        <span className="nav-logo-text">Arti<span className="nav-logo-accent">Home</span></span>
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
