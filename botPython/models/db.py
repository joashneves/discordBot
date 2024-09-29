from sqlalchemy import create_engine, Column, String, Integer, ForeignKey
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

Base.metadata.create_all(engine)