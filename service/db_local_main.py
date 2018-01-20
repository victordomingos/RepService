#!/usr/bin/env python3.6
# encoding: utf-8
"""
Este módulo é parte integrante da aplicação Promais Service, desenvolvida por
Victor Domingos e distribuída sob os termos da licença Creative Commons
Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)
"""
import os
import pprint

from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from datetime import datetime


import db_local_base as db_base
import db_local_models as db_models

from global_setup import LOCAL_DATABASE_PATH

def delete_database():
    engine = create_engine(
        'sqlite+pysqlite:///' + os.path.expanduser(LOCAL_DATABASE_PATH))
    session = sessionmaker()
    session.configure(bind=engine)
    db_base.Base.metadata.drop_all(engine)


def init_database():
    engine = create_engine(
        'sqlite+pysqlite:///' + os.path.expanduser(LOCAL_DATABASE_PATH))
    session = sessionmaker()
    session.configure(bind=engine)
    db_base.Base.metadata.create_all(engine)
    

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


def change_password(username, old_password, new_password1):
    """ Change the password for the given user if the old passowrd matches.
    """
    print("DB: Changing password for the user {username}.")
    result = True  # TODO
    return result


def save_repair(rep_num):
    print("a guardar o processo de reparação", rep_num)
    db_last_rep_number = "1234"
    return db_last_rep_number


def save_contact(contacto):
    print("a guardar o contacto", contacto)
    db_last_contact_number = "999"
    return db_last_contact_number


def save_remessa(remessa):
    print("a guardar a remessa", remessa)
    db_last_remessa_number = "1984"
    return db_last_remessa_number


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





# ----------------------------------------------------------------------------------------
# Just a bunch of experiences to get the hang of SQLalchemy while developing the models...
# ----------------------------------------------------------------------------------------


def test_populate():
    engine = create_engine('sqlite+pysqlite:///' + os.path.expanduser(LOCAL_DATABASE_PATH))
    session = sessionmaker()
    session.configure(bind=engine)
    s = session()
    
    print("A inserir lojas...")
    for i in range(2):
        loja = db_models.Loja(nome=f"That Great NPK Store #{str(i)}")
        s.add(loja)

    s.commit()

    print("A inserir utilizadores...")
    lojas = s.query(db_models.Loja).all()
    for i in range(15):
        lojinha = lojas[i % 2]
        utilizador = db_models.User(username="utilizador" + str(i), email="test@networkprojectforknowledge.org" + str(i), password="abc1234567", loja=lojinha)
        s.add(utilizador)

    s.commit()


    print("A inserir contactos de clientes e fornecedores...")
    utilizadores = s.query(db_models.User).all()
    nomes = ("José", "Manuel", "Maria", "Guilhermina", "Estêvão", "Joaninha", "Apólito", "John")
    apelidos = ("Laranja", "Bonito", "Santiago", "de Malva e Cunha", "Azeredo", "Starck", "Brückner")
    empresas = ("", "NPK", "NPK - Network project for Knowledge", "Aquela Empresa Faltástica, S.A.", "", "")
    telefones = ("222000000", "960000000", "+351210000000")
    from random import choice
    for i in range(1000):
        contacto = db_models.Contact(
            nome=f"{choice(nomes)} {choice(apelidos)}", 
            empresa=choice(empresas),
            telefone=choice(telefones),
            telemovel = choice(telefones),
            telefone_empresa = choice(telefones),
            email="test@networkprojectforknowledge.org",
            morada = "Rua da Santa Paciência Que Nos Acuda Em Dias Daqueles\nEdifício Especial XXI, porta 789, 3º Esquerdo Trás",
            cod_postal = "4700-000",
            localidade = "Braga",
            pais = "Portugal das Maravilhas",
            nif = "999999990",
            notas = "Apontamentos adicionais sobre este contacto...",
            is_cliente = 1,
            is_fornecedor = 0,
            criado_por_utilizador = choice(utilizadores))
        s.add(contacto)

    s.commit()

    
    print("A inserir artigos...")
    for i in range(1500):
        artigo = db_models.Artigo(descr_artigo=f"Aquele artigo número {str(i)}", part_number="NPKPN662"+str(i)+"ZQ"+str(i))
        s.add(artigo)

    s.commit()

    print("A inserir reparações...")
    contactos = s.query(db_models.Contact).all()
    artigos = s.query(db_models.Artigo).all()
    utilizadores = s.query(db_models.User).all()
    for i in range(3500):
        print("i:", i)
        reparacao = db_models.Repair(
            cliente = contactos[i%15],
            artigo = artigos[i%1500],
            sn = "W123132JJG123B123ZLT",
            fornecedor = contactos[(i+5)%15],
            estado_artigo = 1,
            obs_estado = "Marcas de acidente, com amolgadelas e vidro partido",
            is_garantia = 0,
            data_compra = datetime(2017,1,31),
            num_fatura = "12345FC",
            loja_compra = "NPK Store",
            desc_servico = "Tentar ressuscitar o dispositivo",
            avaria_reprod_loja = True,
            requer_copia_seg = 0,
            is_find_my_ativo = 1,
            Senha = "123456",
            acessorios_entregues = "Bolsa da marca NPK Accessories",
            notas = "",
            local_reparacao = contactos[i%2],
            estado_reparacao = 3,
            fatura_fornecedor = "FC123400001",
            nar_autorizacao_rep = "1234000",
            data_fatura_fornecedor = datetime(2017,1,31),
            num_guia_rececao = "123455",
            data_guia_rececao = datetime(2017,1,31),
            cod_resultado_reparacao = 4,
            descr_detalhe_reparacao = "Foi substituído em garantia o neurónio avariado",
            novo_sn_artigo = "G1231000TYZ",
            notas_entrega = "Entregue a José Manuel da Silva Curioso",

            utilizador_entrega = utilizadores[(i+5)%15],

            data_entrega = datetime(2017,1,31),
            num_quebra_stock = "1234",
            is_stock = 0,
            modo_entrega = 0,
            reincidencia_processo_id = 123,
            morada_entrega = "",

            criado_por_utilizador = utilizadores[i%15])
        s.add(reparacao)

    s.commit()


def print_database():
    engine = create_engine('sqlite+pysqlite:///' + os.path.expanduser(LOCAL_DATABASE_PATH))
    session = sessionmaker()
    session.configure(bind=engine)
    s = session()

    lojas = s.query(db_models.Loja).all()
    utilizadores = s.query(db_models.User).all()
    contactos = s.query(db_models.Contact).all()
    artigos = s.query(db_models.Artigo).all()
    reparacoes = s.query(db_models.Repair).all()

    print("\n========================\n          LOJAS\n========================")
    for lojinha in lojas:
        print(f"\nA loja {lojinha.nome}, com o ID {lojinha.id}, tem os seguintes utilizadores:)")
        pprint.pprint([(u.id, u.username) for u in lojinha.users])


    print("\n==============================\n         UTILIZADORES\n==============================")
    for utilizador in utilizadores:
        print(f"\nO utilizador {utilizador.username} tem o ID {utilizador.id} pertence à loja: {utilizador.loja_id} ({utilizador.loja.nome})")        


    print("\n==============================\n          CONTACTOS\n==============================")
    for contacto in contactos:
        print(contacto)
        print("\nReparações como cliente:")
        pprint.pprint([(rep.id, rep.artigo.descr_artigo, rep.cliente.nome) for rep in contacto.reparacoes_como_cliente])
        print("\nReparações como fornecedor:")
        pprint.pprint([(rep.id, rep.artigo.descr_artigo, rep.cliente.nome) for rep in contacto.reparacoes_como_fornecedor])


    print("\n========================\n           ARTIGOS\n========================")
    for artigo in artigos:
        pprint.pprint(artigo)

    print("\n========================\n           REPARAÇÕES\n========================")
    for reparacao in reparacoes:
        pprint.pprint(reparacao)
    

if __name__ == "__main__":
    # Testing...
    delete_database()
    init_database()
    test_populate()
    print_database()

