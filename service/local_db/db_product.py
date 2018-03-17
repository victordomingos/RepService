#!/usr/bin/env python3
# encoding: utf-8
"""
Este módulo é parte integrante da aplicação Promais Service, desenvolvida por
Victor Domingos e distribuída sob os termos da licença Creative Commons
Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)
"""
import os

from sqlalchemy import create_engine, or_, and_
from sqlalchemy.orm import sessionmaker, load_only
from typing import Dict, Tuple, List, Union, Optional, Any

from passlib.hash import pbkdf2_sha256

from local_db import db_models
from misc.misc_funcs import calcular_dias_desde
from global_setup import LOCAL_DATABASE_PATH
from misc.constants import ESTADOS, PRIORIDADES


class DBProduct(object):
    def obter_artigo(self, session, part_number: str):
        return {'id': 1,
                'descr': "This is the description for this product",
                'part_number': "ZD123"}
