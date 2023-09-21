import sys
from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect, request
import requests

from schemas import *
from flask_cors import CORS
import sqlite3

info = Info(title="API de operção de vendas e estoque", version="1.0.0")
app = OpenAPI(__name__, info=info)
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024

CORS(app)

# definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
produto_tag = Tag(name="Produto", description="Visualização de produtos")
vendas_tag = Tag(name="Vendas", description="Adição, cancelamento e visualizacão de vendas")


@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')


@app.get('/produtos', tags=[produto_tag],
         responses={"200": ListagemProdutosSchema, "500": ErrorSchema})
def get_produtos():
    """Busca todos os Produto cadastrados

    Retorna lista de produtos em estoque.
    """
    try:
        db = sqlite3.connect('db.db')
        cursor = db.cursor()
        itens =  cursor.execute( '''
        select 
            i.codItem, i.ean, i.descricao,
            i.uniVenda, i.qtdEmbComp,
            i.vl1, i.vl2, i.codFab,
            f.nome as fabricante,
            i.qtdEstoque, i.controlado
        from item i
        join fabricante f
            on i.codfab = f.codfab
        where i.qtdEstoque > 0
        ''')
        data = [
            {
                'codItem':item[0]
                ,'ean':item[1]
                ,'descricao':item[2]
                ,'uniVenda':item[3]
                ,'qtdEmbComp':item[4]
                ,'vl1':item[5]
                ,'vl2':item[6]
                ,'codFab':item[7]
                ,'fabricante':item[8]
                ,'qtdEstoque':item[9]
                ,'controlado':item[10]
            } for item in itens
        ]
        return {'message':f'{data} itens encontrados', 
                'data':data}, 200
    except:
        return {'message':'Erro de processamento'}, 500


@app.get('/vendas', tags=[vendas_tag],
         responses={"200": VendasListView, "404": ErrorSchema})
def get_vendas():
    """Faz a busca por todas as Vendas registradas

    Retorna as vendas registradas com informações gerais.
    """
    # cria a engine de conexão com o banco
    try:
        db = sqlite3.connect('db.db')
        cursor = db.cursor()
        venda =  cursor.execute( '''
            select 
                v.id as numPedido,
                v.cliente_cpf,
                v.data_vend as dtEmissao,
                coalesce(c.nome, 'Cliente não cadastrado') as cliente,
                v.medico_crm,
                v.medico_nome,
                (select sum(iv.qtd*vlUnit) from iten_venda iv where iv.id_venda = v.id) as vlTotal,
                s.descricao as status
            from venda v
            join status_venda s
                on v.status = s.id
            left join cliente c
                on v.cliente_cpf = c.cpf
            ''').fetchall()
        
        data = [
            {
                'numPedido':v[0]
                ,'cliente_cpf':v[1]
                ,'dtEmissao':v[2]
                ,'cliente':v[3]
                ,'medico_crm':v[4]
                ,'medico_nome':v[5]
                ,'vlTotal':v[6]
                ,'status':v[7]
            } for v in venda
        ]
    
        return {'message':f'{data} itens encontrados', 
                'data':data}, 200
    except:
        return {'message':'Erro de processamento'}, 500


@app.get('/venda', tags=[vendas_tag],
            responses={"200": VendaBuscaPorIDSchema, "404": ErrorSchema})
def get_venda(query: VendaBuscaPorIDSchema):
    """Busca por uma venda a partir de um ID(Número do pedido)

    Retorna a venda selecionada, assim como os itens relacionados.
    """
    db = sqlite3.connect('db.db')
    cursor = db.cursor()
    venda =  cursor.execute(f"""
        select 
            v.cliente_cpf,
            v.id_forma_pagamento,
            v.prazo_entrega,
            v.data_vend as dtEmissao,
            v.obs,
            v.medico_crm,
            v.medico_nome,
            v.cidade,
            v.estado,
            s.descricao as status
            from venda v
            join status_venda s 
            on v.status = s.id
        where v.id = {query.numPedido}
        """).fetchone()

    itens = cursor.execute(f"""
        select 
            i.codItem as codItem,
            v.qtd as quant,
            v.vlUnit as vr_unitario,
            v.unidade,
            i.descricao as produto
            from iten_venda v
        join item i
        on i.codItem = v.codItem        
        where v.cancel = 0
        and v.id_venda = {query.numPedido}
        """).fetchall()    
    
    result = {
            'cliente_cpf':venda[0],
            'id_forma_pagamento':venda[1],
            'prazo_entrega':venda[2],
            'dtEmissao':str(venda[3]),
            'obs':venda[4],
            'medico_crm':venda[5],
            'medico_nome':venda[6],
            'cidade':venda[7],
            'estado':venda[8],
            'status':venda[9],
            'itens': [
                        {
                            'codItem':item[0]
                            ,'quant':item[1]
                            ,'vr_unitario':item[2]
                            ,'unidade':item[3]
                            ,'produto':item[4]
                        }
                        for item in itens
                    ]
            }
        
    return {"data":result, "message":"Venda encontrada"}


@app.post('/venda', tags=[vendas_tag],
         responses={"200": VendaMensagemRetorno, "400": ErrorSchema, "500": ErrorSchema, "403": ErrorSchema})
def post_venda(body:VendaPostSchema):
    """Registra uma nova venda no banco de dados

    Retorna uma confirmação sobre a tentativa de registro.
    """
    data = body.dict()
    headers = {"Content-Type": "application/json"}

    user = requests.request("GET",f"http://localhost:5000/permission?token={request.headers.get('X-Custom-Token')}", headers=headers)

    if user.status_code == 200:
        if user.json().get('vendedor')==1:
            try:
                db = sqlite3.connect('db.db')
                cursor = db.cursor()
                nova_venda = int(cursor.execute('select max(id)+1 from venda').fetchone()[0])
                
                cursor.execute(f'''
                    insert into venda(
                        id, data_vend, id_forma_pagamento, cod_formPg, 
                        prazo_entrega, cliente_cpf, medico_crm, 
                        medico_nome, estado, cidade, status, vendedor)
                    values({nova_venda}, DATE(), {data.get("id_forma_pagamento")},{data.get("cod_formPg")},
                            {data.get("prazo_entrega")}, '{data.get("cpf_cliente")}',  '{data.get("medico_crm")}', 
                            '{data.get("medico_nome")}','{data.get("estado")}','{data.get("cidade")}', 1, '{data.get("vendedor")}');
                    ''')
                
                for item in data.get("itens"):
                    cursor.execute(f'''
                    insert into iten_venda(
                        id_venda, codItem, qtd, vlUnit, 
                        unidade, cancel)
                    values({nova_venda}, '{item.get('codItem')}', {item.get('quant')}, 
                        {item.get('vr_unitario')}, '{item.get('unidade')}', 0);
                    ''')
                    cursor.execute(f'''
                    update item
                        set qtdEstoque = qtdEstoque - {item.get('quant')}
                        where codItem = {item.get('codItem')};
                    ''')
                
                cursor.execute(f'''
                    insert into receita
                    values({nova_venda}, '{data.get("receita").get('nome')}', '{data.get("receita").get('extensao')}', 
                            '{data.get("receita").get('arquivo')}', {data.get("receita").get('tamanho')});
                    ''')
                
                db.commit()
                
                return {'message':'Venda registrada com sucesso.'}, 200        
            except:
                print(sys.exc_info())
                return {'message':'Erro de processamento'}, 500
        else: return {'message':'Usuário não tem permissão para essa operação.'},403
    else:
        return {"message":"Erro na validação do usuário"}, 400


@app.post('/venda/cancel', tags=[vendas_tag],
         responses={"200": VendaMensagemRetorno, "400": ErrorSchema, "500": ErrorSchema, "403": ErrorSchema})
def put_cancel_venda(body:VendaPutStatus):
    """Cancela uma venda a partir do ID
    
    Retorna uma confirmação sobre a tentativa de registro.
    """
    headers = {"Content-Type": "application/json"}

    user = requests.request("POST",f"http://localhost:5000/permission?token={request.headers.get('X-Custom-Token')}", headers=headers)

    if user.status_code == 200:
        if user.content.get('vendedor')==1:
            try:
                db = sqlite3.connect('db.db')
                cursor = db.cursor()
                cursor.execute(f'''
                    update venda 
                        set status = 4
                    where id = {body.numPedido}
                    ''')
                db.commit()
                return {'message':'Cancelamento confirmado com suceso'}, 200   
            except:
                return {'message':'Erro de processamento'}, 500
        else: return {'message':'Usuário não tem permissão para essa operação.'},403
    else:
        return {"message":"Erro na validação do usuário"}, 400


@app.put('/recebimento', tags=[vendas_tag],
         responses={"200": VendaMensagemRetorno, "400": ErrorSchema, "500": ErrorSchema, "403": ErrorSchema})
def put_recebimento(body: VendaPutStatus):
    """Altera o status de uma venda para "Recebido pelo cliente".

    Retorna uma confirmação sobre a tentativa de registro.
    """
    headers = {"Content-Type": "application/json"}

    user = requests.request("POST",f"http://localhost:5000/permission?token={request.headers.get('X-Custom-Token')}", headers=headers)

    if user.status_code == 200:
        if user.content.get('vendedor')==1:
            try:
                db = sqlite3.connect('db.db')
                cursor = db.cursor()
                cursor.execute(f'''
                    update venda 
                        set status = 3
                    where id = {body.numPedido}
                    ''')
                db.commit()
                return {'message':'Recebimento confirmado com suceso'}, 200   
            except:
                return {'message':'Erro de processamento'}, 500
        else: return {'message':'Usuário não tem permissão para essa operação.'},403
    else:
        return {"message":"Erro na validação do usuário"}, 400


@app.delete('/venda/produto', tags=[vendas_tag],
         responses={"200": VendaMensagemRetorno, "400": ErrorSchema, "500": ErrorSchema, "403": ErrorSchema})
def delete_venda_item(query: VendaDeleteVendaItem):
    """Cancela um produto a partir do código do item e do ID da venda
    
    Retorna uma confirmação sobre a tentativa de registro.
    """
    headers = {"Content-Type": "application/json"}

    user = requests.request("POST",f"http://localhost:5000/permission?token={request.headers.get('X-Custom-Token')}", headers=headers)

    if user.status_code == 200:
        if user.content.get('vendedor')==1:
            try:
                db = sqlite3.connect('db.db')
                cursor = db.cursor()
                cursor.execute(f'''
                    update iten_venda 
                        set cancel = 1
                    where id_venda = {query.numPedido}
                    and codItem = {query.codItem}
                    ''')
                db.commit()
                return {'message':'Item removido com suceso'}, 200
            except:
                return {'message':'Erro de processamento'}, 500
        else: return {'message':'Usuário não tem permissão para essa operação.'},403
    else:
        return {"message":"Erro na validação do usuário"}, 400
