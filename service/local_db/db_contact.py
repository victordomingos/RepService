from typing import Dict, List, Union, Optional, Any

from sqlalchemy import or_, and_
from sqlalchemy.orm import load_only

from local_db import db_models


class DBContact(object):

    @staticmethod
    def save_contact(session, contact: Union[str, int, Any]) -> Union[int, bool]:
        try:
            new_contact = db_models.Contact(**contact)
            session.add(new_contact)
            session.commit()
            return new_contact.id
        except Exception as e:
            print("Não foi possível guardar o contacto:", e)
            return False


    @staticmethod
    def update_contact(session, contact) -> bool:
        try:
            db_contact = session.query(db_models.Contact).get(contact['id'])

            db_contact.nome = contact['nome']
            db_contact.empresa = contact['empresa']
            db_contact.telefone = contact['telefone']
            db_contact.telemovel = contact['telemovel']
            db_contact.telefone_empresa = contact['telefone_empresa']
            db_contact.email = contact['email']
            db_contact.morada = contact['morada']
            db_contact.cod_postal = contact['cod_postal']
            db_contact.localidade = contact['localidade']
            db_contact.pais = contact['pais']
            db_contact.nif = contact['nif']
            db_contact.notas = contact['notas']
            db_contact.is_cliente = contact['is_cliente']
            db_contact.is_fornecedor = contact['is_fornecedor']
            db_contact.ult_atualizacao_por_utilizador_id = contact['atualizado_por_utilizador_id']
            return True
        except Exception as e:
            print("Não foi possível atualizar o contacto:", e)
            return False


    @staticmethod
    def count_contacts(session) -> int:
        return session.query(db_models.Contact).count()


    @staticmethod
    def search_contacts(session, txt_pesquisa: str = "", tipo: str = "Clientes"):
        termo_pesquisa = txt_pesquisa

        numeric = False
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

        # TODO: restringir a pesquisa aos registos que tenham o estado selecionado

        if tipo == "Clientes":
            contactos = session.query(db_models.Contact).filter(
                and_(db_models.Contact.is_cliente.is_(True),
                     or_(
                         db_models.Contact.id.like(termo_pesquisa + "%"),
                         db_models.Contact.nome.ilike(termo_pesquisa),
                         db_models.Contact.telefone.ilike(termo_pesquisa + "%"),
                         db_models.Contact.telemovel.ilike(termo_pesquisa + "%"),
                         db_models.Contact.email.ilike(termo_pesquisa),
                         db_models.Contact.nif.like(termo_pesquisa + "%"),
                     )))
        else:
            contactos = session.query(db_models.Contact).filter(
                and_(db_models.Contact.is_fornecedor.is_(True),
                     or_(
                         db_models.Contact.id.like(termo_pesquisa + "%"),
                         db_models.Contact.nome.ilike(termo_pesquisa),
                         db_models.Contact.telefone.ilike(termo_pesquisa + "%"),
                         db_models.Contact.telemovel.ilike(termo_pesquisa + "%"),
                         db_models.Contact.email.ilike(termo_pesquisa),
                         db_models.Contact.nif.like(termo_pesquisa + "%"),
                     )))

        return [{'id': contact.id,
                 'nome': contact.nome,
                 'telefone': contact.telefone,
                 'email': contact.email}
                for contact in contactos]


    @staticmethod
    def get_contact(session, num_contacto: int) -> Dict[str, Union[int, str]]:
        contacto = session.query(db_models.Contact).get(num_contacto)

        if contacto.atualizado_por_utilizador:
            atualizado_por_utilizador_nome = contacto.atualizado_por_utilizador.nome
        else:
            atualizado_por_utilizador_nome = None

        return {
            'id': contacto.id,
            'nome': contacto.nome,
            'empresa': contacto.empresa,
            'telefone': contacto.telefone,
            'telemovel': contacto.telemovel,
            'telefone_empresa': contacto.telefone_empresa,
            'email': contacto.email,
            'morada': contacto.morada,
            'cod_postal': contacto.cod_postal,
            'localidade': contacto.localidade,
            'pais': contacto.pais,
            'nif': contacto.nif,
            'notas': contacto.notas,
            'is_cliente': contacto.is_cliente,
            'is_fornecedor': contacto.is_fornecedor,
            'criado_por_utilizador_id': contacto.criado_por_utilizador_id,
            'ult_atualizacao_por_utilizador_id': contacto.ult_atualizacao_por_utilizador_id,
            'created_on': contacto.created_on.isoformat(sep=' ', timespec='minutes'),
            'updated_on': contacto.updated_on.isoformat(sep=' ', timespec='minutes'),
            'criado_por_utilizador_nome': contacto.criado_por_utilizador.nome,
            'atualizado_por_utilizador_nome': atualizado_por_utilizador_nome}


    @staticmethod
    def get_contact_info(session, num_contacto: int, tipo: str) -> Optional[
        Dict[str, Union[str, Any]]]:
        """ Obter informação resumida de um contacto, para utilização no
            formulário de nova reparação. Caso não exista na base de dados um
            contacto que corresponda aos dados introduzidos (cliente ou fornecedor
            com o número indicado), a função devolve None.
        """
        contacto = session.query(db_models.Contact).get(num_contacto)

        if not contacto:
            return None

        if tipo == "Fornecedor":
            if not contacto.is_fornecedor:
                return None
        elif tipo == "Cliente":
            if not contacto.is_cliente:
                return None
        else:
            print("Tipo de contacto desconhecido:", tipo)
            return None

        if contacto.telefone:
            telefone = contacto.telefone
        elif contacto.telemovel:
            telefone = contacto.telemovel
        elif contacto.telefone_empresa:
            telefone = contacto.telefone_empresa + " (Empresa)"
        else:
            telefone = "N/D"
        return {
            'id': contacto.id,
            'nome': contacto.nome,
            'telefone': telefone,
            'email': contacto.email
        }


    @staticmethod
    def contact_exists(session, nif: int) -> Optional[Dict[str, Union[str, Any]]]:
        """ Verifica se já existe na base de dados algum contacto com o NIF indicado
                e, caso exista, obtém o ID e nome respetivos. Caso não exista, a função
                devolve None.
            """
        contacto = session.query(db_models.Contact.id, db_models.Contact.nome) \
            .filter(db_models.Contact.nif == nif).first()

        if contacto:
            return {
                'id': contacto.id,
                'nome': contacto.nome,
            }
        else:
            return None


    @staticmethod
    def get_costumers(session) -> List[Dict[str, Union[int, str]]]:
        contactos = session.query(db_models.Contact).filter_by(is_cliente=True)
        return [{'id': contact.id,
                 'nome': contact.nome,
                 'telefone': contact.telefone,
                 'email': contact.email}
                for contact in contactos]


    @staticmethod
    def get_suppliers(session) -> List[Dict[str, Union[int, str]]]:
        contactos = session.query(db_models.Contact).filter_by(is_fornecedor=True) \
            .options(load_only("id", "nome", "telefone", "email"))
        return [{'id': contact.id,
                 'nome': contact.nome,
                 'telefone': contact.telefone,
                 'email': contact.email}
                for contact in contactos]


    @staticmethod
    def get_suppliers_list(session) -> List[Dict[str, Union[int, str]]]:
        """ Obter lista simplificada de fornecedores e/ou centros técnicos.
        """
        contactos = session.query(db_models.Contact).filter_by(is_fornecedor=True) \
            .options(load_only("id", "nome"))

        return [{'id': contact.id,
                 'nome': contact.nome}
                for contact in contactos]
