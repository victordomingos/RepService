#!/usr/bin/env python3.6
# encoding: utf-8
"""
Este módulo é parte integrante da aplicação Promais Service, desenvolvida por
Victor Domingos e distribuída sob os termos da licença Creative Commons
Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)
"""


from datetime import datetime
import os

from sqlalchemy import (create_engine, Table, Column, Integer, String,
                        ForeignKey, MetaData, DateTime)

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker


from global_setup import LOCAL_DATABASE_PATH

metadata = MetaData()
Base = declarative_base(metadata=metadata)



class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, autoincrement=True, primary_key=True, nullable=False)
    username = Column(String, index=True, nullable=False, unique=True)
    email = Column(String, index=True, nullable=False, unique=True)
    password = Column(String, nullable=False, unique=False)
    pwd_last_changed = Column(DateTime(), default=datetime.now)
    created_on = Column(DateTime(), default=datetime.now)
    updated_on = Column(DateTime(), default=datetime.now, onupdate=datetime.now)

    def __repr__(self):
        return f"<User(id={self.id}, name='{self.username}', email='{self.email}', password='{self.password}')>"


def init_database():
    engine = create_engine('sqlite:///'+os.path.expanduser(LOCAL_DATABASE_PATH))
    metadata.create_all(engine)

    """
    repairs = Table('repairs', metadata,
        Column('id', Integer, primary_key=True),
        Column('cliente_id', Integer, ForeignKey("contacts.id"),
        Column('cliente_id', Integer, ForeignKey("contacts.id"),
        Column('email', String(255), index=True, nullable=False, unique=True),
        Column('password', String(255), nullable=False, unique=False),
        Column('pwd_last_changed', DateTime(), default=datetime.now),
        Column('created_on', DateTime(), default=datetime.now),
        Column('updated_on', DateTime(), default=datetime.now, onupdate=datetime.now),
    )

    repairs = Table('contacts', metadata,
        Column('id', Integer, primary_key=True),
        Column('cliente_id', Integer, ForeignKey("contacts.id"),
        Column('email', String(255), index=True, nullable=False, unique=True),
        Column('password', String(255), nullable=False, unique=False),
        Column('pwd_last_changed', DateTime(), default=datetime.now),
        Column('created_on', DateTime(), default=datetime.now),
        Column('updated_on', DateTime(), default=datetime.now, onupdate=datetime.now),
    )
    """







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



if __name__ == "__main__":    
    # Testing...
    init_database()
    engine = create_engine('sqlite:///'+os.path.expanduser(LOCAL_DATABASE_PATH))
    Session = sessionmaker(bind=engine)
    session = Session()

    for i in range(100):
        new_user = User(username="Victor"+str(i), email="test@networkprojectforknowledge.org"+str(i), password="1234")
        print(new_user)
        session.add(new_user)
        session.commit()
        print(">", new_user)
    

    our_user = session.query(User).filter_by(username='Victor1').first()
    print("OUR USER:", our_user)
    
