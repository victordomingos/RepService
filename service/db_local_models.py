#!/usr/bin/env python3.6
# encoding: utf-8
"""
Este módulo é parte integrante da aplicação Promais Service, desenvolvida por
Victor Domingos e distribuída sob os termos da licença Creative Commons
Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)
"""
from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey, MetaData, DateTime, func
from sqlalchemy.orm import relationship, backref

from db_local_base import Base


class Loja(Base):
    __tablename__ = 'loja'
    id = Column(Integer, primary_key=True)
    nome = Column(String)
    
    def __repr__(self):
        return f"<Loja(id={self.id}, Nome='{self.nome}')>"


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    
    loja_id = Column(Integer, ForeignKey('loja.id'))
    loja = relationship(Loja, backref=backref('users', uselist=True))
    
    pwd_last_changed = Column(DateTime(), default=func.now())
    created_on = Column(DateTime(), default=func.now())
    updated_on = Column(DateTime(), default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<User(id={self.id}, name='{self.username}', email='{self.email}', password='{self.password}', loja={self.loja})>"

"""
class LojaUtilizadorLink(Base):
    __tablename__ = 'loja_utilizador_link'
    loja_id = Column(Integer, ForeignKey('loja.id'), primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
"""

class Contact(Base):
    __tablename__ = 'contact'
    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    empresa = Column(String)
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
    is_cliente = Column(Boolean)
    is_fornecedor = Column(Boolean)
    #is_loja = Column(Integer)
    #reparacoes = relationship('Repair', backref='contact', uselist=True)  # TODO

    criado_por_utilizador_id = Column(Integer, ForeignKey('user.id'))
    criado_por_utilizador = relationship(User, backref=backref('users', uselist=True))
    created_on = Column(DateTime(), default=func.now())
    updated_on = Column(DateTime(), default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<Contact(id={self.id}, name='{self.nome}', empresa='{self.empresa}', is_cliente='{self.is_cliente}', is_fornecedor='{self.is_fornecedor}'>"


class Artigo(Base):
    __tablename__ = 'artigo'
    id = Column(Integer, primary_key=True)
    descr_artigo = Column(String, nullable=False)
    part_number = Column(String)

    def __repr__(self):
        return f"<Article(id={self.id}, descr_artigo='{self.descr_artigo}', P/N='{self.part_number}'>"



class Repair(Base):
    __tablename__ = 'repair'
    id = Column(Integer, primary_key=True)

    cliente_id = Column(Integer, ForeignKey('contact.id'))
    cliente = relationship("Contact",  foreign_keys=[cliente_id])

    artigo_id = Column(Integer, ForeignKey('artigo.id'))
    artigo = relationship("Artigo", foreign_keys=[artigo_id])

    sn = Column(String)

    fornecedor_id = Column(Integer, ForeignKey('contact.id'))
    fornecedor = relationship("Contact", foreign_keys=[fornecedor_id])

    estado_artigo = Column(Integer)
    obs_estado = Column(String)
    is_garantia = Column(Integer)
    data_compra = Column(Date)
    num_fatura = Column(String)
    loja_compra = Column(String)
    desc_servico = Column(String)
    avaria_reprod_loja = Column(Boolean)
    requer_copia_seg = Column(Integer)
    is_find_my_ativo = Column(Integer)
    Senha = Column(String)
    acessorios_entregues = Column(String)
    notas = Column(String)

    local_reparacao_id = Column(Integer, ForeignKey('contact.id'))
    local_reparacao = relationship("Contact", foreign_keys=[local_reparacao_id])

    estado_reparacao = Column(Integer)
    fatura_fornecedor = Column(String)
    nar_autorizacao_rep = Column(String)
    data_fatura_fornecedor = Column(Date)
    num_guia_rececao = Column(String)
    data_guia_rececao = Column(Date)
    cod_resultado_reparacao = Column(Integer)
    descr_detalhe_reparacao = Column(String)
    novo_sn_artigo = Column(String)
    notas_entrega = Column(String)

    utilizador_entrega_id = Column(Integer, ForeignKey('user.id'))
    utilizador_entrega = relationship(User, foreign_keys=[utilizador_entrega_id])

    data_entrega = Column(DateTime())
    num_quebra_stock = Column(String)
    is_stock = Column(Boolean)
    modo_entrega = Column(Integer)
    reincidencia_processo_id = Column(Integer) #TODO ? apenas 1 processo, ou lista de todas as reincidências?
    morada_entrega = Column(String)

    criado_por_utilizador_id = Column(Integer, ForeignKey('user.id'))
    criado_por_utilizador = relationship(User, foreign_keys=[criado_por_utilizador_id])
    created_on = Column(DateTime(), default=func.now())
    updated_on = Column(DateTime(), default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<Repair(id={self.id}, cliente={self.cliente_id},{self.cliente})>"

