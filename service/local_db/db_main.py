#!/usr/bin/env python3
# encoding: utf-8
"""
Este módulo é parte integrante da aplicação Promais Service, desenvolvida por
Victor Domingos e distribuída sob os termos da licença Creative Commons
Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)
"""
import os

from sqlalchemy import create_engine, or_, and_
from sqlalchemy.orm import sessionmaker, load_only
from typing import Dict, Tuple, List, Union, Optional, Any

import db_local_models as db_models

from misc import calcular_dias_desde
from global_setup import LOCAL_DATABASE_PATH, ESTADOS, PRIORIDADES


def iniciar_sessao_db():
    engine = create_engine('sqlite+pysqlite:///' + os.path.expanduser(LOCAL_DATABASE_PATH))
    session = sessionmaker()
    session.configure(bind=engine)
    return session(), engine


# =============================== LOGIN ===============================
# TODO
def validate_login(username: str, password: str) -> Tuple[bool, str]:
    """ Check if username and password match the info in database. Token stuff
        is provided here only to ensure code compatibility for future web API
        access.
    """
    s, _ = iniciar_sessao_db()

    if username == "npk" and password == "...":  # change this
        loggedin = True
        token = "The amazing NPK Token"
    else:
        loggedin = False
        token = None

    return loggedin, token


def get_user_id(username: str) -> int:
    """ Return the user ID from database, queried with a string containing the
        username.
    """
    s, _ = iniciar_sessao_db()
    utilizador = s.query(db_models.User.id).filter(db_models.User.nome==username).one()
    return utilizador.id


def change_password(username: str, old_password: str, new_password1: str) -> bool:
    """ Change the password for the given user if the old password matches.
        Returns False if it fails for some reason.
    """
    print("DB: Changing password for the user {username}.")
    result = True  # TODO
    return result

# =============================== Produtos ===============================
def obter_artigo(part_number: str):
    return {'id': 1,
            'descr': "This is the description for this product",
            'part_number': "ZD123"}


# =============================== Reparações ===============================
def save_repair(repair) -> int:
    print("a guardar o processo de reparação", repair)
    s, _ = iniciar_sessao_db()
    new_repair = db_models.Repair(**repair)
    s.add(new_repair)
    s.commit()
    print(new_repair, type(new_repair), new_repair.id)
    return new_repair.id


def update_repair_status(rep_num: int, status: int):
    print(f"A atualizar o estado da reparação nº {rep_num}: {status} ({ESTADOS[status]})")
    reparacao = obter_reparacao(rep_num)

    s, _ = iniciar_sessao_db()

    pass  # TODO atualizar reparacao com novo estado.


def update_repair_priority(rep_num: int, priority: int):
    print(f"A atualizar a prioridade da reparação nº {rep_num}: {priority} ({PRIORIDADES[priority]})")
    reparacao = _obter_reparacao(rep_num)
    s, _ = iniciar_sessao_db()
    pass  # TODO atualizar reparacao com prioridade.

def contar_reparacoes() -> int:
    s, _ = iniciar_sessao_db()
    return s.query(db_models.Repair).count()

def contar_contactos() -> int:
    s, _ = iniciar_sessao_db()
    return s.query(db_models.Contact).count()

def contar_remessas() -> int:
    s, _ = iniciar_sessao_db()
    return 0 #TODO


def obter_todas_reparacoes() -> List[Dict[str, Union[int, str]]]:
    """ Obtém lista de dicionários contendo todas as reparações, para preencher
        a tabela principal (inclui apenas os campos necessários).
    """
    s, _ = iniciar_sessao_db()

    return [{'id': rep.id,
             'cliente_nome': rep.cliente.nome,
             'descr_artigo': rep.product.descr_product,
             'sn': rep.sn,
             'descr_servico': rep.descr_servico,
             'estado': rep.estado_reparacao,
             'dias': calcular_dias_desde(rep.created_on),
             'prioridade': rep.prioridade}
            for rep in s.query(db_models.Repair)]


def obter_reparacoes_por_estados(status_list: List[int]) -> List[Dict[str, Union[int, str]]]:
    """ Obtem lista de dicionários contendo todas as reparações que se
        encontram num dado estado, para preencher a tabela principal (inclui
        apenas os campos necessários).
    """
    s, _ = iniciar_sessao_db()

    if not status_list:
        return obter_todas_reparacoes()

    reparacoes = s.query(db_models.Repair) \
                         .filter(db_models.Repair.estado_reparacao.in_(status_list))

    return [{'id': rep.id,
            'cliente_nome': rep.cliente.nome,
            'descr_artigo': rep.product.descr_product,
            'sn': rep.sn,
            'descr_servico': rep.descr_servico,
            'estado': rep.estado_reparacao,
            'dias': calcular_dias_desde(rep.created_on),
            'prioridade': rep.prioridade}
           for rep in reparacoes]


def pesquisar_reparacoes(txt_pesquisa: str, estados: List[int]=None) -> List[Dict[str, Union[int, str]]]:
    """ Obtem lista de dicionários contendo todas as reparações que se
        correspondem ao termos de pesquisa indicado e que se encontram num
        dado estado, para preencher a tabela principal (inclui apenas os
        campos necessários). Para permitir um melhor desempenho, apenas é
        mostrada uma parte dos registos.
    """
    s, _ = iniciar_sessao_db()

    if estados is None:
        estados = []

    termo_pesquisa = txt_pesquisa

    for c in txt_pesquisa:
        if c in "1234567890.":
            numeric = True
        else:
            numeric = False
            break

    if not numeric:
        if '*' in txt_pesquisa or '_' in txt_pesquisa or '?' in txt_pesquisa:
            termo_pesquisa = txt_pesquisa.replace('_', '__').replace('*', '%').replace('?', '_')
        else:
            termo_pesquisa = f"%{txt_pesquisa}%"

    reps = s.query(db_models.Repair, db_models.Contact, db_models.Product) \
                .filter(and_(db_models.Repair.product_id == db_models.Product.id,
                             db_models.Repair.cliente_id == db_models.Contact.id)) \
                .filter(and_(db_models.Repair.estado_reparacao.in_(estados),
                             or_(
                                 db_models.Repair.id.like(termo_pesquisa),
                                 db_models.Contact.nome.ilike(termo_pesquisa),
                                 db_models.Contact.telefone.ilike(termo_pesquisa),
                                 db_models.Contact.telemovel.ilike(termo_pesquisa),
                                 db_models.Contact.email.ilike(termo_pesquisa),
                                 db_models.Product.descr_product.ilike(termo_pesquisa),
                                 db_models.Product.part_number.ilike(termo_pesquisa),
                                 db_models.Repair.descr_servico.ilike(termo_pesquisa),
                                 db_models.Repair.notas.ilike(termo_pesquisa),
                                 db_models.Repair.num_fatura.ilike(termo_pesquisa),
                                 db_models.Repair.sn.ilike(termo_pesquisa)
                        ))) \
                .order_by(db_models.Repair.created_on)[:3000]

    return [{'id': rep[0].id,
              'cliente_nome': rep[1].nome,
              'descr_artigo': rep[2].descr_product,
              'sn': rep[0].sn,
              'descr_servico': rep[0].descr_servico,
              'estado': rep[0].estado_reparacao,
              'dias': calcular_dias_desde(rep[0].created_on),
              'prioridade': rep[0].prioridade}
            for rep in reps]


def _obter_reparacao(num_rep: int):
    """ Returns a Repair object.
    """
    s, _ = iniciar_sessao_db()
    return s.query(db_models.Repair).get(num_rep)


def obter_reparacao(num_rep: int) -> Dict[str, Union[int, str]]:
    """ Obtém um dicionário contendo a informação referente a uma reparação
        (inclui os campos necessários para preencher a janela de detalhes
        de reparação).
    """
    rep = _obter_reparacao(num_rep)

    #TODO: distinguir e adaptar para rep. cliente/stock
    return {'id': rep.id,
            'cliente_id': rep.cliente.id,
            'cliente_nome': rep.cliente.nome,
            'cliente_telefone': rep.cliente.telefone,
            'cliente_email': rep.cliente.email,
            'product_id': rep.product.id,
            'product_descr': rep.product.descr_product,
            'product_part_number': rep.product.part_number,
            'sn': rep.sn,
            'fornecedor_id': rep.fornecedor_id,
            'estado_artigo': rep.estado_artigo,
            'obs_estado': rep.obs_estado,
            'is_garantia': rep.is_garantia,
            'data_compra': rep.data_compra,
            'num_fatura': rep.num_fatura,
            'loja_compra': rep.loja_compra,
            'descr_servico': rep.descr_servico,
            'avaria_reprod_loja': rep.avaria_reprod_loja,
            'requer_copia_seg': rep.requer_copia_seg,
            'is_find_my_ativo': rep.is_find_my_ativo,
            'senha': rep.senha,
            'acessorios_entregues': rep.acessorios_entregues,
            'notas': rep.notas,
            'local_reparacao_id': rep.local_reparacao_id,
            'estado_reparacao': rep.estado_reparacao,
            'fatura_fornecedor': rep.fatura_fornecedor,
            'nar_autorizacao_rep': rep.nar_autorizacao_rep,
            'data_fatura_fornecedor': rep.data_fatura_fornecedor,
            'num_guia_rececao': rep.num_guia_rececao,
            'data_guia_rececao': rep.data_guia_rececao,
            'cod_resultado_reparacao': rep.cod_resultado_reparacao,
            'descr_detalhe_reparacao': rep.descr_detalhe_reparacao,
            'novo_sn_artigo': rep.novo_sn_artigo,
            'notas_entrega': rep.notas_entrega,
            'utilizador_entrega_id': rep.utilizador_entrega_id,
            'data_entrega': rep.data_entrega,
            'num_quebra_stock': rep.num_quebra_stock,
            'is_rep_stock': rep.is_stock,
            'is_rep_cliente': not rep.is_stock,
            'modo_entrega': rep.modo_entrega,
            'cliente_pagou_portes': rep.cliente_pagou_portes,
            'reincidencia_processo_id': rep.reincidencia_processo_id,
            'morada_entrega': rep.morada_entrega,
            'prioridade': rep.prioridade,
            'criado_por_utilizador_id': rep.criado_por_utilizador_id,
            'ult_atualizacao_por_utilizador_id': rep.ult_atualizacao_por_utilizador_id,

            'created_on': rep.created_on,
            'updated_on': rep.updated_on,

            'fornecedor': rep.fornecedor,
            'local_reparacao': rep.local_reparacao.nome,
            'utilizador_entrega': rep.utilizador_entrega,
            'criado_por_utilizador': rep.criado_por_utilizador,
            'atualizado_por_utilizador': rep.atualizado_por_utilizador
            }

def obter_num_serie(num_rep: int) -> str:
    rep = _obter_reparacao(num_rep)
    return rep.sn


# =============================== Mensagens/Eventos ===============================

def obter_mensagens(user_id: int) -> List[Dict[str, Union[int, str]]]:
    """ Obtém lista de dicionários contendo todas as mensagens visíveis, para
        o utilizador atual, para apresentar na janela principal (inclui apenas
        os campos necessários).
    """

    s, _ = iniciar_sessao_db()
    utilizador = s.query(db_models.User).get(user_id)

    msgs = s.query(db_models.UtilizadorNotificadoPorEvento_link) \
                        .filter_by(is_visible=1, user=utilizador)

    return [{'evento_id': msg.evento_id,
             'repair_id': msg.event.repair.id,
             'remetente_nome': msg.event.criado_por_utilizador.nome,
             'data': msg.event.created_on,
             'texto': msg.event.descricao,
             'estado_msg': msg.is_open}
            for msg in msgs]


def obter_evento(event_id: int) -> Dict[str, Union[int, str]]:
    """ Obtém um dicionário contendo a informação referente a uma mensagem ou
        evento (inclui os campos necessários para preencher a janela de detalhes
        de mensagem/evento).
    """
    s, _ = iniciar_sessao_db()
    evento = s.query(db_models.Event).get(event_id)

    return {'repair_id': evento.repair.id,
            'cliente_nome': evento.repair.cliente.nome,
            'remetente_nome': evento.criado_por_utilizador.nome,
            'artigo': evento.repair.product.descr_product,
            'data': evento.created_on,
            'texto': evento.descricao,
            'estado_atual': evento.repair.estado_reparacao,
            'resultado': evento.repair.cod_resultado_reparacao}


# =============================== Contactos ===============================
def save_contact(contacto) -> int:
    print("a guardar o contacto", contacto)
    db_last_contact_number = 999
    return db_last_contact_number


def pesquisar_contactos(txt_pesquisa: str="", tipo: str ="Clientes"):
    s, _ = iniciar_sessao_db()

    termo_pesquisa = txt_pesquisa

    numeric = False
    for c in txt_pesquisa:
        if c in "1234567890.":
            numeric = True
        else:
            numeric = False
            break

    if not numeric:
        if '*' in txt_pesquisa or '_' in txt_pesquisa or '?' in txt_pesquisa:
            termo_pesquisa = txt_pesquisa.replace('_', '__').replace('*', '%').replace('?', '_')
        else:
            termo_pesquisa = f"%{txt_pesquisa}%"

    #TODO: restringir a pesquisa aos registos que tenham o estado selecionado

    if tipo == "Clientes":
        contactos = s.query(db_models.Contact).filter(
        and_(db_models.Contact.is_cliente.is_(True),
            or_(
                db_models.Contact.id.like(termo_pesquisa),
                db_models.Contact.nome.ilike(termo_pesquisa),
                db_models.Contact.telefone.ilike(termo_pesquisa),
                db_models.Contact.telemovel.ilike(termo_pesquisa),
                db_models.Contact.email.ilike(termo_pesquisa),
        )))
    else:
        contactos = s.query(db_models.Contact).filter(
        and_(db_models.Contact.is_fornecedor.is_(True),
            or_(
                db_models.Contact.id.like(termo_pesquisa),
                db_models.Contact.nome.ilike(termo_pesquisa),
                db_models.Contact.telefone.ilike(termo_pesquisa),
                db_models.Contact.telemovel.ilike(termo_pesquisa),
                db_models.Contact.email.ilike(termo_pesquisa),
        )))

    return [{'id': contact.id,
             'nome': contact.nome,
             'telefone': contact.telefone,
             'email': contact.email}
            for contact in contactos]


def obter_clientes() -> List[Dict[str, Union[int, str]]]:
    s, _ = iniciar_sessao_db()
    contactos = s.query(db_models.Contact).filter_by(is_cliente=True)
    return [{'id': contact.id,
             'nome': contact.nome,
             'telefone': contact.telefone,
             'email': contact.email}
            for contact in contactos]


def obter_fornecedores() -> List[Dict[str, Union[int, str]]]:
    s, _ = iniciar_sessao_db()
    contactos = s.query(db_models.Contact).filter_by(is_fornecedor=True) \
                        .options(load_only("id", "nome", "telefone", "email"))
    return [{'id': contact.id,
             'nome': contact.nome,
             'telefone': contact.telefone,
             'email': contact.email}
            for contact in contactos]


def obter_lista_fornecedores() -> List[Dict[str, Union[int, str]]]:
    """ Obter lista simplificada de fornecedores e/ou centros técnicos.
    """
    s, _ = iniciar_sessao_db()
    contactos = s.query(db_models.Contact).filter_by(is_fornecedor=True)\
                        .options(load_only("id", "nome"))

    return [{'id': contact.id,
             'nome': contact.nome}
            for contact in contactos]


def obter_contacto(num_contacto: int) -> Dict[str, Union[int, str]]:
    s, _ = iniciar_sessao_db()
    contacto = s.query(db_models.Contact).get(num_contacto)

    return {
        'id': contacto.id,
        'nome': contacto.nome,
        'empresa': contacto.empresa,
        'telefone': contacto.telefone,
        'telemovel': contacto.telemovel,
        'telefone_empresa': contacto.telefone_empresa,
        'email': contacto.email,
        'morada': contacto.morada,
        'cod_postal': contacto.cod_postal,
        'localidade': contacto.localidade,
        'pais': contacto.pais,
        'nif': contacto.nif,
        'notas': contacto.notas,
        'is_cliente': contacto.is_cliente,
        'is_fornecedor': contacto.is_fornecedor,
        'criado_por_utilizador_id': contacto.criado_por_utilizador_id,
        'ult_atualizacao_por_utilizador_id': contacto.ult_atualizacao_por_utilizador_id,
        'created_on': contacto.created_on.isoformat(sep=' ', timespec='minutes'),
        'updated_on': contacto.updated_on.isoformat(sep=' ', timespec='minutes'),
        'criado_por_utilizador_nome': contacto.criado_por_utilizador.nome,
        'atualizado_por_utilizador_nome': contacto.atualizado_por_utilizador.nome}


def obter_info_contacto(num_contacto: int, tipo:str) -> Optional[Dict[str, Union[str, Any]]]:
    """ Obter informação resumida de um contacto, para utilização no
        formulário de nova reparação. Caso não exista na base de dados um
        contacto que corresponda aos dados introduzidos (cliente ou fornecedor
        com o número indicado), a função devolve None.
    """
    s, _ = iniciar_sessao_db()

    contacto = s.query(db_models.Contact).get(num_contacto)

    if not contacto:
        return None

    if tipo == "Fornecedor":
        if not contacto.is_fornecedor:
            return None
    elif tipo == "Cliente":
        if not contacto.is_cliente:
            return None
    else:
        return None

    if contacto.telefone:
        telefone = contacto.telefone
    elif contacto.telemovel:
        telefone = contacto.telemovel
    elif contacto.telefone_empresa:
        telefone = contacto.telefone_empresa + " (Empresa)"
    else:
        telefone = "N/D"
    return {
        'id': contacto.id,
        'nome': contacto.nome,
        'telefone': telefone,
        'email': contacto.email
        }


# =============================== Remessas ===============================
def save_remessa(remessa: int) -> int:
    print("a guardar a remessa", remessa)
    db_last_remessa_number = 1984
    return db_last_remessa_number


def obter_lista_processos_por_receber():
    print("A obter lista atualizada de processos de reparação que falta receber dos fornecedores e/ou centros técnicos.")
    # TODO:
    lista = ["12234 - iPhone 7 128GB Space grey - José manuel da Silva Castro",
             "85738 - MacBook Pro 15\" Retina - Manuel José de Castro Silva",
             "32738 - iPod shuffle 2GB - Laranjas e Limões, Lda.",
             "25720 - Beats X - NPK - Network Project for Knowledge",
             "85738 - MacBook Pro 15\" Retina - Manuel José de Castro Silva",
             "32738 - iPod shuffle 2GB - Laranjas e Limões, Lda."]

    return lista


def obter_lista_processos_por_enviar():
    print("A obter lista atualizada de processos de reparação que falta receber dos fornecedores e/ou centros técnicos.")
    # TODO:
    lista = ["12234 - iPhone 7 128GB Space grey - José manuel da Silva Castro",
             "85738 - MacBook Pro 15\" Retina - Manuel José de Castro Silva",
             "32738 - iPod shuffle 2GB - Laranjas e Limões, Lda.",
             "25720 - Beats X - NPK - Network Project for Knowledge",
             "85738 - MacBook Pro 15\" Retina - Manuel José de Castro Silva",
             "32738 - iPod shuffle 2GB - Laranjas e Limões, Lda."]

    return lista


# =============================== Empréstimos ===============================

def obter_lista_artigos_emprest() -> Dict[str, Tuple[str, str]]:
    """
    Devolve um dicionário em que as chaves correspondem ao ID de artigo, sendo
    o artigo definido através de uma tupla que contém a descrição e o número de
    série.
    """
    print("A obter lista atualizada de artigos de empréstimo. ")
    # TODO:
    artigos = {"12234": ("iPhone 7 128GB Space grey", ""),
               "85738": ("MacBook Pro 15\" Retina", ""),
               "32738": ("iPod shuffle 2GB", ""),
               "25720": ("Beats X", "XWD45123456PTXCH"),
               "85737": ("MacBook Pro 15\" Retina", ""),
               "32736": ("iPod shuffle 2GB", ""),
               "25725": ("Beats X - NPK - Network Project for Knowledge", ""),
               "85734": ("MacBook Pro 15\" Retina", ""),
               "32733": ("iPod shuffle 2GB", ""),
               "25722": ("Beats X - NPK - Network Project for Knowledge", ""),
               "85731": ("MacBook Pro 15\" Retina", "XWD45123456PTXCH"),
               "32730": ("iPod shuffle 2GB", "WXBG23123GB654P"),
               "25729": ("Beats X - NPK - Network Project for Knowledge", "")
               }
    return artigos


# =============================== Orçamentos ===============================


# =============================== Comunicação ===============================

