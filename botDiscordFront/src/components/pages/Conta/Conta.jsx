import React from "react";
import styles from './Conta.module.css';

import AtualizarUsuario from "../../organisms/AtualizarUsuario/AtualizarUsuario";
import Coluna from "../../molecules/coluna/Coluna";



const Conta = () =>{
    return(
        <>
        <div className={styles.paginaPrincipal}> 
            <Coluna />
            <div className={styles.mainContent}>
            <AtualizarUsuario/>
            </div>
        </div>
        </>
    )
}

export default Conta;