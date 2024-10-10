import { useState } from "react";
import styles from './CadastrarUsuario.module.css';
import axios from "axios";

const CadastrarUsuario = () => {
    const [name, setName] = useState('');
    const [user, setUser] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState(null);
    const [success, setSuccess] = useState(null);
    const [loading, setLoading] = useState(false);

    const handleSubmit = async (event) => {
        event.preventDefault();

        const usuarioDTO = {
            name: name,
            username: user,
            email: email,
            password: password,
        };

        const token = sessionStorage.getItem('accessToken');
        const userName = sessionStorage.getItem('user')

        setLoading(true);

        try {
            const response = await axios.post(
                `${import.meta.env.VITE_REACT_APP_LINK}Contas`,
                usuarioDTO,
                {
                    headers: {
                        Authorization: `Bearer ${token}`
                    }
                }
            );
            setSuccess('Usuário cadastrado com sucesso!');
            setError(null);

            // Atualiza a página após o sucesso
            window.location.reload();
        } catch (error) {
            if (error.response?.status === 401) {
                setError('Você não está autorizado a cadastrar o usuário.');
            } else {
                setError('Ocorreu um erro ao cadastrar o usuário.');
            }
            setSuccess(null);
        } finally {
            setLoading(false);
        }
    };

    return (
        <article className={styles.mainCadastrar}>
            <h1>Cadastrar Usuário</h1>
            <form className={styles.formCadastrar} onSubmit={handleSubmit}>
                <div className={styles.secaoPreencher}>
                    <label htmlFor="nome">Nome:</label>
                    <input
                        className={styles.inputCadastrar}
                        type="text"
                        id="nome"
                        value={name}
                        onChange={(e) => setName(e.target.value)}
                        required
                        disabled={loading} // Desabilita o campo se estiver carregando
                    />
                </div>
                <div className={styles.secaoPreencher}>
                    <label htmlFor="user">Usuario:</label>
                    <input
                        className={styles.inputCadastrar}
                        type="text"
                        id="User"
                        value={user}
                        onChange={(e) => setUser(e.target.value)}
                        required
                        disabled={loading} // Desabilita o campo se estiver carregando
                    />
                </div>
                <div className={styles.secaoPreencher}>
                    <label htmlFor="email">Email:</label>
                    <input
                        className={styles.inputCadastrar}
                        type="email"
                        id="email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        required
                        disabled={loading} // Desabilita o campo se estiver carregando
                    />
                </div>
                <div className={styles.secaoPreencher}>
                    <label htmlFor="senha">Senha:</label>
                    <input
                        className={styles.inputCadastrar}
                        type="password"
                        id="senha"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        required
                        disabled={loading} // Desabilita o campo se estiver carregando
                    />
                </div>
                <button type="submit" className={styles.botaoCadastrar} disabled={loading}>
                    {loading ? 'Cadastrando...' : 'Cadastrar'}
                </button>
            </form>
            {error && <p style={{ color: 'red' }}>{error}</p>}
            {success && <p style={{ color: 'green' }}>{success}</p>}
        </article>
    );
};

export default CadastrarUsuario;