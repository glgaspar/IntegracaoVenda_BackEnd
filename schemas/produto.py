from pydantic import BaseModel
from typing import Optional, List


class ProdutoViewSchema(BaseModel):
    """ Define como um produto será retornado: produto.
    """
    codItem: int = 1
    ean: str = '00000000000000'
    descricao: str = "Produto 1"
    uniVenda: str = "FR"
    qtdEmbComp: int = 1
    vl1: float = 29.99
    vl2: float = 29.99
    codFab: int = 1
    fabricante: str = "XXX"
    qtdEstoque: int = 1
    controlado: bool = True


class ListagemProdutosSchema(BaseModel):
    """ Define como uma listagem de produtos será retornada.
    """
    data:List[ProdutoViewSchema]


class ProdutoMensagemRetorno(BaseModel):
    message: str
