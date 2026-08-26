from pydantic import BaseModel, ConfigDict, Field

class ProdutoBase(BaseModel):
    nome: str = Field(min_length=1, max_length=100)
    preco: float 
    quantidade: int 

class ProdutoCreate(ProdutoBase):
    pass

class ProdutoUpdate(ProdutoBase):
    pass

class ProdutoResponse(ProdutoBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
    
class SaopauloBase(BaseModel):
    nome: str = Field(min_length=1, max_length=100)
    titulos: int
    cores: str
    idade: int


class SaopauloCreate(SaopauloBase):
    pass


class SaopauloResponse(SaopauloBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
