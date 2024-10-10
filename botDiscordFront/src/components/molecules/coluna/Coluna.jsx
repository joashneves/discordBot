import { useState, useEffect} from 'react';
import { useNavigate } from 'react-router-dom'; // Importa o useNavigate
import styles from './Coluna.module.css';

const Coluna = () => {
    const navigate = useNavigate(); // Hook do React Router
    const [administrador, setAdministrador] = useState(false);

    useEffect(() => {
        const checkAuth = () => {
          const token = sessionStorage.getItem('accessToken');
          if (token) {
            setAdministrador(true);
          }
        };
    
        checkAuth();
      }, [navigate]);

    return (
        <>
            <header>
                <article className={styles.colunaMain}>
                    <p
                        className={styles.conteudo_link}
                        onClick={() => navigate('/Home')} // Redireciona para a página inicial
                    >
                        Início
                    </p>
                    <p
                        className={styles.conteudo_link}
                        onClick={() => navigate('/Persona')} // Redireciona para a página de Poersonages
                    >
                        Personagens
                    </p>
                    {administrador ? (<p
                        className={styles.conteudo_link}
                        onClick={() => navigate('/adm')} // Redireciona para a página de Administradores
                    >
                        Administrador
                    </p>) : (<></>)}
                    <p
                        className={styles.conteudo_link}
                        onClick={() => navigate('/Conta')} // Redireciona para a página de conta do usuario
                    >
                        Contas
                    </p>

                    
                </article>
            </header>
        </>
    );
}

export default Coluna;
