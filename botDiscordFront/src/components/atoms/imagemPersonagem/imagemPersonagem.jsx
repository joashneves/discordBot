import React, { useEffect, useState } from 'react';
import axios from 'axios';

const ImagemPersonagem = ({ nome, idFranquia }) => {
    const [imagemUrl, setImagemUrl] = useState('');
    const [errorMessage, setErrorMessage] = useState('');
    const [nomeFranquia, setNomeFranquia] = useState('');

    useEffect(() => {
        // Carregar a imagem do personagem assim que o componente for montado
        const buscarImagem = async () => {
            setErrorMessage(''); // Limpa mensagens de erro anteriores
            try {
                console.log(`/DownloadPersonagemByName?nome=${encodeURIComponent(nome)}&franquia=${encodeURIComponent(nomeFranquia)}`)
                const response = await fetch(`${import.meta.env.VITE_REACT_APP_LINK}Personagems/DownloadPersonagemByName?nome=${encodeURIComponent(nome)}&franquia=${encodeURIComponent(nomeFranquia)}`);

                if (!response.ok) {
                    const errorData = await response.json();
                    setErrorMessage(errorData.mensagem || 'Ocorreu um erro ao buscar a imagem.');
                    return;
                }

                // Obtém a URL da imagem da resposta
                const blob = await response.blob();
                const url = URL.createObjectURL(blob);
                setImagemUrl(url);
            } catch (error) {
                setErrorMessage('Ocorreu um erro ao buscar a imagem: ' + error.message);
            }
        };

        // Função para buscar o nome da franquia com base no idFranquia
        const fetchFranquia = async () => {
            try {
                const responde_franquia = await axios.get(`${import.meta.env.VITE_REACT_APP_LINK}Franquias/${idFranquia}`);
                const data_franquia = responde_franquia.data;
                setNomeFranquia(data_franquia.name);
            } catch (err) {
                console.log(err);
                setErrorMessage('Erro ao carregar a franquia.');
            }
        };

        fetchFranquia().then(() => buscarImagem());
    }, [nome, idFranquia]); // Dependências para atualizar ao mudar nome ou idFranquia

    const handleDownload = () => {
        // Lógica para download da imagem
        const link = document.createElement('a');
        link.href = imagemUrl;
        link.download = `${nome}.png`; // Altere a extensão conforme necessário
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    };

    return (
        <div>
            {errorMessage && <p style={{ color: 'red' }}>{errorMessage}</p>}
            {imagemUrl && (
                <div>
                    <h2>Imagem do Personagem:</h2>
                    <img src={imagemUrl} alt={`Imagem de ${nome}`} style={{ maxWidth: '300px', maxHeight: '300px' }} />
                    <button onClick={handleDownload}>Baixar Imagem</button>
                </div>
            )}
        </div>
    );
};

export default ImagemPersonagem;
