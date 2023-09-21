create table fabricante(
	codFab integer PRIMARY KEY,
	nome varchar(255)
)

create table item(
	codItem integer PRIMARY KEY,
	ean varchar(14),
	descricao varchar(255),
	uniVenda varchar(5),
	uniCompra varchar(5),
	qtdEmbComp integer,
	vl1 decimal(10,2),
	vl2 decimal(10,2),
	codFab integer,
	qtdEstoque integer,
	controlado boolean,
	FOREIGN KEY (codFab) references FABRICANTE(codFab)
)

create table cliente(
cpf varchar(11) primary key,
nome varchar(255),
uf varchar(2),
cidade varchar(255)
)

create table venda(
	id integer PRIMARY KEY,
	data timestamp not null,
	id_forma_pagamento integer not null,
	cod_formPg integer not null,
	prazo_entrega integer not null,
	obs varchar(255),
	cliente_cpf varchar(11),
	medico_crm varchar(12),
	medico_nome varchar(255),
	cancel BOOLEAN default 0
)

create table iten_venda(
	id_venda integer,
	codItem integer,
	qtd integer,
	vlUnit decimal(10,2),
	unidade varchar(5),
	FOREIGN KEY (id_venda) references venda(id),
	FOREIGN KEY (codItem) references item(codItem)
)

create table receita(
	id_venda integer PRIMARY KEY,
	nome varchar(255),
	extensao varchar(10),
	arquivo text,
	tamanho integer
)

create table status_venda(
    id integer primary key,
    descricao varchar(20)
)

INSERT INTO fabricante (codFab, nome)
VALUES
    (1, 'Fabricante A'),
    (2, 'Fabricante B'),
    (3, 'Fabricante C'),
    (4, 'Fabricante D'),
    (5, 'Fabricante E'),
    (6, 'Fabricante F'),
    (7, 'Fabricante G'),
    (8, 'Fabricante H'),
    (9, 'Fabricante I'),
    (10, 'Fabricante J');


INSERT INTO item (codItem, ean, descricao, uniVenda, uniCompra, qtdEmbComp, vl2, vl1, codFab, qtdEstoque, controlado)
VALUES
    (1, '12345678901234', 'Produto 1', 'UN', 'UN', 10, 10.50, 15.00, 1, 100, true),
    (2, '23456789012345', 'Produto 2', 'CX', 'CX', 20, 25.00, 30.00, 2, 200, false),
    (3, '34567890123456', 'Produto 3', 'KG', 'KG', 5, 5.00, 7.00, 1, 50, false),
    (4, '45678901234567', 'Produto 4', 'UN', 'UN', 15, 12.00, 18.00, 3, 75, true),
    (5, '56789012345678', 'Produto 5', 'CX', 'CX', 25, 30.00, 35.00, 2, 250, false),
    (6, '67890123456789', 'Produto 6', 'KG', 'KG', 10, 8.00, 12.00, 4, 100, true),
    (7, '78901234567890', 'Produto 7', 'UN', 'UN', 8, 18.00, 22.00, 3, 80, false),
    (8, '89012345678901', 'Produto 8', 'CX', 'CX', 30, 35.00, 40.00, 5, 300, true),
    (9, '90123456789012', 'Produto 9', 'KG', 'KG', 12, 10.00, 14.00, 1, 120, false),
    (10, '01234567890123', 'Produto 10', 'UN', 'UN', 7, 20.00, 25.00, 4, 70, true);

INSERT INTO cliente (cpf, nome, uf, cidade)
VALUES
    ('00000000000', 'Cliente A', 'SP', 'São Paulo'),
    ('11111111111', 'Cliente B', 'RJ', 'Rio de Janeiro'),
    ('22222222222', 'Cliente C', 'MG', 'Belo Horizonte'),
    ('33333333333', 'Cliente D', 'RS', 'Porto Alegre'),
    ('44444444444', 'Cliente E', 'BA', 'Salvador'),
    ('55555555555', 'Cliente F', 'PE', 'Recife'),
    ('66666666666', 'Cliente G', 'PR', 'Curitiba'),
    ('77777777777', 'Cliente H', 'SC', 'Florianópolis'),
    ('88888888888', 'Cliente I', 'GO', 'Goiânia'),
    ('99999999999', 'Cliente J', 'DF', 'Brasília');

INSERT INTO venda (id, data_vend, id_forma_pagamento, cod_formPg, prazo_entrega, obs, cliente_cpf, medico_crm, medico_nome, status)
VALUES
    (1, '2023-09-09 10:00:00', 1, 4, 7, 'Venda 1', '00000000000', 'CRM123456', 'Médico 1', 2),
    (2, '2023-09-08 15:30:00', 2, 8, 5, 'Venda 2', '11111111111', 'CRM234567', 'Médico 2', 3),
    (3, '2023-09-07 14:20:00', 1, 4, 3, 'Venda 3', '22222222222', 'CRM345678', 'Médico 3', 4),
    (4, '2023-09-06 11:45:00', 2, 8, 2, 'Venda 4', '33333333333', 'CRM456789', 'Médico 4', 2),
    (5, '2023-09-05 09:10:00', 1, 4, 4, 'Venda 5', '44444444444', 'CRM567890', 'Médico 5', 1),
    (6, '2023-09-04 12:55:00', 2, 8, 6, 'Venda 6', '55555555555', 'CRM678901', 'Médico 6', 2),
    (7, '2023-09-03 17:45:00', 1, 4, 1, 'Venda 7', '66666666666', 'CRM789012', 'Médico 7', 4),
    (8, '2023-09-02 13:20:00', 2, 8, 7, 'Venda 8', '44444444444', 'CRM890123', 'Médico 8', 3),
    (9, '2023-09-01 16:30:00', 1, 4, 2, 'Venda 9', '22222222222', 'CRM901234', 'Médico 9', 3),
    (10, '2023-08-31 18:00:00', 2, 8, 5, 'Venda 10', '22222222222', 'CRM012345', 'Médico 10', 3);

INSERT INTO iten_venda (id_venda, codItem, qtd, vlUnit, unidade)
VALUES
    (1, 1, 5, 10.50, 'FR'),
    (1, 2, 3, 25.00, 'FA'),
    (2, 3, 2, 5.00, 'CP'),
    (2, 4, 7, 12.00, 'FR'),
    (3, 5, 4, 30.00, 'FA'),
    (3, 6, 8, 8.00, 'CP'),
    (4, 7, 10, 18.00, 'FR'),
    (4, 8, 6, 35.00, 'FA'),
    (5, 9, 3, 10.00, 'CP'),
    (5, 10, 5, 20.00, 'FR');

INSERT INTO status_venda (id, descricao)
VALUES
    (1,'ENVIADO'),
    (2,'CONFIRMADO'),
    (3,'ENTREGUE'),
    (4,'CANCELADO')