#!/usr/bin/env python3
# encoding: utf-8
"""
Este módulo é parte integrante da aplicação Promais Service, desenvolvida por
Victor Domingos e distribuída sob os termos da licença Creative Commons
Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)
"""

from typing import Union

from local_db import db_models


class DBStore(object):

    @staticmethod
    def get_store_id(session, nome: str) -> int:
        """ Return the store ID from database, queried with a string containing the
            store name.
        """
        store = session.query(db_models.Loja.id).filter(db_models.Loja.nome == nome).one()
        return store.id


    def create_store(self, session, nome: str) -> Union[int, bool]:
        # verificar primeiro se já existe loja com o nome indicado...
        try:
            store_id = self.get_store_id(session, nome)
            print(f"A store already exists with the specified name (ID: {store_id}).")
            return False
        except:
            pass

        try:
            store = db_models.Loja(nome=nome)
            session.add(store)
            return store.id
        except Exception as e:
            print("An exception was found while trying to create new store:", e)
            return False
