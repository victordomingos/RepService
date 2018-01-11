#!/usr/bin/env python3.6
# encoding: utf-8
"""
Este módulo é parte integrante da aplicação Promais Service, desenvolvida por
Victor Domingos e distribuída sob os termos da licença Creative Commons
Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)
"""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import db_local_base as db_base
import db_local_models as db_models

from global_setup import LOCAL_DATABASE_PATH


def init_database():
    engine = create_engine('sqlite:///'+os.path.expanduser(LOCAL_DATABASE_PATH))
    session = sessionmaker()
    session.configure(bind=engine)
    db_base.Base.metadata.create_all(engine)


#TODO
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
    #TODO:
    fornecedores = ["Loja X",
                    "Importador Nacional A",
                    "Distribuidor Ibérico Y",
                    "Centro de assistência N",
                    "Centro de assistência P",
                    "Centro de assistência K"]

    return fornecedores
    

def obter_lista_processos_por_receber():
    print("A obter lista atualizada de processos de reparação que falta receber dos fornecedores e/ou centros técnicos.")
    #TODO:
    lista = ["12234 - iPhone 7 128GB Space grey - José manuel da Silva Castro",
            "85738 - MacBook Pro 15\" Retina - Manuel José de Castro Silva",
            "32738 - iPod shuffle 2GB - Laranjas e Limões, Lda.",
            "25720 - Beats X - NPK - Network Project for Knowledge",
            "85738 - MacBook Pro 15\" Retina - Manuel José de Castro Silva",
            "32738 - iPod shuffle 2GB - Laranjas e Limões, Lda."]

    return lista


def obter_lista_processos_por_enviar():
    print("A obter lista atualizada de processos de reparação que falta receber dos fornecedores e/ou centros técnicos.")
    #TODO:
    lista = ["12234 - iPhone 7 128GB Space grey - José manuel da Silva Castro",
            "85738 - MacBook Pro 15\" Retina - Manuel José de Castro Silva",
            "32738 - iPod shuffle 2GB - Laranjas e Limões, Lda.",
            "25720 - Beats X - NPK - Network Project for Knowledge",
            "85738 - MacBook Pro 15\" Retina - Manuel José de Castro Silva",
            "32738 - iPod shuffle 2GB - Laranjas e Limões, Lda."]

    return lista



def obter_lista_fornecedores():
    print("A obter lista atualizada de fornecedores e/ou centros técnicos.")
    #TODO:
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
    #TODO:
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

    
def test_populate():
    loja = db_models.Loja(nome="That Great NPK Store")
    utilizador = db_models.User(username="utilizador"+str(i), email="test@networkprojectforknowledge.org"+str(i), password="1234", loja=loja)
    contacto = db_models.Contact()
    artigo = db_models.Artigo()
    reparacao = db_models.Repair()
    
    loja.utilizadores.append(utilizador)
    
    session.add(loja)
    session.commit()
    
    #print(new_user)
    #session.add(new_user)
    #session.commit()
    #print(">", new_user)

    #our_user = session.query(User).filter_by(username='Victor1').first()
    #print("OUR USER:", our_user)


if __name__ == "__main__":    
    # Testing...
    init_database()
    test_populate()
    
    


    
