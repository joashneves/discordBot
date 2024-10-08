import React from 'react';
import styles from './PersonagemTemplate.module.css';
import { useNavigate } from 'react-router-dom'; 
import ImagemPersonagem from '../imagemPersonagem/imagemPersonagem';

// Mapeamento do GenderEnum para emoticons e cores
const genderMapping = {
    0: { label: 'Feminino', emoji: '👩', color: '#FF69B4' }, // Rosa
    1: { label: 'Masculino', emoji: '👨', color: '#1E90FF' }, // Azul
    2: { label: 'Não Binário', emoji: '⚧️', color: '#FFD700' }, // Dourado
    3: { label: 'Fluido', emoji: '🌈', color: '#FF4500' }, // Laranja
    4: { label: 'Outros', emoji: '🤷', color: '#808080' }, // Cinza
};

const PersonagemTemplate = (props) => {
    const navigate = useNavigate();

    // Obtém o mapeamento do gênero com base no valor do enum
    const genderInfo = genderMapping[props.gender];

    return (
        <>
            <div className={styles.corDefundo}> 
                <div>
                    <p>Nome :</p>
                    <p>{props.name}</p> {/* Corrigido para props.name */}
                </div>
                <div>
                    <p>Gênero :</p>
                    {genderInfo ? (
                        <p style={{ color: genderInfo.color }}>
                            {genderInfo.emoji} {genderInfo.label}
                        </p>
                    ) : (
                        <p>Gênero desconhecido</p>
                    )}
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
