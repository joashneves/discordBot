import React from "react";
import styles from './Home.module.css';
import Coluna from "../../molecules/coluna/Coluna";

const Home = () =>{

    return(
        <>
        <div className={styles.paginaPrincipal}>
            <Coluna/>
        <div className={styles.mainContent}>
            
        </div>
        </div>
        </>
    )
}

export default Home;