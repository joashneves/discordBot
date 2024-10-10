import { useState, useEffect } from "react";
import axios from "axios";
import UsuarioTemplateLista from "../../atoms/UsuarioTemplateLista/UsuarioTemplateLista";

const UsuarioLista = () => {
    const [Usuario, setUsuario] = useState([]); // Estado para armazenar a lista de Usuario

    const [pageNumber, setPageNumber] = useState(0); // Página atual
    const pageQuantity = 8; // Quantidade de boletins por página
    // useEffect para buscar os Usuario quando o componente for montado
    useEffect(() => {

        const token = sessionStorage.getItem('accessToken');
        axios.get(`${import.meta.env.VITE_REACT_APP_LINK}Contas/Pag?pageNumber=${pageNumber}&pageQuantity=${pageQuantity}`, {
            headers: {
                Authorization: `Bearer ${token}` // Adiciona o token aqui
            }
        }) // Substitua pela URL da sua API
            .then(response => {
                setUsuario(response.data); // Armazena os Usuario no estado
            })
            .catch(error => {
                console.error('Erro ao buscar Usuario:', error);
            });
    }, [pageNumber]); // O array vazio [] faz com que o useEffect execute apenas uma vez após a montagem do componente

    const handleNextPage = () => {
        setPageNumber(pageNumber + 1);
    };

    const handlePreviousPage = () => {
        if (pageNumber > 0) setPageNumber(pageNumber - 1);
    };

    return (
        <>
            {Usuario.length > 0 ? (
                Usuario.slice().reverse().map((usuario) => (
                    <UsuarioTemplateLista 
                    name = {usuario.name}
                    user={usuario.userName}
                    email={(usuario.email)} 
                    nivel={usuario.nivel}/>
                ))
            ) : (
                <p>Carregando Usuario...</p>
            )}
            <div>
                <button onClick={handlePreviousPage} disabled={pageNumber === 0}>
                    Página Anterior
                </button>
                <span>{pageNumber + 1}</span>
                <button onClick={handleNextPage}>
                    Próxima Página
                </button>
            </div>
        </>
    );
}

export default UsuarioLista;