from pydantic import BaseModel
from typing import List

class VendasView(BaseModel):
    """Define como é o retorno de uma venda resumida.
    """
    numPedido: int = 1
    cliente_cpf: str
    dtEmissao: str
    cliente: str
    medico_crm: str
    medico_nome: str
    vlTotal: float
    status: str


class VendasListView(BaseModel):
    """Define como é a lista de vendas retornada.
    """
    data: List[VendasView]


class VendaBuscaPorIDSchema(BaseModel):
    """ Define como deve ser feita a busca de detalhes de uma venda.
    """
    numPedido: str


class VendaItemBuscaPorIDSchema(BaseModel):
    """ Define como é o retorno dos itens nos detalhes de uma venda.
    """
    codItem: str = '00000000000000'
    quant: int = 1
    vr_unitario: float = 0
    unidade: str = 'FA'
    produto: str = "Produto 1"


class VendaBuscaPorIDView(BaseModel):
    """ Define como é o retorno de uma busca de detalhes de uma venda.
    """
    cliente_cpf: str = '00000000000'
    id_forma_pagamento: int = 1
    prazo_entrega: int = 1
    dtEmissao: str
    obs: str 
    medico_crm: str 
    medico_nome: str
    cidade: str
    estado: str
    status: str 
    itens: List[VendaItemBuscaPorIDSchema]


class VendaReceitaPostSchema(BaseModel):
    """Define com enviar um arquivo de receita para anexar a uma venda.
    """
    nome: str
    extensao: str
    arquivo: List[int]
    tamanho: int


class VendaItensPostSchema(BaseModel):
    """Define como enviar um item para registrar em venda.
    """
    codItem: str
    produto: str
    quant: int
    vr_unitario: float
    unidade: str

class VendaPostSchema(BaseModel):
    """Define como deve ser enviada uma venda a ser registrada.
    """
    cpf_cliente: str
    id_forma_pagamento: int
    cod_formPg: int
    prazo_entrega: int
    ordem_de_compra: str
    medico_nome: str
    medico_crm: str
    cidade: str
    estado: str
    vendedor: str
    itens: List[VendaItensPostSchema]
    receita: VendaReceitaPostSchema

class VendaPutStatus(BaseModel):
    """Define com deve ser enviado um pedido para alteração de status.
    """
    numPedido: int


class VendaDeleteVendaItem(BaseModel):
    """Define como deve ser enviado o cancelamento de um item de uma venda.
    """
    numPedido: int
    codItem: int


class VendaMensagemRetorno(BaseModel):
    message: str