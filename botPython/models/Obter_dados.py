from models.db import _Sessao, Usuario

class Obter_dados():
    def obter_usuario(id_discord):
        with _Sessao() as sessao:
            usuario_db = sessao.query(Usuario).filter_by(id_discord=id_discord).first()
            if not usuario_db:
                usuario_db = Usuario(id_discord=id_discord)
                sessao.add(usuario_db)
                sessao.commit()
        return usuario_db