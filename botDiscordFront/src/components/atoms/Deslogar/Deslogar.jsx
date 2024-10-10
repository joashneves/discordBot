import { useNavigate } from 'react-router-dom';
import styles from './Deslogar.module.css';

const Deslogar = () => {
    const navigate = useNavigate();

    const handleLogout = () => {
        // Limpa o sessionStorage
        sessionStorage.clear();

        // Redireciona para a página de login
        navigate('/');
    };

    return (
        <>
            <button className={styles.deslogarbotao} onClick={handleLogout}>
                Sair
            </button>
        </>
    );
}

export default Deslogar;
