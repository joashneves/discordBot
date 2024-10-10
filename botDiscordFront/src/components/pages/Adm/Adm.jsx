import React from "react";
import styles from './Conta.module.css';

import Coluna from "../../molecules/coluna/Coluna";
import CadastrarUsuario from "../../organisms/CadastrarUsuario/CadastrarUsuario";



const Adm = () =>{
    return(
        <>
        <div className={styles.paginaPrincipal}> 
            <Coluna />
            <div className={styles.mainContent}>
            <CadastrarUsuario/>
            </div>
        </div>
        </>
    )
}

export default Adm;