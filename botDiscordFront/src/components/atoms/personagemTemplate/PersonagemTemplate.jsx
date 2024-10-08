import React from 'react';
import styles from './PersonagemTemplate.module.css';
import { useNavigate } from 'react-router-dom'; 
import ImagemPersonagem from '../imagemPersonagem/imagemPersonagem';

const PersonagemTemplate = (props) => {
  const navigate = useNavigate();
  return (
    <>
      <div className={styles.corDefundo} > 
        <div>
          <p>Nome :</p>
          <p>{props.name}</p> {/* Corrigido para props.name */}
        </div>
        <div>
          <p>Genero :</p>
          <p>{props.gender}</p> {/* Corrigido para props.description */}
        </div>
        <div>
            <ImagemPersonagem idFranquia={props.idFranquia} nome={props.name}/>
        </div>
      </div>
      <hr />
    </>
  );
}

export default PersonagemTemplate;
