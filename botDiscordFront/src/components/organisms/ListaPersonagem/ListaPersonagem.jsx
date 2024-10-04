import React, { useEffect, useState } from 'react';
import axios from 'axios';
import PersonagemTemplate from '../../atoms/personagemTemplate/PersonagemTemplate'; // Certifique-se de ter esse componente

const ListaPersonagens = ({ idFranquia }) => {
  const [personagens, setPersonagens] = useState([]); // Inicializando como array vazio
  const [pageNumber, setPageNumber] = useState(0); // Página atual
  const pageQuantity = 10; // Quantidade de personagens por página

  // Buscar personagens com base na franquia e paginação
  useEffect(() => {
    console.log(idFranquia)
    axios.get(`${import.meta.env.VITE_REACT_APP_LINK}Personagems/franquia/${idFranquia}?pageNumber=${pageNumber}&pageQuantity=${pageQuantity}`)
      .then(response => {
        setPersonagens(response.data || []); // Acessa o array de personagens corretamente
      })
      .catch(error => {
        console.error('Erro ao buscar personagens:', error);
      });
  }, [idFranquia, pageNumber]);

  // Funções para mudar de página
  const handleNextPage = () => {
    setPageNumber(pageNumber + 1);
  };

  const handlePreviousPage = () => {
    if (pageNumber > 0) setPageNumber(pageNumber - 1);
  };

  return (
    <>
      {personagens.length > 0 ? (
        personagens.map((personagem) => (
          <PersonagemTemplate
            key={personagem.id}
            id={personagem.id}
            name={personagem.name}
            gender={personagem.gender}
            caminhoArquivo={personagem.caminhoArquivo}
          />
        ))
      ) : (
        <p>Nenhum personagem encontrado.</p>
      )}

      {/* Botões de paginação */}
      <div>
        <button onClick={handlePreviousPage} disabled={pageNumber === 0}>
          Página Anterior
        </button>
        <span>{pageNumber + 1}</span>
        <button onClick={handleNextPage}>
          Próxima Página
        </button>
      </div>
    </>
  );
}

export default ListaPersonagens;
