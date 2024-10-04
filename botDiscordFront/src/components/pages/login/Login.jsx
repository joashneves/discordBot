import React from "react";
import LoginForm from "../../organisms/LoginForm/LoginForm";
import styles from './Login.module.css';

const Login = () =>{
    return(
        <>
        <div className={styles.centralizarDiv}>
        <LoginForm/>
        </div>
        </>
    )
}

export default Login;