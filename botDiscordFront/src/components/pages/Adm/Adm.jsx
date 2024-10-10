import React from "react";
import styles from './Conta.module.css';

import Coluna from "../../molecules/coluna/Coluna";
import CadastrarUsuario from "../../organisms/CadastrarUsuario/CadastrarUsuario";
import UsuarioLista from "../../organisms/UsuarioLista/UsuarioLista";



const Adm = () =>{
    return(
        <>
        <div className={styles.paginaPrincipal}> 
            <Coluna />
            <div className={styles.mainContent}>
            <CadastrarUsuario/>
            <UsuarioLista/>
            </div>
        </div>
        </>
    )
}

export default Adm;