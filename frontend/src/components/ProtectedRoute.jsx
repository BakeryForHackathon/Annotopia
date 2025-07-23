import React from 'react';
import { Navigate, useLocation } from 'react-router-dom';

/**
 * A component that acts as a guard for routes that require authentication.
 * It checks for an access token in localStorage. If not present, it redirects
 * the user to the /login page.
 * @param {{children: React.ReactNode}} props
 */
const ProtectedRoute = ({ children }) => {
  const location = useLocation();
  const accessToken = localStorage.getItem('accessToken');

  if (!accessToken) {
    // Redirect them to the /login page, but save the current location they were
    // trying to go to. This allows us to send them along to that page after a
    // successful login.
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  return children;
};

export default ProtectedRoute;