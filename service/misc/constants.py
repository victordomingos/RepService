#!/usr/bin/env python3
# encoding: utf-8
"""
Este módulo é parte integrante da aplicação Promais Service, desenvolvida por
Victor Domingos e distribuída sob os termos da licença Creative Commons
Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)
"""

import os
import os.path

APP_NAME = "RepService 2018"
__author__ = "Victor Domingos"
__copyright__ = "Copyright 2018 Victor Domingos"
APP_LICENSE = "Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)"
APP_VERSION = "v0.20 development"
__email__ = "web@victordomingos.com"
__status__ = "Development"


# Estados (como serão registados na base de dados)
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

PROCESSOS_FINALIZADOS = [ENTREGUE, ABANDONADO, ANULADO, SEM_INFORMACAO]
PROCESSOS_EM_CURSO = [EM_PROCESSAMENTO, AGUARDA_ENVIO, AGUARDA_RESP_FORNECEDOR,
                   AGUARDA_RESP_CLIENTE, AGUARDA_RECECAO, RECEBIDO,
                   DISPONIVEL_P_LEVANTAMENTO]

# Lista de estados (mesma sequência, para quando precisamos de uma string)
ESTADOS = {0: "Em processamento",
           1: "A aguardar envio",
           2: "Aguarda resposta do fornecedor",
           3: "Aguarda resposta do cliente",
           4: "A aguardar receção",
           5: "Recebido - avisar cliente",
           6: "Disponível p/ levantamento",
           7: "Entregue",
           8: "Abandonado",
           9: "Anulado",
           10: "Sem informação"
           }

# Resultados de eventos (como serão registados na base de dados)
EV_SEM_INFORMACAO = 0
EV_GARANTIA_APROVADA_REPARADO = 1
EV_GARANTIA_APROVADA_SUBSTITUIDO = 2
EV_GARANTIA_APROVADA_NOTA_DE_CREDITO = 3
EV_GARANTIA_RECUSADA = 4
EV_ORCAMENTO_ACEITE = 5
EV_ORCAMENTO_RECUSADO = 6
EV_INTERVENCAO_IMPOSSIVEL = 7

# Lista de resultados (mesma sequência, para quando precisamos de uma string)
RESULTADOS = {0: "Sem informação",
              1: "Garantia aprovada - artigo reparado",
              2: "Garantia aprovada - artigo substituído",
              3: "Garantia aprovada - emitida nota de crédito",
              4: "Garantia recusada",
              5: "Orçamento aceite",
              6: "Orçamento recusado",
              7: "Intervenção impossível"}


# Modos de entrega (como serão registados na base de dados)
LEVANTAMENTO = 0
ENVIAR_MORADA_FICHA = 1
ENVIAR_NOVA_MORADA = 2

# Lista de modos de entrega (mesma sequência, para quando precisamos de uma string)
MODOS_ENTREGA = {0: "Levantamento nas n/ instalações",
                 1: "Enviar para a morada da ficha de cliente",
                 2: "Enviar para outra morada..."}


PRIORIDADES = {0: "Normal", 1: "Alta", 2: "Urgente"}


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
os.chdir("../")
APP_PATH = os.getcwd()
ICON_PATH = APP_PATH + "/images/icons/"


TODOS_OS_PAISES = ("Angola", "Alemanha", "Afeganistão", "África do Sul",
                   "Albânia", "Andorra", "Anguilla", "Antártida", "Antígua & Barbuda",
                   "Arábia Saudita", "Argélia", "Argentina", "Arménia", "Aruba", "Austrália",
                   "Áustria", "Azerbaijão", "Brasil", "Bélgica", "Bahamas", "Bahrein",
                   "Bangladesh", "Barbados", "Bielorrússia", "Belize", "Benin", "Bermudas",
                   "Bolívia", "Bonaire, St. Eustatius & Saba", "Bósnia-Herzegovina",
                   "Botsuana", "Brunei", "Bulgária", "Burkina Faso", "Burundi", "Butão",
                   "Cabo Verde", "Camarões", "Camboja", "Canadá", "Cazaquistão", "Chade",
                   "Chile", "China", "Chipre", "Colômbia", "Congo", "Coreia do Norte",
                   "Coreia do Sul", "Costa do Marfim", "Costa Rica", "Croácia", "Cuba",
                   "Curaçao", "Dinamarca", "Djibuti", "Dominica", "Espanha", "Estados Unidos",
                   "Egito", "El Salvador", "Emirados Árabes Unidos", "Equador", "Eritréia",
                   "Eslováquia", "Eslovénia", "Estónia", "Etiópia", "França",
                   "Federação Russa", "Fiji", "Filipinas", "Finlândia", "Gabão", "Gâmbia",
                   "Gana", "Geórgia", "Gibraltar", "Granada", "Grécia", "Gronelândia",
                   "Guadalupe", "Guam (Território dos Estados Unidos)", "Guatemala",
                   "Guernsey", "Guiana", "Guiana Francesa", "Guiné", "Guiné Equatorial",
                   "Guiné-Bissau", "Haiti", "Holanda", "Honduras", "Hong-Kong", "Hungria",
                   "Iémen", "Ilha Bouvet (Território da Noruega)", "Ilha do Homem",
                   "Ilha Natal", "Ilha Pitcairn", "Ilha Reunião", "Ilhas Aland",
                   "Ilhas Cayman", "Ilhas Cocos", "Ilhas Comores", "Ilhas Cook",
                   "Ilhas Faroes", "Ilhas Falkland (Malvinas)",
                   "Ilhas Geórgia do Sul e Sandwich do Sul",
                   "Ilhas Heard e McDonald (Território da Austrália)",
                   "Ilhas Marianas do Norte", "Ilhas Marshall",
                   "Ilhas Menores dos Estados Unidos", "Ilhas Norfolk", "Ilhas Seychelles",
                   "Ilhas Solomão", "Ilhas Svalbard & Jan Mayen", "Ilhas Tokelau",
                   "Ilhas Turks e Caicos", "Ilhas Virgens (Estados Unidos)",
                   "Ilhas Virgens (Inglaterra)", "Ilhas Wallis & Futuna", "Índia",
                   "Indonésia", "Irão", "Iraque", "Irlanda", "Islândia", "Israel", "Itália",
                   "Jamaica", "Japão", "Jersey", "Jordânia", "Kiribati", "Kuait",
                   "Luxemburgo", "Laos", "Letónia", "Lesoto", "Líbano", "Libéria", "Líbia",
                   "Liechtenstein", "Lituânia", "Macau", "Macedónia (República Jugoslava)",
                   "Madagascar", "Malásia", "Malaui", "Maldivas", "Mali", "Malta", "Marrocos",
                   "Martinica", "Maurício", "Mauritânia", "Mayotte", "México", "Micronésia",
                   "Moçambique", "Moldova", "Mónaco", "Mongólia", "Montenegro", "Montserrat",
                   "Birmânia (Myanmar)", "Namíbia", "Nauru", "Nepal", "Nicarágua", "Níger",
                   "Nigéria", "Niue", "Noruega", "Nova Caledónia", "Nova Zelândia", "Omã",
                   "Portugal", "Palau", "Panamá", "Papua-Nova Guiné", "Paquistão", "Paraguai",
                   "Peru", "Polinésia Francesa", "Polónia", "Porto Rico", "Qatar", "Quénia",
                   "Quirguistão", "Reino Unido", "República Centro-Africana",
                   "República Democrática do Congo", "República Dominicana",
                   "República Checa", "Roménia", "Ruanda", "Saara Ocidental",
                   "Saint Vincent e Granadinas", "Samoa Ocidental", "San Marino",
                   "Santa Helena", "Santa Lúcia", "São Bartolomeu", "São Cristóvão e Névis",
                   "San Martin", "São Tomé e Príncipe", "Senegal", "Serra Leoa", "Sérvia",
                   "Singapura", "Síria", "Somália", "Sri Lanka", "St. Maarten",
                   "St.Pierre & Miquelon", "Suazilândia", "Sudão", "Sudão do Sul", "Suécia",
                   "Suíça", "Suriname", "Tadjiquistão", "Tailândia", "Taiwan", "Tanzânia",
                   "Território Britânico do Oceano Índico", "Territórios do Sul da França",
                   "Territórios Palestinos Ocupados", "Timor Leste", "Togo", "Tonga",
                   "Trinidad & Tobago", "Tunísia", "Turquemenistão", "Turquia", "Tuvalu",
                   "Ucrânia", "Uganda", "Uruguai", "Uzbequistão", "Vanuatu", "Vaticano",
                   "Venezuela", "Vietname", "Zâmbia", "Zimbábue")


CREDITS = ("António Cascalheira", "Bjorn Pettersen", "Brian Oakley",
           "Jackjr300", "Jannick", "Jay Loden", "Juliette Monsel", "Márcio Araújo", "Nelson Brochado",
           "Pat Thoyts", "Patrick Seemann", "Ruocheng Wang")
