import sys
import os
import base64
from datetime import datetime
from typing import Optional
from tkinter import messagebox
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.font

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
    if not txt.strip():
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


def validate_past_date(given_date: str):
    """ Ao sair de um campo de texto ttk.Entry referente a uma data, verifica
        se o texto introduzido é válido e corresponde a uma data passada. Se
        for válido, a função devolve o objeto datetime correspondente, caso
        função devolve False caso o texto não seja válido.
    """
    if not given_date:
        return False

    try:
        my_date = datetime.strptime(given_date, '%Y-%m-%d')
        if my_date > datetime.now():
            raise ValueError('The date is in the future, not in the past as expected!')
        else:
            return my_date
    except Exception as e:
        msg = 'Por favor, escreva a data no formato correto (AAAA-MM-DD).'
        messagebox.showwarning(message=msg, parent=master)
        print("Data validation exception (date string:", dt, "\n", e)
        return False


def obfuscate_text(text: str) -> str:
    """ Create a simple (insecure) obfuscated string """
    return base64.b64encode(text.encode('utf-8'))


def reveal_text(text: str) -> str:
    """ Reveal the content of an obfuscated string """
    return base64.b64decode(text).decode('utf-8')


def clean_data(data: dict) -> dict:
    """ Return a copy of a dictionary, replacing None values by empty strings,
    and datetime objects by properly formatted date strings. """
    print(data)
    clean_dataset = {}
    for key, value in data.items():
        print(key, "-", value)
        if value is None:
            value = ''
        elif type(value) is datetime:
            value = value.isoformat(sep=' ', timespec='minutes')
        clean_dataset[key] = value
    return clean_dataset