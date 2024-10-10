import React from "react";
import styles from './Conta.module.css';

import Coluna from "../../molecules/Coluna/Coluna";
import AtualizarUsuario from "../../organisms/AtualizarUsuario/AtualizarUsuario";



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