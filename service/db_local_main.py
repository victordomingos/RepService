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
    

    for i in range(50):
        loja = db_models.Loja(nome=f"That Great NPK Store #{str(i)}")
        s.add(loja)

    s.commit()


    lojas = s.query(db_models.Loja).all()
    for i in range(500):
        lojinha = lojas[i % 50]
        utilizador = db_models.User(username="utilizador" + str(i), email="test@networkprojectforknowledge.org" + str(i), password="abc1234567", loja=lojinha)
        s.add(utilizador)

    s.commit()



    utilizadores = s.query(db_models.User).all()
    nomes = ("José", "Manuel", "Maria", "Guilhermina", "Estêvão", "Joaninha", "Apólito", "John")
    apelidos = ("Laranja", "Bonito", "Santiago", "de Malva e Cunha", "Azeredo", "Starck", "Brückner")
    empresas = ("", "NPK", "NPK - Network project for Knowledge", "Aquela Empresa Faltástica, S.A.", "", "")
    telefones = ("222000000", "960000000", "+351210000000")
    from random import choice
    for i in range(3000):
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

    

    for i in range(5000):
        artigo = db_models.Artigo(descr_artigo=f"Aquele artigo número {str(i)}", part_number="NPKPN662"+str(i)+"ZQ"+str(i))
        s.add(artigo)

    s.commit()


    #reparacao = db_models.Repair()



def print_database():
    engine = create_engine('sqlite+pysqlite:///' + os.path.expanduser(LOCAL_DATABASE_PATH))
    session = sessionmaker()
    session.configure(bind=engine)
    s = session()

    lojas = s.query(db_models.Loja).all()
    utilizadores = s.query(db_models.User).all()
    contactos = s.query(db_models.Contact).all()
    artigos = s.query(db_models.Artigo).all()

    print("========================")
    print("          LOJAS")
    print("========================\n")
    for lojinha in lojas:
        pprint.pprint(lojinha)
        print("")
        pprint.pprint(lojinha.users)
        print("\n")


    print("==============================")
    print("        UTILIZADORES")
    print("==============================\n")
    for utilizador in utilizadores:
        pprint.pprint(utilizador)
        pprint.pprint(utilizador.loja)
        print(f"O utilizador {utilizador.username} tem o ID {utilizador.id} pertence à loja: {utilizador.loja_id} ({utilizador.loja.nome})")
        print("\n")
        


    print("==============================")
    print("        CONTACTOS")
    print("==============================\n")
    for contacto in contactos:
        pprint.pprint(contacto)
        #pprint.pprint(contacto.reparacoes)
        #print(f"O utilizador {utilizador.username} tem o ID {utilizador.id} pertence à loja: {utilizador.loja_id} ({utilizador.loja.nome})")
        #print("\n")


    print("========================")
    print("          ARTIGOS")
    print("========================\n")
    for artigo in artigos:
        pprint.pprint(artigo)



if __name__ == "__main__":
    # Testing...
    delete_database()
    init_database()
    test_populate()
    print_database()

