from typing import Annotated, List

from fastapi import Depends, FastAPI, HTTPException, Path
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from database import Base, engine, get_db
from models import LivroDB, ProdutoDB
from schemas import (
    ProdutoCreate,
    ProdutoResponse,
    LivroCreate,
    LivroResponse,
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

@app.get('/livros', response_model=List[LivroResponse])
def listar_livros(db: Session = Depends(get_db)):
    return db.query(LivroDB).order_by(LivroDB.id).all()


@app.get('/livros/{livro_id}', response_model=LivroResponse)
def obter_livro(
    livro_id: Annotated[
        int,
        Path(title='O ID do livro', ge=1),
    ],
    db: Session = Depends(get_db),
):
    livro = (
        db.query(LivroDB)
        .filter(LivroDB.id == livro_id)
        .first()
    )

    if livro is None:
        raise HTTPException(
            status_code=404,
            detail='Livro não encontrado',
        )

    return livro


@app.post('/livros', response_model=LivroResponse, status_code=201)
def criar_livro(
    livro: LivroCreate,
    db: Session = Depends(get_db),
):
    novo_livro = LivroDB(**livro.model_dump())
    db.add(novo_livro)
    db.commit()
    db.refresh(novo_livro)
    return novo_livro


@app.put('/livros/{livro_id}', response_model=LivroResponse)
def atualizar_livro(
    livro_id: Annotated[int, Path(ge=1)],
    dados: LivroCreate,
    db: Session = Depends(get_db),
):
    livro = (
        db.query(LivroDB)
        .filter(LivroDB.id == livro_id)
        .first()
    )

    if livro is None:
        raise HTTPException(
            status_code=404,
            detail='Livro não encontrado',
        )

    livro.titulo = dados.titulo
    livro.autor = dados.autor
    livro.genero = dados.genero
    livro.ano_publicacao = dados.ano_publicacao

    db.commit()
    db.refresh(livro)
    return livro


@app.delete('/livros/{livro_id}', status_code=204)
def remover_livro(
    livro_id: Annotated[int, Path(ge=1)],
    db: Session = Depends(get_db),
):
    livro = (
        db.query(LivroDB)
        .filter(LivroDB.id == livro_id)
        .first()
    )

    if livro is None:
        raise HTTPException(
            status_code=404,
            detail='Livro não encontrado',
        )

    db.delete(livro)
    db.commit()

    return None
