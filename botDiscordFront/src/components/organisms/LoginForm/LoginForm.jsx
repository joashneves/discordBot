import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import styles from './LoginForm.module.css';
import axios from 'axios';

const LoginForm = () => {
    const [userName, setUserOrEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const navigate = useNavigate();
  
    const handleLogin = async (e) => {
      e.preventDefault();
      try {
        const response = await axios.post(`${import.meta.env.VITE_REACT_APP_LINK}Contas/login`, {
          userName,
          password,
        });
        console.log(response.data)
        // Acessa o token aninhado dentro de response.data.token.token
        const token  = response.data?.token?.token;
            // Verifica se a resposta contém um token
        if (token) {
          sessionStorage.setItem('accessToken', token); // Salva o token no sessionStorage
        }
        sessionStorage.setItem('user', userName); 
        sessionStorage.setItem('password', password); 
  
        // Redireciona para a página desejada após o login
        navigate('/Home');
      } catch (err) {
        console.log(err)
        setError('Falha ao realizar o login. Verifique suas credenciais.');
      }
    };

    return (
        <article className={styles.principalForm}>
            <h2>Login</h2>
            <form onSubmit={handleLogin} className={styles.form}>
                <div className={styles.formGroup}>
                    <label htmlFor="username">Username:</label>
                    <input
                        type="text"
                        id="username"
                        value={userName}
                        onChange={(e) => setUserOrEmail(e.target.value)}
                        required
                        className={styles.preencherInput}
                    />
                </div>
                <div className={styles.formGroup}>
                    <label htmlFor="password">Password:</label>
                    <input
                        type="password"
                        id="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        required
                        className={styles.preencherInput}
                    />
                </div>
                <button type="submit" value="Cadastrar" className={styles.botaologin}>Login</button>
            </form>
        </article>
    );
};


export default LoginForm;
