#!/usr/bin/env python3
# encoding: utf-8
"""
Este módulo é parte integrante da aplicação Promais Service, desenvolvida por
Victor Domingos e distribuída sob os termos da licença Creative Commons
Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)
"""
import sys
import os
from datetime import datetime
from typing import Optional


def calcular_dias_desde(data: datetime) -> int:
    """ Calcular número de dias que passaram desde data indicada.
        Ex: calcular_dias_desde(data)
        Nota: Requer data no formato datetime.today()
    """
    hoje = datetime.today()
    diferenca = hoje - data
    return diferenca.days   # nº de dias que já passaram

def txt_para_data(txt: str) -> Optional[datetime]:
    """ Converte uma string contendo uma data do tipo 2013-08-13 (obtida por
        exemplo através do tkcalendar/DatePicker) num objeto do tipo datetime.
    """
    if not str.strip:
        return None
    return datetime.strptime(txt, '%Y-%m-%d')


def restart_program():
    """Restarts the current program.
    Note: this function does not return. Any cleanup action (like
    saving data) must be done before calling this function."""
    python = sys.executable
    os.execl(python, python, * sys.argv)
