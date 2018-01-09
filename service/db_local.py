#!/usr/bin/env python3.6
# encoding: utf-8
"""
Este módulo é parte integrante da aplicação Promais Service, desenvolvida por
Victor Domingos e distribuída sob os termos da licença Creative Commons
Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)
"""
#from datetime import datetime
import os
from sqlalchemy import create_engine
from sqlalchemy import (Column, Integer, String,
                        ForeignKey, MetaData, DateTime, func)

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm import sessionmaker


from global_setup import LOCAL_DATABASE_PATH

Base = declarative_base()


class Loja(Base):
    __tablename__ = 'loja'
    id = Column(Integer, primary_key=True)
    nome = Column(String)
    utilizadores = relationship('Utilizador', secondary='loja_utilizador_link')
    
    def __repr__(self):
        return f"<Loja(id={self.id}, Nome='{self.nome}', Utilizadores='{self.utilizadores}'>"


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String, index=True, nullable=False, unique=True)
    email = Column(String, index=True, nullable=False)
    password = Column(String, nullable=False, unique=False)
    lojas = relationship(Loja, secondary='loja_utilizador_link')
    pwd_last_changed = Column(DateTime(), default=func.now)
    created_on = Column(DateTime(), default=func.now)
    updated_on = Column(DateTime(), default=func.now, onupdate=func.now)

    def __repr__(self):
        return f"<User(id={self.id}, name='{self.username}', email='{self.email}', password='{self.password}', loja={self.loja})>"


class LojaUtilizadorLink(Base):
    __tablename__ = 'loja_utilizador_link'
    loja_id = Column(Integer, ForeignKey('loja.id'), primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)



class Contact(Base):
    __tablename__ = 'contact'
    id = Column(Integer, primary_key=True)
    nome = Column(String, index=True, nullable=False, unique=True)
    empresa = Column(String, index=True, nullable=False)
    telefone = Column(String) 
    telemovel = Column(String)  
    telefone_empresa = Column(String) 
    email = Column(String) 
    morada = Column(String) 
    cod_postal = Column(String) 
    localidade = Column(String) 
    pais = Column(String) 
    nif = Column(String) 
    notas = Column(String) 
    is_cliente = Column(Integer) 
    is_fornecedor = Column(Integer) 
    is_loja = Column(Integer) 
    criado_por_utilizador_id = Column(Integer, ForeignKey('user.id'))
    criado_por_utilizador = relationship(User, backref=backref('users', uselist=True))
    created_on = Column(DateTime(), default=func.now)
    updated_on = Column(DateTime(), default=func.now, onupdate=func.now)

    def __repr__(self):
        return f"<Contact(id={self.id}, name='{self.nome}', empresa='{self.empresa}', is_cliente='{self.is_cliente}', is_fornecedor='{self.is_fornecedor}', is_loja='{self.is_loja}')>"


class Artigo(Base):
    __tablename__ = 'artigo'
    id = Column(Integer, primary_key=True)
    descr_artigo = Column(String, index=True, nullable=False)
    part_number = Column(String, index=True)

    def __repr__(self):
        return f"<Article(id={self.id}, descr_artigo='{self.descr_artigo}', P/N='{self.part_number}'>"


class Repair(Base):
    __tablename__ = 'repair'
    id = Column(Integer, primary_key=True)
    cliente_id = Column(Integer, ForeignKey('contact.id'))
    cliente = relationship(Contact, backref=backref('contacts', uselist=True))
    artigo_id = Column(Integer, ForeignKey('artigo.id'))
    artigo = relationship(Artigo, backref=backref('artigos', uselist=True))
    sn = Column(String) 
    fornecedor_id = Column(Integer, ForeignKey('contact.id'))
    fornecedor = relationship(Contact, backref=backref('contacts', uselist=True))
    estado_artigo = Column(Integer) 
    obs_estado = Column(String) 
    is_garantia = Column(Integer) 
    data_compra = Column(DateTime())
    num_fatura = Column(String) 
    loja_compra = Column(String) 
    desc_servico = Column(String) 
    avaria_reprod_loja = Column(String) 
    requer_copia_seg = Column(String) 
    is_find_my_ativo = Column(Integer) 
    Senha = Column(String) 
    acessorios_entregues = Column(String) 
    notas = Column(String) 
    local_reparacao = Column(Integer) 
    estado_reparacao = Column(String) 
    fatura_fornecedor = Column(String) 
    nar_autorizacao_rep  = Column(String) 
    data_fatura_fornecedor  = Column(String) 
    num_guia_rececao = Column(String) 
    data_guia_rececao = Column(String) 
    cod_resultado_reparacao = Column(String) 
    descr_detalhe_reparacao = Column(String) 
    novo_sn_artigo = Column(String) 
    notas_entrega = Column(String) 
    utilizador_entrega_id = Column(Integer, ForeignKey('user.id'))
    utilizador_entrega = relationship(User, backref=backref('users', uselist=True))
    data_entrega = Column(DateTime())     
    num_quebra_stock = Column(String) 
    is_stock = Column(Integer)
    modo_entrega = Column(Integer) 
    reincidencia_processo_id = Column(Integer) 
    morada_entrega = Column(String) 
    criado_por_utilizador_id = Column(Integer, ForeignKey('user.id'))
    criado_por_utilizador = relationship(User, backref=backref('users', uselist=True))
    created_on = Column(DateTime(), default=func.now)
    updated_on = Column(DateTime(), default=func.now, onupdate=func.now)

    def __repr__(self):
        return f"<Repair(id={self.id})>"


def init_database():
    engine = create_engine('sqlite:///'+os.path.expanduser(LOCAL_DATABASE_PATH))
    session = sessionmaker()
    session.configure(bind=engine)
    Base.metadata.create_all(engine)


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


def test_lojas():
    l = Loja()
    
def test_users():
    for i in range(100):
        new_user = User(username="utilizador"+str(i), email="test@networkprojectforknowledge.org"+str(i), password="1234", loja=123)
        print(new_user)
        session.add(new_user)
        session.commit()
        print(">", new_user)

    our_user = session.query(User).filter_by(username='Victor1').first()
    print("OUR USER:", our_user)


if __name__ == "__main__":    
    # Testing...
    init_database()
    #test_lojas()
    #test_users()
    
    


    
