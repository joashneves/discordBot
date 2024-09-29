from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine('sqlite:///dados.db')
Base = declarative_base()
_Sessao = sessionmaker(engine)
class Usuario(Base):
    __tablename__ = 'usuarios'

    id = Column(Integer, primary_key=True)
    id_discord = Column(Integer)

Base.metadata.create_all(engine)