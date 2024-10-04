import React from 'react';
import styles from './FranquiaTemplate.module.css';
import { useNavigate } from 'react-router-dom'; 

const FranquiaTemplate = (props) => {
  const navigate = useNavigate();
  return (
    <>
      <div className={styles.corDefundo} onClick={() => navigate(`/personagens/${props.id}`)}> 
        <div>
          <p>Nome :</p>
          <p>{props.name}</p> {/* Corrigido para props.name */}
        </div>
        <div>
          <p>Descrição :</p>
          <p>{props.description}</p> {/* Corrigido para props.description */}
        </div>
        <div>
          <p>Criador :</p>
          <p>{props.creator}</p> {/* Corrigido para props.creator */}
        </div>
        <div>
          <p>Pertence :</p>
          <p>{props.attachment}</p> {/* Corrigido para props.attachment */}
        </div>
        <div>
          <p>Data de Publicação :</p>
          <p>{props.data_Published}</p> {/* Corrigido para props.data_Published */}
        </div>
      </div>
      <hr />
    </>
  );
}

export default FranquiaTemplate;
