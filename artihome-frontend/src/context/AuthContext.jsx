import React, { createContext, useState, useEffect } from 'react';
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
    const authTokens = data.token || data.tokens;
    localStorage.setItem('access_token', authTokens.access);
    localStorage.setItem('refresh_token', authTokens.refresh);
    localStorage.setItem('user', JSON.stringify(data.user));
    setUser(data.user);
  };

  const register = async (payload) => {
    const { data } = await apiRegister(payload);
    const authTokens = data.token || data.tokens;
    localStorage.setItem('access_token', authTokens.access);
    localStorage.setItem('refresh_token', authTokens.refresh);
    localStorage.setItem('user', JSON.stringify(data.user));
    setUser(data.user);
  };

  const logout = async () => {
    try {
      await apiLogout();
    } catch(e) {
      if (import.meta.env.DEV) {
        console.error('Logout API failed, clearing local storage anyway', e);
      }
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
