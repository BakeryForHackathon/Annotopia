import { useNavigate } from 'react-router-dom';
import { useCallback } from 'react';

/**
 * Custom hook to manage authentication-related logic.
 * This centralizes the logout functionality.
 * @returns {{logout: function}}
 */
export const useAuth = () => {
  const navigate = useNavigate();

  const logout = useCallback(() => {
    // Clear user session data from storage
    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');
    // Navigate to the login page
    navigate('/login');
  }, [navigate]);

  return { logout };
};