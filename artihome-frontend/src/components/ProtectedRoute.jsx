import React, { useContext } from 'react';
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
