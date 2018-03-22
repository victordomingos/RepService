from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship, backref

from local_db.db_base import Base


class Loja(Base):
    __tablename__ = 'loja'
    id = Column(Integer, primary_key=True)
    nome = Column(String)

    def __repr__(self):
        return f"<Loja(id={self.id}, Nome='{self.nome}')>"


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    loja_id = Column(Integer, ForeignKey('loja.id'))
    pwd_last_changed = Column(DateTime(), default=func.now())

    created_on = Column(DateTime(), default=func.now())
    updated_on = Column(DateTime(), default=func.now(), onupdate=func.now())

    loja = relationship(Loja, backref=backref('users', uselist=True))
    eventos = relationship("UtilizadorNotificadoPorEvento_link", back_populates="user")

    def __repr__(self):
        return f"<User(id={self.id}, name='{self.nome}', email='{self.email}', password='{self.password}', loja={self.loja})>"


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
    criado_por_utilizador_id = Column(Integer, ForeignKey('user.id'))
    ult_atualizacao_por_utilizador_id = Column(Integer, ForeignKey('user.id'))

    created_on = Column(DateTime(), default=func.now())
    updated_on = Column(DateTime(), default=func.now(), onupdate=func.now())

    criado_por_utilizador = relationship("User", foreign_keys=[criado_por_utilizador_id])
    atualizado_por_utilizador = relationship("User", foreign_keys=[ult_atualizacao_por_utilizador_id])

    def __repr__(self):
        return f"<Contact(id={self.id}, name='{self.nome}', empresa='{self.empresa}', is_cliente='{self.is_cliente}', is_fornecedor='{self.is_fornecedor}'>"

"""
class Product(Base):
    __tablename__ = 'product'

    id = Column(Integer, primary_key=True)
    descr_product = Column(String, nullable=False)
    part_number = Column(String)

    def __repr__(self):
        return f"<Article(id={self.id}, descr_product='{self.descr_product}', P/N='{self.part_number}'>"
"""

class Repair(Base):
    __tablename__ = 'repair'

    id = Column(Integer, primary_key=True, autoincrement=True)
    cliente_id = Column(Integer, ForeignKey('contact.id'))
    # product_id = Column(Integer, ForeignKey('product.id'))
    # Replaced by the following two lines. Opting for bit less normalization for now.
    descr_product = Column(String, nullable=False)
    part_number = Column(String)
    sn = Column(String)
    fornecedor_id = Column(Integer, ForeignKey('contact.id'))
    estado_artigo = Column(Integer)
    obs_estado = Column(String)
    is_garantia = Column(Integer)
    data_compra = Column(Date)
    num_fatura = Column(String)
    loja_compra = Column(String)
    descr_servico = Column(String)
    avaria_reprod_loja = Column(Boolean)
    requer_copia_seg = Column(Integer)
    is_find_my_ativo = Column(Integer)
    senha = Column(String)
    acessorios_entregues = Column(String)
    notas = Column(String)
    local_reparacao_id = Column(Integer, ForeignKey('contact.id'))
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
    data_entrega = Column(DateTime())
    num_quebra_stock = Column(String)
    is_stock = Column(Boolean)
    modo_entrega = Column(Integer)
    cliente_pagou_portes = Column(Integer)
    reincidencia_processo_id = Column(Integer)
    morada_entrega = Column(String)
    prioridade = 1
    criado_por_utilizador_id = Column(Integer, ForeignKey('user.id'))
    ult_atualizacao_por_utilizador_id = Column(Integer, ForeignKey('user.id'))

    created_on = Column(DateTime(), default=func.now())
    updated_on = Column(DateTime(), default=func.now(), onupdate=func.now())

    cliente = relationship("Contact", foreign_keys=[cliente_id],
        backref=backref("reparacoes_como_cliente", uselist=True, order_by=id))
    # product = relationship("Product", foreign_keys=[product_id],
    #     backref=backref("lista_reparacoes", uselist=True, order_by=id))
    fornecedor = relationship("Contact", foreign_keys=[fornecedor_id],
        backref=backref("reparacoes_como_fornecedor", uselist=True, order_by=id))
    local_reparacao = relationship("Contact", foreign_keys=[local_reparacao_id],
        backref=backref("reparacoes_como_local_reparacao", uselist=True, order_by=id))
    utilizador_entrega = relationship(User, foreign_keys=[utilizador_entrega_id])
    criado_por_utilizador = relationship("User", foreign_keys=[criado_por_utilizador_id])
    atualizado_por_utilizador = relationship(User, foreign_keys=[ult_atualizacao_por_utilizador_id])

    def __repr__(self):
        return f"<Repair(id={self.id}, cliente={self.cliente_id},{self.cliente})>"


class Event(Base):
    __tablename__ = 'event'

    id = Column(Integer, primary_key=True)
    repair_id = Column(Integer, ForeignKey('repair.id'))
    descricao = Column(String)
    criado_por_utilizador_id = Column(Integer, ForeignKey('user.id'))
    created_on = Column(DateTime(), default=func.now())
    updated_on = Column(DateTime(), default=func.now(), onupdate=func.now())

    repair = relationship("Repair", foreign_keys=[repair_id],
        backref=backref("eventos", uselist=True, order_by=id))
    criado_por_utilizador = relationship("User", foreign_keys=[criado_por_utilizador_id])
    utilizadores = relationship("UtilizadorNotificadoPorEvento_link", back_populates="event")

    def __repr__(self):
        return f"<Evento(id={self.id}, Reparação='{self.repair.id}', Descrição={self.descricao})>"


class UtilizadorNotificadoPorEvento_link(Base):
    __tablename__ = 'utilizador_notificado_por_evento_link'

    evento_id = Column(Integer, ForeignKey('event.id'), primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    is_visible = Column(Boolean)
    is_open = Column(Boolean)

    user = relationship("User", back_populates="eventos")
    event = relationship("Event", back_populates="utilizadores")

