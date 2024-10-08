import React from "react";
import styles from './PersonagemLista.module.css';
import Coluna from "../../molecules/coluna/Coluna";
import ListaPersonagens from "../../organisms/ListaPersonagem/ListaPersonagem";
import { useParams } from "react-router-dom";
import EnviarPersonagem from "../../organisms/EnviarPersonagem/EnviarPersonagem";

const PersonagemLista = () => {

    const { id } = useParams(); // Obter o :id da URL
    const idFranquia = parseInt(id, 10); // Converter o id para um número

    return (
        <>
            <div className={styles.paginaPrincipal}>
                <Coluna />
                <div className={styles.mainContent}>
                <EnviarPersonagem/>
                <ListaPersonagens idFranquia={id} />
                </div>

            </div>
        </>
    )
}

export default PersonagemLista;