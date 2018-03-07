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
from tkinter import messagebox


from global_setup import DEFAULT_PHONE_REGION

from phonenumbers import parse, is_valid_number, normalize_diallable_chars_only
from phonenumbers import format_out_of_country_keeping_alpha_chars


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


def check_and_normalize_phone_number(number: str) -> Optional[str]:
    """ Verifica se o número indicado é ser um número de telefone válido. Se
        estiver num formato válido, a função devolve uma versão normalizada
        desse número de telefone. Caso contrário, devolve None.
    """
    if not number:
        return None

    try:
        # Tenta normalizar pressupondo a presença do indicativo internacional
        number = normalize_diallable_chars_only(number)
        n = parse(number)
    except Exception as e:
        try:
            # Tenta normalizar com o indicativo do país pré-definido
            n = parse(number, DEFAULT_PHONE_REGION)
        except:
            return None

    if is_valid_number(n):
        normalized_number = format_out_of_country_keeping_alpha_chars(n,
                    region_calling_from=DEFAULT_PHONE_REGION)
        return normalized_number
    else:
        return None


def validate_phone_entry(master, widget):
    """ Ao sair de um campo de texto ttk.Entry referente a número de telefone,
        tenta verificar se o nº introduzido é válido e formata-o de forma mais
        legível.
    """
    number = widget.get()

    if not number:
        return

    telefone = check_and_normalize_phone_number(number)
    if telefone:
        widget.delete(0, 'end')
        widget.insert(0, telefone)
    else:
        msg = 'Por favor, escreva o número de telefone no formato correto.'
        messagebox.showwarning(message=msg, parent=master)
