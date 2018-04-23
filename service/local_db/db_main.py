""" Database public API with session scope context manager.

This module provides an API that is meant to be used by the GUI callbacks to
access all funtions related to database I/O. It implements a session scope as
context manager in order to allow multiple operations in a single session,
while automatically committing them and closing the session if the operation is
successful. The idea behind this apparently redundant approach is to make the
current API compatible with an eventual web API in the future, by keeping all
the database functions completely independent from the GUI code.

The functions available here should wrap the call to the database method in
the db_session_scope() context, include the context manager as the first
argument and then pass all the parameters. The value returned by the database
methods should be also returned back, without any manipulation.

    Example:

        from local_db.db_user import DBUser
        from typing import Tuple

        def validate_login(username: str, password: str) -> Tuple[bool, str]:
            with db_session_scope() as s
                return DBUser.validate_login(s, username, password)

The docstrings documenting these database operations will be located in their
respective modules.
"""
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import Dict, Tuple, List, Union, Optional, Any
from contextlib import contextmanager

from global_setup import LOCAL_DATABASE_PATH
from local_db.db_user import DBUser
from local_db.db_store import DBStore
from local_db.db_contact import DBContact
from local_db.db_event import DBEvent
#from local_db.db_product import DBProduct
from local_db.db_repair import DBRepair
from local_db.db_borrows import DBBorrow
from local_db.db_shipment import DBShipment


@contextmanager
def db_session_scope():
    """Provide a transactional scope around a series of operations."""
    engine = create_engine('sqlite+pysqlite:///' + os.path.expanduser(LOCAL_DATABASE_PATH))
    my_session_mkr = sessionmaker()
    my_session_mkr.configure(bind=engine)
    session = my_session_mkr()

    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


# ============================ LOGIN / Utilizadores ============================
def validate_login(username: str, password: str) -> Tuple[bool, str]:
    with db_session_scope() as s:
        return DBUser.validate_login(s, username, password)


def get_user_id(username: str) -> Union[int, bool]:
    with db_session_scope() as s:
        return DBUser.get_user_id(s, username)


def create_user(username: str, email: str, password: str, loja_id: int) -> bool:
    with db_session_scope() as s:
        return DBUser().create_user(s, username, email, password, loja_id)


def change_password(username: str, old_password: str, new_password: str) -> bool:
    with db_session_scope() as s:
        return DBUser().change_password(s, username, old_password, new_password)


# =============================== Lojas ===============================
def get_store_id(nome: str) -> int:
    with db_session_scope() as s:
        return DBStore.get_store_id(s, nome)


def create_store(nome: str) -> Union[int, bool]:
    with db_session_scope() as s:
        return DBStore().create_store(s, nome)

"""
# =============================== Produtos ===============================
def obter_artigo(part_number: str):
    with db_session_scope() as s:
        return DBProduct().obter_artigo(s, part_number)
"""

# =============================== Reparações ===============================
def save_repair(repair) -> int:
    with db_session_scope() as s:
        return DBRepair().save_repair(s, repair)


def update_repair_status(rep_num: int, status: int):
    with db_session_scope() as s:
        return DBRepair().update_repair_status(s, rep_num, status)


def update_repair_priority(rep_num: int, priority: int):
    with db_session_scope() as s:
        return DBRepair().update_repair_priority(s, rep_num, priority)


def contar_reparacoes() -> int:
    with db_session_scope() as s:
        return DBRepair.count_repairs(s)


def obter_todas_reparacoes() -> List[Dict[str, Union[int, str]]]:
    with db_session_scope() as s:
        return DBRepair.get_all_repairs(s)


def obter_reparacoes_por_estados(status_list: List[int]) -> List[Dict[str, Union[int, str]]]:
    with db_session_scope() as s:
        return DBRepair.get_repairs_by_status(s, status_list)


def obter_reparacoes_por_contacto(contact_id: int) -> List[Dict[str, Union[int, str]]]:
    with db_session_scope() as s:
        return DBRepair.get_repairs_by_contact(s, contact_id)


def pesquisar_reparacoes(txt_pesquisa: str, estados: List[int]=None) -> List[Dict[str, Union[int, str]]]:
    with db_session_scope() as s:
        return DBRepair.search_repairs(s, txt_pesquisa, estados)


def obter_reparacao(num_rep: int) -> Dict[str, Union[int, str]]:
    with db_session_scope() as s:
        return DBRepair().get_repair(s, num_rep)

def obter_num_serie(num_rep: int) -> str:
    with db_session_scope() as s:
        return DBRepair().get_serial_number(s, num_rep)


# =============================== Mensagens/Eventos ===============================

def obter_mensagens(user_id: int) -> List[Dict[str, Union[int, str]]]:
    with db_session_scope() as s:
        return DBEvent.get_messages(s, user_id)


def obter_evento(event_id: int) -> Dict[str, Union[int, str]]:
    with db_session_scope() as s:
        return DBEvent.get_event(s, event_id)


# =============================== Contactos ===============================
def save_contact(contact: Union[str, int, Any]) -> Union[int, bool]:
    with db_session_scope() as s:
        cont_id = DBContact.save_contact(s, contact)
        print("cont_id:", cont_id)
        return cont_id


def update_contact(contact) -> bool:
    with db_session_scope() as s:
        return DBContact.update_contact(s, contact)


def contar_contactos() -> int:
    with db_session_scope() as s:
        return DBContact.count_contacts(s)


def pesquisar_contactos(txt_pesquisa: str="", tipo: str ="Clientes"):
    with db_session_scope() as s:
        return DBContact.search_contacts(s, txt_pesquisa, tipo)


def obter_clientes() -> List[Dict[str, Union[int, str]]]:
    with db_session_scope() as s:
        return DBContact.get_costumers(s)


def obter_fornecedores() -> List[Dict[str, Union[int, str]]]:
    with db_session_scope() as s:
        return DBContact.get_suppliers(s)


def obter_lista_fornecedores() -> List[Dict[str, Union[int, str]]]:
    with db_session_scope() as s:
        return DBContact.get_suppliers_list(s)


def obter_contacto(num_contacto: int) -> Dict[str, Union[int, str]]:
    with db_session_scope() as s:
        return DBContact.get_contact(s, num_contacto)


def obter_info_contacto(num_contacto: int, tipo:str) -> Optional[Dict[str, Union[str, Any]]]:
    with db_session_scope() as s:
        return DBContact.get_contact_info(s, num_contacto, tipo)


def contact_exists(nif: int) -> Optional[Dict[str, Union[str, Any]]]:
    with db_session_scope() as s:
        return DBContact.contact_exists(s, nif)


def validar_fornecedor(num_contacto: int): -> bool
    with db_session_scope() as s:
        return DBContact.is_supplier(s, num_contacto)


def validar_cliente(num_contacto: int): -> bool
    with db_session_scope() as s:
        return DBContact.is_costumer(s, num_contacto)

# =============================== Remessas ===============================
def save_remessa(remessa: int) -> int:
    with db_session_scope() as s:
        return DBShipment().save_shipment(s, remessa)


def obter_lista_processos_por_receber():
    with db_session_scope() as s:
        return DBShipment().save_shipment(s)


def obter_lista_processos_por_enviar():
    with db_session_scope() as s:
        return DBShipment().save_shipment(s)


def contar_remessas() -> int:
    with db_session_scope() as s:
        return DBShipment.count_shipments(s)


# =============================== Empréstimos ===============================

def obter_lista_artigos_emprest() -> Dict[str, Tuple[str, str]]:
    with db_session_scope() as s:
        return DBBorrow().get_products_to_borrow_list(s)


# =============================== Orçamentos ===============================


# =============================== Comunicação ===============================
