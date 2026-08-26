from typing import Annotated, List

from fastapi import Depends, FastAPI, HTTPException, Path
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from database import Base, engine, get_db
from models import ProdutoDB, SaopauloDB
from schemas import (
    ProdutoCreate,
    ProdutoResponse,
    SaopauloCreate,
    SaopauloResponse,
)


Base.metadata.create_all(bind=engine)


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.get('/')
def home():
    return {'status': 'API Online - Todos os endpoints ativos'}
@app.get('/produtos', response_model=List[ProdutoResponse])
def listar_produtos(db: Session = Depends(get_db)):
    return db.query(ProdutoDB).order_by(ProdutoDB.id).all()


@app.get('/produtos/{produto_id}', response_model=ProdutoResponse)
def obter_produto(
    produto_id: Annotated[int, Path(title='O ID do produto', ge=1)],
    db: Session = Depends(get_db),
):
    produto = (
        db.query(ProdutoDB)
        .filter(ProdutoDB.id == produto_id)
        .first()
    )

    if produto is None:
        raise HTTPException(
            status_code=404,
            detail='Produto não encontrado',
        )

    return produto


@app.post('/produtos', response_model=ProdutoResponse, status_code=201)
def criar_produto(
    produto: ProdutoCreate,
    db: Session = Depends(get_db),
):
    novo_produto = ProdutoDB(**produto.model_dump())
    db.add(novo_produto)
    db.commit()
    db.refresh(novo_produto)
    return novo_produto


@app.put('/produtos/{produto_id}', response_model=ProdutoResponse)
def atualizar_produto(
    produto_id: Annotated[int, Path(ge=1)],
    dados: ProdutoCreate,
    db: Session = Depends(get_db),
):
    produto = (
        db.query(ProdutoDB)
        .filter(ProdutoDB.id == produto_id)
        .first()
    )

    if produto is None:
        raise HTTPException(
            status_code=404,
            detail='Produto não encontrado',
        )

    produto.nome = dados.nome
    produto.preco = dados.preco
    produto.quantidade = dados.quantidade

    db.commit()
    db.refresh(produto)
    return produto


@app.delete('/produtos/{produto_id}', status_code=204)
def remover_produto(
    produto_id: Annotated[int, Path(ge=1)],
    db: Session = Depends(get_db),
):
    produto = (
        db.query(ProdutoDB)
        .filter(ProdutoDB.id == produto_id)
        .first()
    )

    if produto is None:
        raise HTTPException(
            status_code=404,
            detail='Produto não encontrado',
        )

    db.delete(produto)
    db.commit()

    return None

@app.get('/saopaulo', response_model=List[SaopauloResponse])
def listar_saopaulo(db: Session = Depends(get_db)):
    return db.query(SaopauloDB).all()


@app.get('/saopaulo/{saopaulo_id}', response_model=SaopauloResponse)
def obter_saopaulo(
    saopaulo_id: Annotated[
        int,
        Path(title='O ID do registro', ge=1),
    ],
    db: Session = Depends(get_db),
):
    saopaulo = (
        db.query(SaopauloDB)
        .filter(SaopauloDB.id == saopaulo_id)
        .first()
    )

    if saopaulo is None:
        raise HTTPException(
            status_code=404,
            detail='São Paulo não encontrado',
        )

    return saopaulo


@app.post('/saopaulo', response_model=SaopauloResponse, status_code=201)
def criar_saopaulo(
    saopaulo: SaopauloCreate,
    db: Session = Depends(get_db),
):
    novo_saopaulo = SaopauloDB(**saopaulo.model_dump())
    db.add(novo_saopaulo)
    db.commit()
    db.refresh(novo_saopaulo)
    return novo_saopaulo


@app.put('/saopaulo/{saopaulo_id}', response_model=SaopauloResponse)
def atualizar_saopaulo(
    saopaulo_id: Annotated[int, Path(ge=1)],
    dados: SaopauloCreate,
    db: Session = Depends(get_db),
):
    saopaulo = (
        db.query(SaopauloDB)
        .filter(SaopauloDB.id == saopaulo_id)
        .first()
    )

    if saopaulo is None:
        raise HTTPException(
            status_code=404,
            detail='São Paulo não encontrado',
        )

    saopaulo.nome = dados.nome
    saopaulo.titulos = dados.titulos
    saopaulo.cores = dados.cores
    saopaulo.idade = dados.idade

    db.commit()
    db.refresh(saopaulo)
    return saopaulo


@app.delete('/saopaulo/{saopaulo_id}', status_code=204)
def remover_saopaulo(
    saopaulo_id: Annotated[int, Path(ge=1)],
    db: Session = Depends(get_db),
):
    saopaulo = (
        db.query(SaopauloDB)
        .filter(SaopauloDB.id == saopaulo_id)
        .first()
    )

    if saopaulo is None:
        raise HTTPException(
            status_code=404,
            detail='São Paulo não encontrado',
        )

    db.delete(saopaulo)
    db.commit()

    return None
