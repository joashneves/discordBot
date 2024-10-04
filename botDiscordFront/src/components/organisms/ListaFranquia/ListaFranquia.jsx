import React, { useEffect, useState } from 'react';
import axios from 'axios';
import FranquiaTemplate from '../../atoms/franquiaTemplate/FranquiaTemplate';
import ProcurarFranquia from '../../atoms/procurarFranquia/ProcurarFranquia';

const ListaFranquia = () => {
  const [franquias, setFranquias] = useState([]); // Inicializando como array vazio
  const [filtros, setFiltros] = useState({
    nome: '',
    descricao: '',
    data_Published: '',
    creator: '',
  });

  const [pageNumber, setPageNumber] = useState(0); // Página atual
  const pageQuantity = 10; // Quantidade de franquias por página

  // Buscar franquias com paginação
  useEffect(() => {
    axios.get(`${import.meta.env.VITE_REACT_APP_LINK}Franquias/Pag?pageNumber=${pageNumber}&pageQuantity=${pageQuantity}`)
      .then(response => {
        setFranquias(response.data.franquias || []); // Acessa o array de franquias corretamente
      })
      .catch(error => {
        console.error('Erro ao buscar franquias:', error);
      });
  }, [pageNumber]);

  // Filtrar franquias com base nos filtros
  const franquiasFiltradas = (franquias || []).filter((franquia) => {  // Garante que franquias seja um array
    const filtroNome = franquia.name.toLowerCase().includes(filtros.nome.toLowerCase());
    const filtroDescricao = franquia.description.toLowerCase().includes(filtros.descricao.toLowerCase());

    const filtroData = filtros.data_Published ? (
      new Date(franquia.data_Published).toISOString().split('T')[0] === new Date(filtros.data_Published).toISOString().split('T')[0]
    ) : true;

    const filtroCreator = filtros.creator ? franquia.creator === filtros.creator : true;

    return filtroNome && filtroDescricao && filtroData && filtroCreator;
  });

  // Funções para mudar de página
  const handleNextPage = () => {
    setPageNumber(pageNumber + 1);
  };

  const handlePreviousPage = () => {
    if (pageNumber > 0) setPageNumber(pageNumber - 1);
  };

  return (
    <>
      <ProcurarFranquia setFiltros={setFiltros} /> {/* Componente para busca de franquias */}
      {franquiasFiltradas.length > 0 ? (
        franquiasFiltradas.slice().reverse().map((franquia) => (
          <FranquiaTemplate
            key={franquia.id}
            id={franquia.id}
            name={franquia.name}
            description={franquia.description}
            creator={franquia.creator}
            data_Published={new Date(franquia.data_Published).toLocaleDateString()}
            attachment={franquia.attachment}
          />
        ))
      ) : (
        <p>Nenhuma franquia encontrada.</p>
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

export default ListaFranquia;
