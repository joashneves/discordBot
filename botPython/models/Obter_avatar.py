from models.db import _Sessao, AvatarSalvo

class Obter_Avatar():
    def obter_Avatar(id_discord:str,caminho_arquiv:str, data_arquivo:str):
        with _Sessao() as sessao:
            servidor_db = sessao.query(AvatarSalvo).filter_by(id_discord=id_discord).first()
            if not servidor_db:
                new_chat = AvatarSalvo(id_discord=id_discord,
                                        caminho_arquiv=caminho_arquiv,
                                        data_arquivo=data_arquivo)
                sessao.add(new_chat)

                sessao.commit()
        return servidor_db
    
    def verificar_chat(guild_id: str, channel_id: str) -> bool:
        with _Sessao() as sessao:
            chat = sessao.query(AvatarSalvo).filter_by(
                guild_id=guild_id, channel_id=channel_id
            ).first()
            return chat is not None  # Retorna True se o chat já existir
