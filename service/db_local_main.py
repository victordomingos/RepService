#!/usr/bin/env python3.6
# encoding: utf-8
"""
Este módulo é parte integrante da aplicação Promais Service, desenvolvida por
Victor Domingos e distribuída sob os termos da licença Creative Commons
Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)
"""
import os
import pprint

from sqlalchemy import create_engine, func, or_, and_
from sqlalchemy.orm import sessionmaker
from datetime import datetime

import db_local_base as db_base
import db_local_models as db_models

from misc import calcular_dias_desde
from global_setup import LOCAL_DATABASE_PATH, ESTADOS, ENTREGUE, PRIORIDADES, RESULTADOS


def iniciar_sessao_db():
    engine = create_engine('sqlite+pysqlite:///' + os.path.expanduser(LOCAL_DATABASE_PATH))
    session = sessionmaker()
    session.configure(bind=engine)
    return session(), engine


# TODO
def validate_login(username, password):
    """ Check if username and password match the info in database. Token stuff
        is provided here only to ensure code compatibility for future web API
        access.
    """
    if username == "npk" and password == "...":  # change this
        loggedin = True
        token = "The amazing NPK Token"
    else:
        loggedin = False
        token = None

    return loggedin, token

def get_user_id(username):
    #TODO - return the user ID from database, queried with a string containing the username.
    return(1)

def change_password(username, old_password, new_password1):
    """ Change the password for the given user if the old passowrd matches.
    """
    print("DB: Changing password for the user {username}.")
    result = True  # TODO
    return result


def save_repair(repair):
    print("a guardar o processo de reparação", repair)
    db_last_rep_number = 12341
    return db_last_rep_number


def save_contact(contacto):
    print("a guardar o contacto", contacto)
    db_last_contact_number = "999"
    return db_last_contact_number


def save_remessa(remessa):
    print("a guardar a remessa", remessa)
    db_last_remessa_number = "1984"
    return db_last_remessa_number

def update_repair_status(rep_num, status):
    print(f"A atualizar o estado da reparação nº {rep_num}: {status} ({ESTADOS[status]})")
    reparacao = obter_reparacao(rep_num)

    s, _ = iniciar_sessao_db()

    pass  # TODO atualizar reparacao com novo estado.


def update_repair_priority(rep_num, priority):
    print(f"A atualizar a prioridade da reparação nº {rep_num}: {priority} ({PRIORIDADES[priority]})")
    reparacao = obter_reparacao(rep_num)

    s, _ = iniciar_sessao_db()

    pass  # TODO atualizar reparacao com prioridade.



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


def obter_lista_fornecedores():
    print("A obter lista atualizada de fornecedores e/ou centros técnicos.")
    # TODO:
    fornecedores = ["Loja X",
                    "Importador Nacional A",
                    "Distribuidor Ibérico Y",
                    "Centro de assistência N",
                    "Centro de assistência P",
                    "Centro de assistência K"]

    return fornecedores


def obter_lista_artigos_emprest():
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


def obter_todas_reparacoes():
    s, _ = iniciar_sessao_db()
    reps = s.query(db_models.Repair).all()
    repair_list = [{'id': rep.id,
                    'cliente_nome': rep.cliente.nome,
                    'descr_artigo': rep.product.descr_product,
                    'sn': rep.sn,
                    'descr_servico': rep.descr_servico,
                    'estado': rep.estado_reparacao,
                    'dias': calcular_dias_desde(rep.created_on),
                    'prioridade': rep.prioridade}
                   for rep in reps]

    return repair_list


def obter_reparacoes_por_estados(status_list):
    s, _ = iniciar_sessao_db()
    reparacoes = s.query(db_models.Repair).filter(db_models.Repair.estado_reparacao.in_(status_list))
    reps = reparacoes.all()

    repair_list = [{'id': rep.id,
                    'cliente_nome': rep.cliente.nome,
                    'descr_artigo': rep.product.descr_product,
                    'sn': rep.sn,
                    'descr_servico': rep.descr_servico,
                    'estado': rep.estado_reparacao,
                    'dias': calcular_dias_desde(rep.created_on),
                    'prioridade': rep.prioridade}
                   for rep in reps]

    return repair_list


def pesquisar_reparacoes(txt_pesquisa, estados=[]):
    s, _ = iniciar_sessao_db()

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

    #TODO:

    reps = s.query(db_models.Repair).filter(
        and_(db_models.Repair.estado_reparacao.in_(estados),
            or_(
                db_models.Repair.id.like(termo_pesquisa),
                #db_models.Contact.nome.ilike(termo_pesquisa),
                #db_models.Contact.telefone.ilike(termo_pesquisa),
                #db_models.Contact.telemovel.ilike(termo_pesquisa),
                #db_models.Contact.email.ilike(termo_pesquisa),
                #db_models.Product.descr_product.ilike(termo_pesquisa),
                #db_models.Product.part_number.ilike(termo_pesquisa),
                db_models.Repair.descr_servico.ilike(termo_pesquisa),
                db_models.Repair.notas.ilike(termo_pesquisa),
                db_models.Repair.num_fatura.ilike(termo_pesquisa),
                db_models.Repair.sn.ilike(termo_pesquisa),
        ))).all()
    repair_list = [{'id': rep.id,
                    'cliente_nome': rep.cliente.nome,
                    'descr_artigo': rep.product.descr_product,
                    'sn': rep.sn,
                    'descr_servico': rep.descr_servico,
                    'estado': rep.estado_reparacao,
                    'dias': calcular_dias_desde(rep.created_on),
                    'prioridade': rep.prioridade}
                   for rep in reps]
    return repair_list


def obter_reparacao(num_rep):
    s, _ = iniciar_sessao_db()
    reparacao = s.query(db_models.Repair).get(num_rep)
    return reparacao


def pesquisar_contactos(txt_pesquisa="", tipo="Clientes"):
    s, _ = iniciar_sessao_db()

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
        ))).all()
    else:
        contactos = s.query(db_models.Contact).filter(
        and_(db_models.Contact.is_fornecedor.is_(True),
            or_(
                db_models.Contact.id.like(termo_pesquisa),
                db_models.Contact.nome.ilike(termo_pesquisa),
                db_models.Contact.telefone.ilike(termo_pesquisa),
                db_models.Contact.telemovel.ilike(termo_pesquisa),
                db_models.Contact.email.ilike(termo_pesquisa),
        ))).all()
    contact_list = [{'id': contact.id,
                     'nome': contact.nome,
                     'telefone': contact.telefone,
                     'email': contact.email}
                   for contact in contactos]

    return contact_list


def obter_clientes():
    s, _ = iniciar_sessao_db()
    contactos = s.query(db_models.Contact).filter_by(is_cliente=True).all()
    contact_list = [{'id': contact.id,
                     'nome': contact.nome,
                     'telefone': contact.telefone,
                     'email': contact.email}
                   for contact in contactos]

    return contact_list


def obter_fornecedores():
    s, _ = iniciar_sessao_db()
    contactos = s.query(db_models.Contact).filter_by(is_fornecedor=True).all()
    contact_list = [{'id': contact.id,
                     'nome': contact.nome,
                     'telefone': contact.telefone,
                     'email': contact.email}
                   for contact in contactos]

    return contact_list


def obter_contacto(num_contacto):
    s, _ = iniciar_sessao_db()
    contacto = s.query(db_models.Contact).get(num_contacto)
    return contacto


def obter_mensagens(user_id):
    s, _ = iniciar_sessao_db()
    utilizador = s.query(db_models.User).get(user_id)

    q_msgs = s.query(db_models.UtilizadorNotificadoPorEvento_link) \
                        .filter_by(is_visible=1, user=utilizador)

    msgs = q_msgs.all()
    return msgs


def obter_evento(event_id):
    s, _ = iniciar_sessao_db()
    evento = s.query(db_models.Event).get(event_id)
    return evento
