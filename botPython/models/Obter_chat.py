from models.db import _Sessao, ServidorConfig

class Obter_chat():
    def obter_chat(guild_id:str,channel_id:str):
        with _Sessao() as sessao:
            servidor_db = sessao.query(ServidorConfig).filter_by(guild_id=guild_id).first()
            if not servidor_db:
                new_chat = ServidorConfig(guild_id=guild_id, channel_id=channel_id)
                sessao.add(new_chat)

                sessao.commit()
        return servidor_db
    
    def verificar_chat(guild_id: str, channel_id: str) -> bool:
        with _Sessao() as sessao:
            chat = sessao.query(ServidorConfig).filter_by(
                guild_id=guild_id, channel_id=channel_id
            ).first()
            return chat is not None  # Retorna True se o chat já existir
