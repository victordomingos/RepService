#!/usr/bin/env python3
# encoding: utf-8
"""
Este módulo é parte integrante da aplicação RepService, desenvolvida por
Victor Domingos e distribuída sob os termos da licença Creative Commons
Attribution-ShareAlike 4.0 International (CC BY-SA 4.0).
"""
import os.path


# Alterar para True no caso de se tratar de uma máquina lenta (animações
# no entryframe)
SLOW_MACHINE = False

# Usar estilo 'aqua' para obter visual nativo no macOS. Noutras plataformas,
# pode ser necessário alterar para outro estilo. Alguns widgets ttk podem
# necessitar de alguns ajustes ao usar estilos diferentes.
ESTILO_APP = 'aqua'

# Alterar para False para utilizar uma ligação remota via web API.
USE_LOCAL_DATABASE = True

# Especificar aqui onde se encontra a base de dados.
if USE_LOCAL_DATABASE:
    LOCAL_DATABASE_PATH = os.path.expanduser('~/Dropbox/.__test_service.local_db')
else:
    REMOTE_API_URL = 'http://localhost:5000'


# --- Dimensões e posições predefinidas dos vários tipos de janelas ---

# Login
LOGIN_MIN_WIDTH = 440
LOGIN_MIN_HEIGHT = 190
LOGIN_MAX_WIDTH = 440
LOGIN_MAX_HEIGHT = 190

# Mudança de senha
CHPWD_MIN_WIDTH = 340
CHPWD_MIN_HEIGHT = 285
CHPWD_MAX_WIDTH = 440
CHPWD_MAX_HEIGHT = 320

# Janela principal - lista de reparações e mensagens
ROOT_GEOMETRIA = '1060x800+0+0'
MASTER_MIN_WIDTH = 970
MASTER_MIN_HEIGHT = 750
MASTER_MAX_WIDTH = 2000
MASTER_MAX_HEIGHT = 2000

# Janela da lista de contactos
CONTACTOS_GEOMETRIA = '430x730+1062+92'
CONTACTOS_MIN_WIDTH = 430
CONTACTOS_MIN_HEIGHT = 730
CONTACTOS_MAX_WIDTH = 600
CONTACTOS_MAX_HEIGHT = 2000

# Janela da lista de remessas
REMESSAS_GEOMETRIA = '430x730+1062+92'
REMESSAS_MIN_WIDTH = 430
REMESSAS_MIN_HEIGHT = 730
REMESSAS_MAX_WIDTH = 600
REMESSAS_MAX_HEIGHT = 2000

# Janelas de detalhes de reparação
W_DETALHE_REP_GEOMETRIA = '830x610'
W_DETALHE_REP_MIN_WIDTH = 768
W_DETALHE_REP_MIN_HEIGHT = 580
W_DETALHE_REP_MAX_WIDTH = 960
W_DETALHE_REP_MAX_HEIGHT = 2000

# Janelas de detalhes de remessa
W_DETALHE_REMESSA_GEOMETRIA = '780x600'
W_DETALHE_REMESSA_MIN_WIDTH = 600
W_DETALHE_REMESSA_MIN_HEIGHT = 450
W_DETALHE_REMESSA_MAX_WIDTH = 960
W_DETALHE_REMESSA_MAX_HEIGHT = 2000

# Janelas de detalhes de contacto
W_DETALHE_CONTACTO_GEOMETRIA = '490x551'
W_DETALHE_CONTACTO_MIN_WIDTH = 490
W_DETALHE_CONTACTO_MIN_HEIGHT = 551
W_DETALHE_CONTACTO_MAX_WIDTH = 900
W_DETALHE_CONTACTO_MAX_HEIGHT = 760

# Janelas de detalhes de mensagem/evento
W_DETALHE_MSG_GEOMETRIA = '420x280'
W_DETALHE_MSG_MIN_WIDTH = 420
W_DETALHE_MSG_MIN_HEIGHT = 280
W_DETALHE_MSG_MAX_WIDTH = 500
W_DETALHE_MSG_MAX_HEIGHT = 480
