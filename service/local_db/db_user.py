#!/usr/bin/env python3
# encoding: utf-8
"""
Este módulo é parte integrante da aplicação Promais Service, desenvolvida por
Victor Domingos e distribuída sob os termos da licença Creative Commons
Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)
"""
from typing import Tuple, Union

from passlib.hash import pbkdf2_sha256

from local_db import db_models


class DBUser(object):

    @staticmethod
    def validate_login(session, username: str, password: str) -> Tuple[bool, str]:
        """ Check if username and password match the info in database. Token stuff
            is provided here only to ensure code compatibility for future web API
            access.
        """
        try:
            user = session.query(db_models.User.id, db_models.User.password) \
                .filter(db_models.User.nome == username).one()

            if pbkdf2_sha256.verify(password, user.password):
                loggedin = True
                token = "The amazing NPK Token"
            else:
                loggedin = False
                token = None
        except:
            loggedin = False
            token = None
        return loggedin, token


    @staticmethod
    def get_user_id(session, username: str) -> Union[int, bool]:
        """ Return the user ID from database, queried with a string containing the
            username.
        """
        try:
            utilizador = session.query(db_models.User.id).filter(
                db_models.User.nome == username).one()
            return utilizador.id
        except:
            return False


    def create_user(self, session, username: str, email: str, password: str, loja_id: int) -> bool:
        # começa por verificar se já existe utilizador com o nome indicado
        if self.get_user_id(session, username):
            return False

        try:
            utilizador = db_models.User(nome=username, email=email,
                                        password=password, loja_id=loja_id)
            session.add(utilizador)
            return True
        except Exception as e:
            print("An exception was found while trying to create new user:", e)
            return False


    def change_password(self, session, username: str, old_password: str, new_password: str) -> bool:
        """ Change the password for the given user if the old password matches.
            Returns False if it fails for some reason.
        """
        if self.validate_login(session, username, old_password):
            try:
                utilizador = session.query(db_models.User).filter(
                    db_models.User.nome == username).one()
                utilizador.password = pbkdf2_sha256.using(salt_size=8).hash(new_password)
                return True
            except Exception as e:
                print(e)
                return False
        else:
            return False
