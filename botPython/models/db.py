from sqlalchemy import create_engine, Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine('sqlite:///dados.db')
Base = declarative_base()
_Sessao = sessionmaker(engine)
class Usuario(Base):
    __tablename__ = 'usuarios'

    id = Column(Integer, primary_key=True)
    id_discord = Column(Integer)
    apelido = Column(String, default='apelido')
    usuario = Column(String, default='usuario')
    descricao = Column(String, default='descrição')
    pronome = Column(String, default='N/a')
    level = Column(Integer, default=0)
    xp = Column(Integer, default=0)
    saldo = Column(Integer, default=0)
    data_criacao = Column(Integer, default=0)

class ServidorConfig(Base):
    __tablename__ = 'servidorConfig'

    id = Column(Integer, primary_key=True, index=True)
    guild_id = Column(String, nullable=False, index=True)  # ID do Servidor
    channel_id = Column(String, nullable=False, index=True)  # ID do Canal

class AvatarSalvo(Base):
    __tablename__ = 'AvataresDiscord'

    id = Column(Integer, primary_key=True)
    id_discord = Column(String, nullable=False)
    caminho_arquiv = Column(String, nullable=False)
    hash_avatar = Column(String, nullable=False)
    data_arquivo = Column(DateTime, nullable=False)  # Data da captura

Base.metadata.create_all(engine)