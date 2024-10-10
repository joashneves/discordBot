import { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import styles from './AtualizarUsuario.module.css';
import axios from "axios";
import Deslogar from "../../atoms/Deslogar/Deslogar";



const AtualizarUsuario = () => {
    const { email } = useParams(); // Pegando o email do usuário da URL
    const navigate = useNavigate(); // Para redirecionar após a atualização
    const [user , setUser] = useState(sessionStorage.getItem('user'));
    const [senhaAntiga, setSenhaAntiga] = useState('');
    const [novaSenha, setNovaSenha] = useState();
    const [error, setError] = useState(null); // Estado para tratar erros
    const [userdata, setUserData] = useState({
        user: 'string',
        email: 'string',
        senhaAntiga: 'string',
        novaSenha: '',
    });

    // Função para buscar os dados do usuário quando o componente é montado
    useEffect(() => {
            const user = sessionStorage.getItem('user'); 
            const token = sessionStorage.getItem('accessToken');
            const fetchUsuario = async () => {
                try {
                    const response = await axios.get(`${import.meta.env.VITE_REACT_APP_LINK}Contas/user/${user}`, {
                        headers: {
                            Authorization: `Bearer ${token}` // Adiciona o token aqui
                        }
                    }
                    );
                    const usuario = response.data;
                    setUserData(response.data);
                    
                } catch (error) {
                    console.error('Erro ao buscar usuário:', error);
                    setError("Erro ao carregar os dados do usuário.");
                }
            };
            fetchUsuario();
        
    }, [user]);

    // Função para enviar o PUT request ao servidor e atualizar os dados
    const handleSubmit = async (event) => {
        event.preventDefault();

        const usuarioObj = {
            userName: user,
            email: userdata.email,
            senhaAntiga: senhaAntiga,
            novaSenha: novaSenha,
        };
        // Recupera o token do sessionStorage
        const token = sessionStorage.getItem('accessToken');
        const userName = sessionStorage.getItem('user');
        try {
            console.log(usuarioObj)
            await axios.put(
                `${import.meta.env.VITE_REACT_APP_LINK}Contas/atualizar`, usuarioObj,
                {
                    headers: {
                        'Authorization': `Bearer ${token}`, // Adiciona o token ao cabeçalho
                        'Content-Type': 'application/json'
                    }
                }
            );
            navigate(`/`); // Redirecionar após o sucesso
        } catch (error) {
            // Verifica se o erro é de não autorizado (status 401)
            if (error.response?.status === 401) {
                setError('Você não está autorizado a atualizar este usuário.');
            } else {
                setError('Erro ao atualizar o usuário.');
            }
        }
    };

    return (
        <div className={styles.corDeFundo}>
            <h1>Conta - {user}</h1>
            {error && <p className={styles.error}>{error}</p>}
            <form onSubmit={handleSubmit} className={styles.formAtualizar}>
                <div className={styles.campopreencher}>
                    <label>
                        Nome de Usuário:
                    </label>
                    <input
                        type="text"
                        name="user"
                        value={user}
                        readOnly
                    />
                </div>
                <div className={styles.campopreencher}>
                    <label>
                        Email:
                    </label>
                    <input
                        type="email"
                        name="email"
                        value={userdata.email}
                        readOnly
                    />
                </div>
                <div className={styles.campopreencher}>
                    <label>
                        Senha Antiga:
                    </label>
                    <input
                        type="password"
                        name="senhaAntiga"
                        onChange={(e) => setSenhaAntiga(e.target.value)}
                        required
                    />
                </div>
                <div className={styles.campopreencher}>
                    <label>
                        Senha Nova:
                    </label>
                    <input
                        type="password"
                        name="senhaNova"
                        onChange={(e) => setNovaSenha(e.target.value)}
                        required
                    />
                </div>
                <div>
                <button type="submit" className={styles.submitButton}>Atualizar</button>
                <hr/>
                <Deslogar/>
                </div>

            </form>
        </div>
    );
};

export default AtualizarUsuario;
