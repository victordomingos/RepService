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

from global_setup import LOCAL_DATABASE_PATH, ESTADOS, ENTREGUE, PRIORIDADES, RESULTADOS


def iniciar_sessao_db():
    engine = create_engine('sqlite+pysqlite:///' + os.path.expanduser(LOCAL_DATABASE_PATH))
    session = sessionmaker()
    session.configure(bind=engine)
    return session(), engine


def delete_database():
    _, engine = iniciar_sessao_db()
    db_base.Base.metadata.drop_all(engine)


def init_database():
    _, engine = iniciar_sessao_db()
    db_base.Base.metadata.create_all(engine)


def calcular_dias_desde(data):
    """ Calcular número de dias que passaram desde data indicada.
        Ex: calcular_dias_desde(data)
        Nota: Requer data no formato datetime.today()
    """
    hoje = datetime.today()
    diferenca = hoje - data
    return diferenca.days   # nº de dias que já passaram


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

    engine = create_engine('sqlite+pysqlite:///' + os.path.expanduser(LOCAL_DATABASE_PATH))
    session = sessionmaker()
    session.configure(bind=engine)
    s = session()

    pass  # TODO atualizar reparacao com novo estado.


def update_repair_priority(rep_num, priority):
    print(f"A atualizar a prioridade da reparação nº {rep_num}: {priority} ({PRIORIDADES[priority]})")
    reparacao = obter_reparacao(rep_num)

    engine = create_engine('sqlite+pysqlite:///' + os.path.expanduser(LOCAL_DATABASE_PATH))
    session = sessionmaker()
    session.configure(bind=engine)
    s = session()

    pass  # TODO atualizar reparacao com prioridade.




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
    #print(repair_list)

    return repair_list


def obter_reparacoes_por_estados(status_list):
    print("A obter:", status_list)
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
    #print(repair_list)

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

    #TODO: restringir a pesquisa aos registos que tenham o estado selecionado


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


# ----------------------------------------------------------------------------------------
# Just a bunch of experiences to get the hang of SQLalchemy while developing the models...
# ----------------------------------------------------------------------------------------


def test_populate(num_lojas=1, num_utilizadores=1, num_contactos=1, num_artigos=1, num_reparacoes=1):
    s, _ = iniciar_sessao_db()
    print("A inserir dados de exemplo na base de dados.\n")

    for i in range(num_lojas):
        print(f"{'  - A inserir lojas...'.ljust(55)}{i+1:7}", end="\r")
        loja = db_models.Loja(nome=f"That Great NPK Store #{str(i)}")
        s.add(loja)

    s.commit()

    print("")
    lojas = s.query(db_models.Loja)
    admin = db_models.User(nome="npk", email="admin@networkprojectforknowledge.org", password="...", loja=lojas.get(1))
    s.add(admin)
    lojas = lojas.all()
    for i in range(num_utilizadores):
        print(f"{'  - A inserir utilizadores...'.ljust(55)}{i+1:7}", end="\r")
        lojinha = lojas[i % 2]
        utilizador = db_models.User(nome="utilizador" + str(i), email="test@networkprojectforknowledge.org" + str(i), password="abc1234567", loja=lojinha)
        s.add(utilizador)

    s.commit()


    print("")
    utilizadores = s.query(db_models.User).all()
    nomes = ("José", "Rita", "Shawn", "Francelina", "Eufrazina", "Eleutério", "Joana Manuela", "Manuel", "Maria", "Guilhermina", "Estêvão", "Joaninha", "Apólito", "John", "Loja X")
    apelidos = ("Laranja", "Bonito", "Santiago", "de Malva e Cunha", "Azeredo", "Starck", "Brückner", "Apolinário Gomes Fernandes", "Carvalho", "Rodrigues", "Ló")
    empresas = ("", "NPK", "NPK - Network project for Knowledge", "Aquela Empresa Faltástica, S.A.", "", "")
    telefones = ("222000000", "960000000", "+351210000000")
    emails = ("test", "info", "npk", "theworldisavampire", "florzinha98", "josefloresmanuel", "mariazinha1978")
    dominios = ("networkprojectforknowledge.org", "baratatonta2001.com.br", "thegreatnpkdomain.com", "zbxvsga.pt", "ihopethisdomaindoesnotexist.net")
    is_cliente = (True, False)
    is_fornecedor = (*20*(False,), True)

    from random import choice
    for i in range(num_contactos):
        print(f"{'  - A inserir contactos (clientes e fornecedores)...'.ljust(55)}{i+1:7}", end="\r")
        forn = choice(is_fornecedor)

        if forn:
            cli = choice(is_cliente)
        else:
            cli = True

        if i == 0:
            atualizado_por_utilizador = None
        else:
            atualizado_por_utilizador = choice(utilizadores)

        contacto = db_models.Contact(
            nome=f"{choice(nomes)} {choice(apelidos)}",
            empresa=choice(empresas),
            telefone=choice(telefones),
            telemovel = choice(telefones),
            telefone_empresa = choice(telefones),
            email=choice(emails) + "@" + choice(dominios),
            morada = "Rua da Santa Paciência Que Nos Acuda Em Dias Daqueles\nEdifício Especial XXI, porta 789, 3º Esquerdo Trás",
            cod_postal = "4700-000",
            localidade = "Braga",
            pais = "Portugal",
            nif = "999999990",
            notas = "Apontamentos adicionais sobre este contacto...",
            is_cliente = bool(cli),
            is_fornecedor = bool(forn),
            criado_por_utilizador = choice(utilizadores),
            atualizado_por_utilizador = atualizado_por_utilizador)
        s.add(contacto)

    s.commit()


    print("")
    artigos = ("Artigo Muito Jeitoso (Early 2015)", "Outro Artigo Bem Jeitoso",
        "Smartphone Daqueles Bons", "Computador do modelo ABCD",
        "Coisa que não funciona devidamente", "Coisa que devia funcionar melhor")

    for i in range(num_artigos):
        print(f"{'  - A inserir artigos...'.ljust(55)}{i+1:7}", end="\r")

        artigo = db_models.Product(descr_product=choice(artigos), part_number="NPKPN662"+str(i)+"ZQ"+str(i))
        s.add(artigo)

    s.commit()

    print("")
    contactos = s.query(db_models.Contact).all()
    num_contactos = s.query(db_models.Contact).count()
    artigos = s.query(db_models.Product).all()
    num_artigos = s.query(db_models.Product).count()
    utilizadores = s.query(db_models.User).all()
    num_utilizadores = s.query(db_models.User).count()
    servicos = ("Substituição de ecrã", "Bateria não carrega",
        "Formatar disco e reinstalar sistema operativo",
        "Substituição ao abrigo da garantia")

    for i in range(num_reparacoes):
        print(f"{'  - A inserir reparações...'.ljust(55)}{i+1:7}", end="\r")
        if (i%2 == 1) or (i%3 == 0) or (i%10 == 0) or i<1000 or i>1150:
            estado = ENTREGUE
        else:
            estado = choice(list(ESTADOS.keys()))
        reparacao = db_models.Repair(
            cliente = contactos[i%num_contactos],
            product = artigos[i%num_artigos],
            sn = "W123132JJG123B123ZLT",
            fornecedor = contactos[(i+5)%num_contactos],
            estado_artigo = 1,
            obs_estado = "Marcas de acidente, com amolgadelas e vidro partido",
            is_garantia = 0,
            data_compra = datetime(2017,1,31),
            num_fatura = "12345FC",
            loja_compra = "NPK Store",
            descr_servico = choice(servicos),
            avaria_reprod_loja = True,
            requer_copia_seg = 0,
            is_find_my_ativo = 1,
            senha = "123456",
            acessorios_entregues = "Bolsa da marca NPK Accessories",
            notas = "",
            local_reparacao = contactos[i%2],
            estado_reparacao = estado,
            fatura_fornecedor = "FC123400001",
            nar_autorizacao_rep = "1234000",
            data_fatura_fornecedor = datetime(2017,1,31),
            num_guia_rececao = "123455",
            data_guia_rececao = datetime(2017,1,31),
            cod_resultado_reparacao = choice(list(RESULTADOS.keys())),
            descr_detalhe_reparacao = "Foi substituído em garantia o neurónio avariado",
            novo_sn_artigo = "G1231000TYZ",
            notas_entrega = "Entregue a José Manuel da Silva Curioso",

            utilizador_entrega = utilizadores[(i+5)%num_utilizadores],
            prioridade = choice(list(PRIORIDADES.items())),
            data_entrega = datetime(2017,1,31),
            num_quebra_stock = "1234",
            is_stock = 0,
            modo_entrega = 0,
            cliente_pagou_portes = 0,
            reincidencia_processo_id = 123,
            morada_entrega = "",

            criado_por_utilizador = utilizadores[i%num_utilizadores])
        s.add(reparacao)

    s.commit()


    print("")
    reparacoes = s.query(db_models.Repair).all()
    utilizadores = s.query(db_models.User).all()
    count = 0
    rep = reparacoes[1]
    for rep in reparacoes:
        print(f"{'  - A inserir eventos...'.ljust(55)}{count+1:7}", end="\r")
        count +=1
        #print("event in rep", rep)
        # create parent, append a child via association
        evento1 = db_models.Event(
            repair_id = rep.id,
            descricao = "Cliente enviou por email a fatura para anexar ao processo de garantia.",
            criado_por_utilizador = choice(utilizadores))

        link = db_models.UtilizadorNotificadoPorEvento_link(
            is_visible=choice([False, True]),
            is_open=choice([True, False]))

        link.user = choice(utilizadores)
        evento1.utilizadores.append(link)
        s.add(evento1)

        textos = ("Centro técnico pediu para questionar cliente sobre algo importante.",
                  "Falta enviar a fatura para garantia.")
        if count % 2 == 0:
            #print("if rep event")
            evento2 = db_models.Event(
                repair_id = rep.id,
                descricao = choice(textos),
                criado_por_utilizador = utilizadores[0])

            link2 = db_models.UtilizadorNotificadoPorEvento_link(
                is_visible=choice([True, False]),
                is_open=choice([False, True]))
            link2.user = utilizadores[0]
            evento2.utilizadores.append(link2)
            s.add(evento2)
            if count >=50:
                break

    s.commit()

    db_filesize = os.path.getsize(os.path.expanduser(LOCAL_DATABASE_PATH)) >> 10
    print(f"\n\nOperação terminada.\nTamanho atual da base de dados: {db_filesize/1024:.1f}MB\n")


def print_database():
    s, _ = iniciar_sessao_db()

    lojas = s.query(db_models.Loja).all()
    utilizadores = s.query(db_models.User).all()
    contactos = s.query(db_models.Contact).all()
    artigos = s.query(db_models.Product).all()
    #reparacoes = s.query(db_models.Repair).all()
    eventos = s.query(db_models.Event).all()
    eventos_visiveis = s.query(db_models.UtilizadorNotificadoPorEvento_link).filter_by(is_visible=1, user=utilizadores[2])

    print("\n========================\n          LOJAS\n========================")
    for lojinha in lojas:
        print(f"\nA loja {lojinha.nome}, com o ID {lojinha.id}, tem os seguintes utilizadores:)")
        pprint.pprint([(u.id, u.nome) for u in lojinha.users])


    print("\n==============================\n         UTILIZADORES\n==============================")
    for utilizador in utilizadores:
        print(f"\nO utilizador {utilizador.nome} tem o ID {utilizador.id} pertence à loja: {utilizador.loja_id} ({utilizador.loja.nome})")


    print("\n==============================\n          CONTACTOS\n==============================")
    for contacto in contactos:
        print(contacto)
        print("\nReparações como cliente:")
        pprint.pprint([(rep.id, rep.product.descr_product, rep.cliente.nome) for rep in contacto.reparacoes_como_cliente])
        print("\nReparações como fornecedor:")
        pprint.pprint([(rep.id, rep.product.descr_product, rep.cliente.nome) for rep in contacto.reparacoes_como_fornecedor])


    print("\n========================\n           ARTIGOS\n========================")
    for artigo in artigos:
        pprint.pprint(artigo)


    print("\n========================\n           REPARAÇÕES\n========================")
    for reparacao in reparacoes:
        pprint.pprint(reparacao)

    print("\n========================\n           EVENTOS\n========================")
    for evento in eventos:
        pprint.pprint(evento)

    print("\n========================\n           EVENTOS Visíveis\n========================")
    for link in eventos_visiveis:
        pprint.pprint(link.event)


if __name__ == "__main__":
    # Testing...
    delete_database()
    init_database()
    
    lojas = 2
    
    utilizadores = lojas * 8
    contactos = lojas * 750
    artigos = lojas * 500
    reps = lojas * 1000
    
    test_populate(num_lojas=lojas,
                  num_utilizadores=utilizadores,
                  num_contactos=contactos,
                  num_artigos=artigos,
                  num_reparacoes=int(reps))
    #print_database()
