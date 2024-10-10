import { useEffect, useState } from "react";
import styles from './UsuarioTemplateLista.module.css'
import axios from "axios";

const UsuarioTemplateLista = (props) => {
    const [atualizacao, setAtualizacao] = useState(true);
    const usernameAdm = sessionStorage.getItem('user')
    const [username, setUsername] = useState(props.user)
    const [email, setEmail] = useState(props.email)
    const [novaSenha, setNovaSenha] = useState()
    const [novoNivel, setNovonivel] = useState(1);

    const atualizarBotao = () => {
        if (atualizacao) {
            setAtualizacao(false)
        } else {
            setAtualizacao(true)
        }
    }
    const enviarCoisa = async (event) => {
        event.preventDefault();

        const userNameADM = sessionStorage.getItem('user')
        const usuarioDTO = {
            userNameADM: userNameADM,
            username: username,
            email: email,
            novaSenha: novaSenha,
            novoNivel: novoNivel
        };
        console.log(usuarioDTO)
        const token = sessionStorage.getItem('accessToken');
        try {
            const response = await axios.put(
                `${import.meta.env.VITE_REACT_APP_LINK}Contas/resetar`,
                usuarioDTO,
                {
                    headers: {
                        Authorization: `Bearer ${token}`
                    }
                }
            );
            // Atualiza a página após o sucesso
            window.location.reload();
        } catch (error) {
            if (error.response?.status === 401) {
                console.log('Você não está autorizado a cadastrar o usuário.');
            } else {
                console.error(error);
            }
        }
    };

    return (
        <>
            {atualizacao ? (
                <div className={styles.corDefundo}>
                    <div><p>Nome : {props.name}</p></div>
                    <div><p>Username : {props.user}</p></div>
                    <div><p>Email : {props.email}</p></div>
                    <div><p>Nivel : {props.nivel}</p></div>
                    <button className={styles.atualizarbotao} onClick={atualizarBotao}>
                        Atualizar
                    </button>
                </div>
            ) : (
                <div className={styles.corDefundo}>
                    <div className={styles.atualizarUsuario}>
                        <div className={styles.campopreencher}>
                            <label>
                                Nome de Usuário:
                            </label>
                            <input
                                type="text"
                                name="user"
                                value={props.user}
                                readOnly
                            />
                        </div>
                        <div className={styles.campopreencher}>
                            <label>
                                Email:
                            </label>
                            <input
                                type="email"
                                name="email"
                                value={props.email}
                                readOnly
                            />
                        </div>
                        <div className={styles.campopreencher}>
                            <label>
                                Nova Senha:
                            </label>
                            <input
                                type="password"
                                name="senhaAntiga"
                                onChange={(e) => setNovaSenha(e.target.value)}
                                required
                            />
                        </div>
                        <div className={styles.campopreencher}>
                            <label>
                                Nivel :
                            </label>
                            <input
                                type="number"
                                name="senhaNova"
                                onChange={(e) => setNovonivel(e.target.value)}
                                required
                            />
                        </div>
                        <div>

                        </div>
                        <button className={styles.cancelarbotao} onClick={atualizarBotao}>
                            Cancelar
                        </button>
                        <button className={styles.atualizarbotao} onClick={enviarCoisa}  >
                            Atualizar
                        </button>
                    </div>
                </div>

            )
            }
            <hr />
        </>

    );
}

export default UsuarioTemplateLista;