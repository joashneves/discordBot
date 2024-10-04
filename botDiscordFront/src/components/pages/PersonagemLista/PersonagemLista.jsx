import React from "react";
import styles from './PersonagemLista.module.css';
import Coluna from "../../molecules/coluna/Coluna";
import ListaPersonagens from "../../organisms/ListaPersonagem/ListaPersonagem";

const PersonagemLista = () => {

    

    return (
        <>
            <div className={styles.paginaPrincipal}>
                <Coluna />
                <div className={styles.mainContent}>
                <ListaPersonagens idFranquia={1} />
                </div>

            </div>
        </>
    )
}

export default PersonagemLista;