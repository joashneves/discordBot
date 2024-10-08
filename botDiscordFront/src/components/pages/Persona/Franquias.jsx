import React from "react";
import styles from './Franquias.module.css';
import Coluna from "../../molecules/coluna/Coluna";
import ListaFranquia from "../../organisms/ListaFranquia/ListaFranquia";
import CadastrarFranquia from "../../organisms/CadastrarFranquia/CadastrarFranquia";

const Franquias = () => {
    return (
        <>
            <div className={styles.paginaPrincipal}>
                <Coluna />
                <div className={styles.mainContent}>
                    <CadastrarFranquia/>
                    <ListaFranquia />
                </div>

            </div>
        </>
    )
}

export default Franquias;