from sqlalchemy import Column, Integer, String, Float
from database import Base
class ProdutoDB(Base):
    __tablename__ = 'produtos'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    preco = Column(Float, nullable=False)
    quantidade = Column(Integer, nullable=False)
class SaopauloDB(Base):
    __tablename__ = 'saopaulo'

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    titulos = Column(Integer, nullable=False)
    cores = Column(String(100), nullable=False)
    idade = Column(Integer, nullable=False)
