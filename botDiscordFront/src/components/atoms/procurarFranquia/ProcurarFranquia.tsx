import React, { useState } from 'react';
import styles from './ProcurarFranquia.module.css';

const ProcurarFranquia = ({ setFiltros }) => {
  const [nome, setNome] = useState('');
  const [descricao, setDescricao] = useState('');
  const [dataPublished, setDataPublished] = useState('');
  const [creator, setCreator] = useState('');

  const handleSearch = () => {
    // Envia os filtros para o componente pai
    setFiltros({ nome, descricao, data_Published: dataPublished, creator });
  };

  return (
    <article className={styles.mainContainer}>
      <h1>Buscar por Franquia</h1>
      <div className={styles.procurarContainer}>
        <input
          type="text"
          placeholder="Procurar por Nome..."
          value={nome}
          onChange={(e) => setNome(e.target.value)}
          className={styles.inputProcurar}
        />
        <input
          type="text"
          placeholder="Procurar por Descrição..."
          value={descricao}
          onChange={(e) => setDescricao(e.target.value)}
          className={styles.inputProcurar}
        />
        <input
          type="date"
          value={dataPublished}
          onChange={(e) => setDataPublished(e.target.value)}
          className={styles.inputProcurar}
        />
        <input
          type="text"
          placeholder="Procurar por Criador..."
          value={creator}
          onChange={(e) => setCreator(e.target.value)}
          className={styles.inputProcurar}
        />
        <button onClick={handleSearch} className={styles.botaoBuscar}>
          Buscar
        </button>
      </div>
    </article>
  );
}

export default ProcurarFranquia;
