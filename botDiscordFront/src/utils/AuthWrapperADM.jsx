import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

const AuthWrapperADM = () => {
  const navigate = useNavigate();

  useEffect(() => {
    const checkAuth = () => {
      const token = sessionStorage.getItem('accessToken');
      const user = sessionStorage.getItem('user'); 
      const password = sessionStorage.getItem('password'); 
      if (!token) {
        // Se não houver token, redireciona para o login
        navigate('/');
      }
    };

    checkAuth();
  }, [navigate]);

  return <>{children}</>;
};

export default AuthWrapperADM;