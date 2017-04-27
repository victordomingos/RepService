#!/usr/bin/env python3.6
# encoding: utf-8

import os.path


MASTER_MIN_WIDTH = 970
MASTER_MIN_HEIGTH = 750
MASTER_MAX_WIDTH = 1366
MASTER_MAX_HEIGTH = 2000

CONTACTOS_MIN_WIDTH = 430
CONTACTOS_MIN_HEIGTH = 730
CONTACTOS_MAX_WIDTH = 600
CONTACTOS_MAX_HEIGTH = 2000

REMESSAS_MIN_WIDTH = 430
REMESSAS_MIN_HEIGTH = 730
REMESSAS_MAX_WIDTH = 600
REMESSAS_MAX_HEIGTH = 2000

WROOT_GEOMETRIA = '1060x800+0+0'
WCONTACTOS_GEOMETRIA = '430x730+1062+92'
WREMESSAS_GEOMETRIA = '430x730+1062+92'
WREPDETALHE_GEOMETRIA = '900x600+80+130'

SLOW_MACHINE = False # Alterar para True no caso de se tratar de uma máquina lenta (animações no entryframe)

#Estados (como serão registados na base de dados)
EM_PROCESSAMENTO = 0
AGUARDA_ENVIO = 1
AGUARDA_RESP_FORNECEDOR = 2
AGUARDA_RESP_CLIENTE = 3
AGUARDA_RECECAO = 4
RECEBIDO = 5
DISPONIVEL_P_LEVANTAMENTO = 6
ENTREGUE = 7
ABANDONADO = 8
ANULADO = 9
SEM_INFORMACAO = 10

#Lista de estados (mesma sequência, para quando precisamos de uma string)
ESTADOS = ("Em processamento",
           "A aguardar envio",
           "Aguarda resposta do fornecedor",
           "Aguarda resposta do cliente",
           "A aguardar receção",
           "Recebido - avisar cliente",
           "Disponível p/ levantamento - avisado",
           "Entregue",
           "Abandonado",
           "Anulado",
           "Sem informação"
           )

EQUIP_MARCAS_USO = 0
EQUIP_BOM_ESTADO = 1
EQUIP_MARCAS_ACIDENTE = 2
EQUIP_FALTA_PECAS = 3

TIPO_REP_CLIENTE = 0
TIPO_REP_STOCK = 1

TIPO_REMESSA_ENVIO = 0
TIPO_REMESSA_RECECAO = 1

GARANTIA_NAO = 0
GARANTIA_NESTE = 1
GARANTIA_NOUTRO = 2

TIPO_CONTACTO_CLIENTE = 0
TIPO_CONTACTO_FORNECEDOR = 1
TIPO_CONTACTO_LOJA = 2


os.chdir(os.path.dirname(__file__))
APP_PATH = os.getcwd()
