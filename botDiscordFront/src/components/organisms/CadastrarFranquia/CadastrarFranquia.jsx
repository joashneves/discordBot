import React, { useState } from 'react';
import styles from './CadastrarFranquia.module.css';
import axios from 'axios';


const CadastrarFranquia = () => {
    // Define o estado para os campos do formulário
    const [name, setName] = useState('');
    const [descricao, setDescricao] = useState('');
    const [creator, setCreator] = useState(''); 
    const [attachment, setAttachment] = useState(''); 
    const [data_Published , setData_Published] = useState(''); 
    const [error, setError] = useState(null);
    const [success, setSuccess] = useState(null);

    const handleSubmit = async (event) => {
        event.preventDefault();

        // Cria o objeto do DTO
        const franquiaDTO = {
            name: name,
            description: descricao,
            creator: creator,
            attachment: attachment,
            data_Published: data_Published
        };

        // Recupera o token do sessionStorage
        const token = sessionStorage.getItem('accessToken');
        const userName = sessionStorage.getItem('user');

        try {
            console.log(franquiaDTO)
            // Faz a requisição POST usando Axios, incluindo o token no cabeçalho
            const response = await axios.post(
                `${import.meta.env.VITE_REACT_APP_LINK}Franquias`, 
                franquiaDTO,
                {
                    headers: {
                        Authorization: `Bearer ${token}` // Adiciona o token aqui
                    }
                }
            );
            

            setSuccess('Franquia cadastrado com sucesso!');
            setError(null);
            window.location.reload();
        } catch (error) {
            // Verifica se o erro é de não autorizado (status 401)
            if (error.response?.status === 401) {
                setError('Você não está autorizado a cadastrar a Franquia.');
            } else {
                setError('Ocorreu um erro ao cadastrar o A franquia.');
            }
            setSuccess(null);
        }
    };

    return (
        <>
            <article className={styles.mainCadastrar}>
                <h1>Cadastrar Franquia</h1>
                <form className={styles.formCadastrar} onSubmit={handleSubmit}>
                    <div className={styles.secaoPreencher}>
                        <label htmlFor="nome">Nome:</label>
                        <input
                            className={styles.inputCadastrar}
                            type="text"
                            id="nome"
                            value={name}
                            onChange={(e) => setName(e.target.value)}
                            placeholder="Digite o nome da franquia"
                        />
                    </div>
                    <div className={styles.secaoPreencher}>
                        <label htmlFor="descricao">Descrição:</label>
                        <textarea
                            className={styles.inputCadastrarDescricao}
                            id="descricao"
                            value={descricao}
                            onChange={(e) => setDescricao(e.target.value)}
                            maxLength={300}
                            rows={6} // Número de linhas visíveis
                            placeholder="Digite a descrição da franquia"
                        />
                    </div>
                    <div className={styles.secaoPreencher}>
                        <label htmlFor="criador">Criador:
                        <input
                        className={styles.inputCadastrar}
                        type="text"
                        id="criador"
                        value={creator}
                        onChange={(e) => setCreator(e.target.value)}
                        placeholder="Digite o nome do criador"/>
                  </label>
                    </div>
                    <div className={styles.secaoPreencher}>
                        <label htmlFor="percente">Pertencente:
                        <input
                        className={styles.inputCadastrar}
                        type="text"
                        id="percente"
                        value={attachment}
                        onChange={(e) => setAttachment(e.target.value)}
                        placeholder="Digite o pertecente da franquia"/>
                  </label>
                    </div>
                    <div className={styles.secaoPreencher}>
                        <label htmlFor="data">Data de publicação:
                        <input
                        className={styles.inputCadastrar}
                        type="date"
                        id="data"
                        onChange={(e) => setData_Published(e.target.value)}
                        placeholder="Digite o nome do criador"/>
                  </label>
                    </div>
                    <button type="submit" className={styles.botaoCadastrar}>
                        Cadastrar
                    </button>
                </form>
                {error && <p style={{ color: 'red' }}>{error}</p>}
                {success && <p style={{ color: 'green' }}>{success}</p>}
            </article>
        </>
    );
};

export default CadastrarFranquia;
