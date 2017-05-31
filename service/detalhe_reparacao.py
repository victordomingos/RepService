#!/usr/bin/env python3.6
# encoding: utf-8
"""
Este módulo é parte integrante da aplicação RepService, desenvolvida por
Victor Domingos e distribuída sob os termos da licença Creative Commons
Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)
"""

import tkinter as tk
from tkinter import ttk
import Pmw
from global_setup import *
from extra_tk_classes import *


class repairDetailWindow(ttk.Frame):
    """ Classe de base para a janela de detalhes de reparações """
    def __init__(self, master, num_reparacao, *args,**kwargs):
        super().__init__(master,*args,**kwargs)
        self.master = master
        self.num_reparacao = num_reparacao
        self.tipo_processo = "Cliente" if bool((self.num_reparacao%2)==0) else "Stock"  #TODO: Substituir isto por função que busca tipo na info da base de dados

        self.is_rep_cliente = (self.tipo_processo == "Cliente")  # i.e. True se for reparação de cliente
        self.estado = ESTADOS[EM_PROCESSAMENTO] #TODO: Obter estado a partir da base de dados

        self.is_garantia = True  # todo - verificar se é garantia
        self.modo_entrega = 2 # todo - obter da base de dados

        self.dicas = Pmw.Balloon(self.master, label_background='#f6f6f6', hull_highlightbackground='#b3b3b3')

        if self.is_rep_cliente:
            self.numero_contacto = "12345" #TODO numero de cliente
            self.nome = "Norberto Plutarco Keppler" #TODO Nome do cliente
            self.telefone = "+351 900 000 000" #TODO Telefone do cliente
            self.email = "repservice@the-NPK-programming-team.py" #TODO Email do cliente
        else:
            self.numero_contacto = "90000" #TODO numero de fornecedor
            self.nome = "That International Provider of Great Stuff, Inc." #TODO Nome do fornecedor
            self.telefone = "+351 200 000 000" #TODO Telefone do fornecedor
            self.email = "repservice@the-NPK-programming-team.py" #TODO Email do fornecedor


        self.configurar_frames_e_estilos()
        self.montar_barra_de_ferramentas()
        self.gerar_painel_principal()
        self.mostrar_painel_principal()

        self.montar_rodape()
        self.composeFrames()


    def montar_barra_de_ferramentas(self):
        self.lbl_titulo = ttk.Label(self.topframe, style="Panel_Title.TLabel", foreground=self.btnTxtColor, text=f"Reparação nº {self.num_reparacao}")

        # Reincidência apenas aparece se reparação está entregue, anulado, abandonado, sem_informacao
        if self.estado >= ESTADOS[ENTREGUE]:
            self.btn_reincidencia = ttk.Button(self.topframe, text="➕ Reincidência", width=4, command=None)
            self.dicas.bind(self.btn_reincidencia, 'Criar novo processo de reincidência\ncom base nesta reparação.')

        # Botão para registar entrega apenas aparece se reparação ainda não está entregue
        if self.estado != ESTADOS[ENTREGUE]:
            self.btn_entregar = ttk.Button(self.topframe, text=" ✅", width=4, command=None)
            self.dicas.bind(self.btn_entregar, 'Marcar esta reparação como entregue.')


        # ----------- Botão com menu "Alterar estado" --------------
        self.mbtn_alterar_estado = ttk.Menubutton(self.topframe, style="TMenubutton", text="Estado")
        self.mbtn_alterar_estado.menu = tk.Menu(self.mbtn_alterar_estado, tearoff=0)
        self.mbtn_alterar_estado["menu"] = self.mbtn_alterar_estado.menu

        self.mbtn_alterar_estado.menu.add_command(label=ESTADOS[EM_PROCESSAMENTO], command=None)
        self.mbtn_alterar_estado.menu.add_command(label=ESTADOS[AGUARDA_ENVIO], command=None)
        self.mbtn_alterar_estado.menu.add_command(label=ESTADOS[AGUARDA_RESP_FORNECEDOR], command=None)
        self.mbtn_alterar_estado.menu.add_command(label=ESTADOS[AGUARDA_RESP_CLIENTE], command=None)
        self.mbtn_alterar_estado.menu.add_command(label=ESTADOS[AGUARDA_RECECAO], command=None)
        self.mbtn_alterar_estado.menu.add_command(label=ESTADOS[RECEBIDO], command=None)
        self.mbtn_alterar_estado.menu.add_command(label=ESTADOS[DISPONIVEL_P_LEVANTAMENTO], command=None)
        self.mbtn_alterar_estado.menu.add_separator()
        self.mbtn_alterar_estado.menu.add_command(label=ESTADOS[ENTREGUE], command=None)
        self.mbtn_alterar_estado.menu.add_separator()
        self.mbtn_alterar_estado.menu.add_command(label=ESTADOS[ANULADO], command=None)
        self.mbtn_alterar_estado.menu.add_command(label=ESTADOS[ABANDONADO], command=None)
        self.mbtn_alterar_estado.menu.add_command(label=ESTADOS[SEM_INFORMACAO], command=None)
        self.dicas.bind(self.mbtn_alterar_estado, 'Alterar o estado deste processo de reparação.')
        # ----------- fim de Botão com menu "Alterar estado" -------------


        # ----------- Botão com menu "Alterar Prioridade" --------------
        self.mbtn_alterar_prioridade = ttk.Menubutton(self.topframe, text="Prioridade")
        self.mbtn_alterar_prioridade.menu = tk.Menu(self.mbtn_alterar_prioridade, tearoff=0)
        self.mbtn_alterar_prioridade["menu"] = self.mbtn_alterar_prioridade.menu

        self.mbtn_alterar_prioridade.menu.add_command(label="Baixa", command=None)
        self.mbtn_alterar_prioridade.menu.add_command(label="Normal", command=None)
        self.mbtn_alterar_prioridade.menu.add_command(label="Alta", command=None)
        self.mbtn_alterar_prioridade.menu.add_command(label="Urgente", command=None)
        self.dicas.bind(self.mbtn_alterar_prioridade, 'Alterar a prioridade deste processo de reparação.')
        # ----------- fim de Botão com menu "Alterar Prioridade" -------------


        # ----------- Botão com menu "Copiar" --------------
        self.mbtn_copiar = ttk.Menubutton(self.topframe, text=" ⚡")
        self.mbtn_copiar.menu = tk.Menu(self.mbtn_copiar, tearoff=0)
        self.mbtn_copiar["menu"] = self.mbtn_copiar.menu

        if self.is_rep_cliente:
            self.mbtn_copiar.menu.add_command(label="Nome", command=None)
            self.mbtn_copiar.menu.add_command(label="NIF", command=None)
            self.mbtn_copiar.menu.add_command(label="Morada", command=None)
            self.mbtn_copiar.menu.add_command(label="Código Postal", command=None)
            self.mbtn_copiar.menu.add_command(label="Localidade", command=None)
            if self.modo_entrega >= 1:
                self.mbtn_copiar.menu.add_separator()
                self.mbtn_copiar.menu.add_command(label="Morada para entrega", command=None)
                self.mbtn_copiar.menu.add_separator()

        self.mbtn_copiar.menu.add_command(label="Email", command=None)
        self.mbtn_copiar.menu.add_command(label="Telefone", command=None)
        self.mbtn_copiar.menu.add_separator()
        self.mbtn_copiar.menu.add_command(label="Descrição do equipamento", command=None)
        self.mbtn_copiar.menu.add_command(label="Número de série", command=None)
        self.dicas.bind(self.mbtn_copiar, 'Clique para selecionar e copiar\ndados referentes a este processo\npara a área de trânsferência.')
        # ----------- fim de Botão com menu "Copiar" -------------


        # ----------- Botão com menu "Imprimir" --------------
        self.mbtn_imprimir = ttk.Menubutton(self.topframe, text="Imprimir")
        self.mbtn_imprimir.menu = tk.Menu(self.mbtn_imprimir, tearoff=0)
        self.mbtn_imprimir["menu"] = self.mbtn_imprimir.menu

        self.mbtn_imprimir.menu.add_command(label="Guia de receção: loja e cliente", command=None)
        self.mbtn_imprimir.menu.add_command(label="Guia de receção: loja e serviço técnico", command=None)

        # TODO - Ocultar ou desativar estas opções se não houver um orçamento criado para esta reparação
        self.mbtn_imprimir.menu.add_separator()
        self.mbtn_imprimir.menu.add_command(label="Orçamento", command=None)
        self.mbtn_imprimir.menu.add_command(label="Recibo de pagamento: orçamento", command=None)

        # TODO - Ocultar ou desativar estas opções se não houver um empréstimo criado para esta reparação
        self.mbtn_imprimir.menu.add_separator()
        self.mbtn_imprimir.menu.add_command(label="Documento de empréstimo", command=None)
        self.mbtn_imprimir.menu.add_command(label="Recibo de pagamento: caução de empréstimo", command=None)
        self.dicas.bind(self.mbtn_imprimir, 'Clique para selecionar\no tipo de documento a imprimir.')
        # ----------- fim de Botão com menu "Imprimir" -------------

        self.btn_comunicacao = ttk.Button(self.topframe, text="✉️", width=4, command=None)
        self.dicas.bind(self.btn_comunicacao, 'Clique para selecionar\no tipo de comunicação a enviar e registar.')


        self.lbl_titulo.grid(column=0, row=0, rowspan=2)
        self.mbtn_alterar_estado.grid(column=4, row=0)
        self.mbtn_alterar_prioridade.grid(column=5, row=0)
        self.btn_comunicacao.grid(column=7, row=0)
        self.mbtn_copiar.grid(column=8, row=0)
        self.mbtn_imprimir.grid(column=9, row=0)

        # Reincidência apenas aparece se reparação está entregue, anulado, abandonado, sem_informacao
        if self.estado >= ESTADOS[ENTREGUE]:
            self.btn_reincidencia.grid(column=10, row=0)

        # Botão para registar entrega apenas aparece se reparação ainda não está entregue
        if self.estado != ESTADOS[ENTREGUE]:
            self.btn_entregar.grid(column=11, row=0)

        self.topframe.grid_columnconfigure(2, weight=1)


    def gerar_painel_principal(self):
        print(f"A mostrar detalhes da reparação nº {self.num_reparacao}")

        # Preparar o notebook da secção principal ------------------------
        self.note = ttk.Notebook(self.centerframe, padding="3 20 3 3")
        self.tab_geral = ttk.Frame(self.note, padding=10)
        self.tab_historico = ttk.Frame(self.note, padding=10)
        self.note.add(self.tab_geral, text="Geral")
        self.note.add(self.tab_historico, text="Histórico")
        self.gerar_tab_geral()
        self.montar_tab_geral()
        self.gerar_tab_historico()
        self.montar_tab_historico()

        if self.is_rep_cliente:
            self.tab_orcamentos = ttk.Frame(self.note, padding=10)
            self.tab_emprestimos = ttk.Frame(self.note, padding=10)
            self.note.add(self.tab_orcamentos, text="Orçamentos")
            self.note.add(self.tab_emprestimos, text="Empréstimos")
            self.gerar_tab_orcamentos()
            self.gerar_tab_emprestimos()
            self.montar_tab_orcamentos()
            self.montar_tab_emprestimos()

        self.desativar_campos()


    def gerar_tab_geral(self):
        # TAB Geral ~~~~~~~~~~~~~~~~
        self.geral_fr1 = ttk.Frame(self.tab_geral)
        self.geral_fr2 = ttk.Frame(self.tab_geral)

        # TODO - obter valor da base de dados
        # Criar widgets para este separador -------------------------------------------------------
        self.txt_numero_contacto = ttk.Entry(self.geral_fr1, font=("Helvetica-Neue", 12), width=5)
        self.btn_buscar_contacto = ttk.Button(self.geral_fr1, width=1, text="+", command=lambda *x: self.create_window_contacts(criar_novo_contacto="Cliente")) # TODO - abrir ficha de cliente
        self.txt_nome = ttk.Entry(self.geral_fr1, font=("Helvetica-Neue", 12), width=35)
        self.lbl_telefone = ttk.Label(self.geral_fr1, style="Panel_Body.TLabel", text=f"Tel.:{self.telefone}")
        self.lbl_email = ttk.Label(self.geral_fr1, style="Panel_Body.TLabel", text=f"Email:{self.email}")

        self.ltxt_descr_equipamento = LabelText(self.geral_fr2, "Descrição:", style="Panel_Body.TLabel", height=2, width=40)

        if self.is_rep_cliente:
            estado = f'Estado: {"Marcas de acidente"}'  # TODO: obter string do estado do equipamento
            self.ltxt_obs_estado_equipamento = LabelText(self.geral_fr2, estado, style="Panel_Body.TLabel", height=2)
            self.ltxt_local_intervencao = LabelEntry(self.geral_fr2, "Local da intervenção:", style="Panel_Body.TLabel", width=25)
            self.ltxt_acessorios = LabelText(self.geral_fr2, "Acessórios entregues:", style="Panel_Body.TLabel")
            if self.is_garantia:
                self.ltxt_data_compra = LabelEntry(self.geral_fr2, "Data de compra:", style="Panel_Body.TLabel", width=10)
                self.ltxt_num_fatura = LabelEntry(self.geral_fr2, "Nº da fatura:", style="Panel_Body.TLabel", width=15)
                self.ltxt_garantia = LabelEntry(self.geral_fr2, "Garantia em:", style="Panel_Body.TLabel")
            else:
                self.lbl_garantia = ttk.Label(self.geral_fr2, text="Garantia:\nFora de garantia", style="Panel_Body.TLabel")

        self.ltxt_cod_artigo = LabelEntry(self.geral_fr2, "Código de artigo:", style="Panel_Body.TLabel")
        self.ltxt_num_serie = LabelEntry(self.geral_fr2, "Nº de série:", style="Panel_Body.TLabel")

        self.ltxt_descr_avaria = LabelText(self.geral_fr2, "Avaria/Serviço:", style="Panel_Body.TLabel")
        self.ltxt_notas = LabelText(self.geral_fr2, "Notas:", style="Panel_Body.TLabel")

        if self.is_rep_cliente:
            self.ltxt_senha = LabelEntry(self.geral_fr2, "Senha:", style="Panel_Body.TLabel", width=22)
            varias_linhas = "• Avaria reproduzida na loja"
            varias_linhas += "\n• Find my iPhone ativo"
            varias_linhas += "\n• Efetuar cópia de segurança"

            if self.modo_entrega == 0:
                varias_linhas += "\n• Levantamento nas n/ instalações"
            elif self.modo_entrega == 1:
                varias_linhas += "\n• Enviar para a morada da ficha de cliente"
            else:
                varias_linhas += "\n• Enviar para a morada abaixo indicada"
                self.ltxt_morada_entrega = LabelText(self.geral_fr2, "Morada a utilizar na entrega:", style="Panel_Body.TLabel")

            self.lbl_varias_linhas = ttk.Label(self.geral_fr2, style="Panel_Body.TLabel", text=varias_linhas)

            """
            self.lbl_avaria_reprod_loja = ttk.Label(self.geral_fr2, style="Panel_Body.TLabel", text="- Avaria reproduzida na loja")
            self.lbl_find_my = ttk.Label(self.geral_fr2, style="Panel_Body.TLabel", text="- Find my iPhone ativo")
            self.lbl_efetuar_copia = ttk.Label(self.geral_fr2, style="Panel_Body.TLabel", text="- Efetuar cópia de segurança")
            if self.modo_entrega == 0:
                self.lbl_modo_entrega = ttk.Label(self.geral_fr2, style="Panel_Body.TLabel", text="- Levantamento nas n/ instalações")
            elif self.modo_entrega == 1:
                self.lbl_modo_entrega = ttk.Label(self.geral_fr2, style="Panel_Body.TLabel", text="- Enviar para a morada da ficha de cliente")
            else:
                self.lbl_modo_entrega = ttk.Label(self.geral_fr2, style="Panel_Body.TLabel", text="- Enviar para a morada abaixo indicada")
                self.ltxt_morada_entrega = LabelText(self.geral_fr2, "Morada a utilizar na entrega:", style="Panel_Body.TLabel")
            """
        else:
            self.ltxt_num_fatura_fornecedor = LabelEntry(self.geral_fr2, "Nº fatura fornecedor:", style="Panel_Body.TLabel", width=15)
            self.ltxt_data_fatura_fornecedor = LabelEntry(self.geral_fr2, "Data fatura fornecedor:", style="Panel_Body.TLabel", width=10)
            self.ltxt_nar = LabelEntry(self.geral_fr2, "NAR:", style="Panel_Body.TLabel", width=7)
            self.ltxt_num_guia_rececao = LabelEntry(self.geral_fr2, "Guia de receção:", style="Panel_Body.TLabel", width=6)
            self.ltxt_data_entrada_stock = LabelEntry(self.geral_fr2, "Data de entrada em stock:", style="Panel_Body.TLabel", width=15)
            self.ltxt_num_quebra_stock = LabelEntry(self.geral_fr2, "Nº de quebra de stock:", style="Panel_Body.TLabel", width=6)


        # Preencher com dados da base de dados -------------------------------------------------
        self.txt_numero_contacto.insert(0, self.numero_contacto)
        self.txt_nome.insert(0, self.nome)


        self.ltxt_descr_equipamento.set('Texto de exemplo para experimentar como sai na prática.\nIsto fica noutra linha...')
        if self.is_rep_cliente:
            self.ltxt_obs_estado_equipamento.set('Texto de exemplo para experimentar como sai na prática.\n Equipamento muito danificado!...')
            self.ltxt_local_intervencao.set('Aquele Tal Centro Técnico')
            self.ltxt_acessorios.set('Texto de exemplo para experimentar como sai na prática.\nIsto fica noutra linha...')
            self.ltxt_senha.set('12343112121')
            if self.is_garantia:
                self.ltxt_data_compra.set('29-07-2035')
                self.ltxt_num_fatura.set('FCR 1234567890/2035')
                self.ltxt_garantia.set('NPK International Online Store')
            if self.modo_entrega > 1:
                self.ltxt_morada_entrega.set("José manuel da silva fictício\nRua imaginária da conceição esplendorosa, nº 31, 3º andar frente\n1234-567 CIDADE MARAVILHOSA BRG\nPortugal")
        else:
            self.ltxt_num_fatura_fornecedor.set('C23918237323812371237/2017')
            self.ltxt_data_fatura_fornecedor.set('01-04-1974')
            self.ltxt_num_guia_rececao.set('231454')
            self.ltxt_data_entrada_stock.set('01-01-1984')
            self.ltxt_num_quebra_stock.set('321123')
            self.ltxt_nar.set('2139467')

        self.ltxt_cod_artigo.set('Z0GV2345623P')
        self.ltxt_num_serie.set('C02G387HJG7865BNFV')
        self.ltxt_descr_avaria.set('Texto de exemplo para experimentar como sai na prática.\nIsto fica noutra linha...')
        self.ltxt_notas.set('Texto de exemplo para experimentar como sai na prática.\nIsto fica noutra linha...')


    def montar_tab_geral(self):
        # Montar todos os campos na grid -------------------------------------------------------------
        self.txt_numero_contacto.grid(column=0, row=0)
        self.btn_buscar_contacto.grid(column=1, row=0)
        self.txt_nome.grid(column=2, sticky='we', row=0)
        self.lbl_telefone.grid(column=3, sticky='w', row=0)
        self.lbl_email.grid(column=4, sticky='we', row=0)

        self.geral_fr1.grid_columnconfigure(4, weight=1)
        self.geral_fr1.grid_columnconfigure(3, weight=1)
        self.geral_fr1.grid_columnconfigure(2, weight=1)

        if self.is_rep_cliente:
            self.ltxt_descr_equipamento.grid(column=0, row=0, columnspan=2, rowspan=4, sticky='we', padx=4)
            self.ltxt_obs_estado_equipamento.grid(column=2, row=0, columnspan=2, rowspan=4, sticky='we', padx=4)
            self.ltxt_cod_artigo.grid(column=4, row=0, rowspan=2,  sticky='we', padx=4)
            self.ltxt_num_serie.grid(column=4, row=2, rowspan=2, sticky='we', padx=4)
            ttk.Separator(self.geral_fr2).grid(column=0, row=4, columnspan=5, sticky='we', pady=10)

            if self.is_garantia:
                self.ltxt_garantia.grid(column=0, row=5, columnspan=2, rowspan=2, sticky='we', padx=4)
                self.ltxt_data_compra.grid(column=2, row=5, rowspan=2, sticky='we', padx=4)
                self.ltxt_num_fatura.grid(column=3, row=5, rowspan=2, sticky='we', padx=4)

            self.ltxt_local_intervencao.grid(column=4, row=5, rowspan=2, sticky='we', padx=4)
            ttk.Separator(self.geral_fr2).grid(column=0, row=7, columnspan=5, sticky='we', pady=10)
            self.ltxt_descr_avaria.grid(column=0, row=8, columnspan=3, rowspan=4, sticky='we', padx=4)

            self.ltxt_senha.grid(column=3, row=8, rowspan=2, sticky='we', padx=4)

            self.lbl_varias_linhas.grid(column=4, row=8, columnspan=2, rowspan=4, sticky='we', padx=4)
            """
            self.lbl_avaria_reprod_loja.grid(column=4, row=8, columnspan=2, sticky='we', padx=4)
            self.lbl_efetuar_copia.grid(column=4, row=9, columnspan=2, sticky='we', padx=4)
            self.lbl_find_my.grid(column=4, row=10, columnspan=2, sticky='we', padx=4)
            self.lbl_modo_entrega.grid(column=4, row=11, columnspan=2, sticky='we', padx=4)
            """
            ttk.Separator(self.geral_fr2).grid(column=0, row=13, columnspan=5, sticky='we', pady=10)

            if self.modo_entrega <= 1:
                self.ltxt_acessorios.grid(column=0, row=14, columnspan=2, rowspan=3, sticky='wes', padx=4)
                self.ltxt_notas.grid(column=2, row=14, columnspan=3, rowspan=3, sticky='wes', padx=4)
            else:
                self.ltxt_acessorios.grid(column=0, row=14, columnspan=1, rowspan=3, sticky='wes', padx=4)
                self.ltxt_notas.grid(column=1, row=14, columnspan=3, rowspan=3, sticky='wes', padx=4)
                self.ltxt_morada_entrega.grid(column=4, row=14, columnspan=1, rowspan=3, sticky='wes', padx=4)

            for i in range(5):
                self.geral_fr2.grid_columnconfigure(i, weight=1)

        else:
            self.ltxt_descr_equipamento.grid(column=0, row=0, columnspan=2, rowspan=6, sticky='wens', padx=4)
            self.ltxt_cod_artigo.grid(column=2, row=0, rowspan=2,  sticky='we', padx=4)
            self.ltxt_num_serie.grid(column=2, row=2, rowspan=2, sticky='we', padx=4)
            self.ltxt_num_fatura_fornecedor.grid(column=3, row=0, rowspan=2, sticky='we', padx=4)
            self.ltxt_data_fatura_fornecedor.grid(column=3, row=2, rowspan=2, sticky='we', padx=4)
            self.ltxt_nar.grid(column=3, row=4, rowspan=2, sticky='we', padx=4)
            self.ltxt_num_guia_rececao.grid(column=4, row=0, rowspan=2, sticky='we', padx=4)
            self.ltxt_data_entrada_stock.grid(column=4, row=2, rowspan=2, sticky='we', padx=4)
            self.ltxt_num_quebra_stock.grid(column=4, row=4, rowspan=2, sticky='we', padx=4)

            ttk.Separator(self.geral_fr2).grid(column=0, row=7, columnspan=5, sticky='we', pady=10)
            self.ltxt_descr_avaria.grid(column=0, row=8, columnspan=5, rowspan=4, sticky='we', padx=4)
            ttk.Separator(self.geral_fr2).grid(column=0, row=12, columnspan=5, sticky='we', pady=10)
            self.ltxt_notas.grid(column=0, row=13, columnspan=5, rowspan=3, sticky='wes', padx=4)

            self.geral_fr2.grid_columnconfigure(0, weight=2)

            for i in range(1,5):
                self.geral_fr2.grid_columnconfigure(i, weight=1)
            self.geral_fr2.grid_columnconfigure(2, weight=1)
            self.geral_fr2.grid_columnconfigure(3, weight=1)

        self.geral_fr1.pack(side='top', expand=False, fill='x')
        ttk.Separator(self.tab_geral).pack(side='top', expand=False, fill='x', pady=10)
        self.geral_fr2.pack(side='top', expand=True, fill='both')


    def gerar_tab_historico(self):
        self.historico_fr1 = ttk.Frame(self.tab_historico)
        self.historico_fr2 = ttk.Frame(self.tab_historico)


    def montar_tab_historico(self):
        self.historico_fr1.pack(side='top', expand=False, fill='x')
        ttk.Separator(self.tab_historico).pack(side='top', expand=False, fill='x', pady=10)
        self.historico_fr2.pack(side='top', expand=True, fill='both')


    def gerar_tab_orcamentos(self):
        self.orcamentos_fr1 = ttk.Frame(self.tab_orcamentos)
        self.orcamentos_fr2 = ttk.Frame(self.tab_orcamentos)


    def montar_tab_orcamentos(self):
        self.orcamentos_fr1.pack(side='top', expand=False, fill='x')
        ttk.Separator(self.tab_orcamentos).pack(side='top', expand=False, fill='x', pady=10)
        self.orcamentos_fr2.pack(side='top', expand=True, fill='both')


    def gerar_tab_emprestimos(self):
        self.emprestimos_fr1 = ttk.Frame(self.tab_emprestimos)
        self.emprestimos_fr2 = ttk.Frame(self.tab_emprestimos)


    def montar_tab_emprestimos(self):
        self.emprestimos_fr1.pack(side='top', expand=False, fill='x')
        ttk.Separator(self.tab_emprestimos).pack(side='top', expand=False, fill='x', pady=10)
        self.emprestimos_fr2.pack(side='top', expand=True, fill='both')


    def desativar_campos(self):
        # Desativar todos os campos de texto para não permitir alterações. ------------------------
        self.txt_numero_contacto.configure(state="disabled")
        self.txt_nome.configure(state="disabled")

        widgets = ( self.ltxt_descr_equipamento,
                    self.ltxt_cod_artigo,
                    self.ltxt_num_serie,
                    self.ltxt_descr_avaria,
                    self.ltxt_notas)
        for widget in widgets:
            widget.disable()

        if self.is_rep_cliente:
            if self.is_garantia:
                self.ltxt_garantia.disable()
                self.ltxt_data_compra.disable()
                self.ltxt_num_fatura.disable()
            self.ltxt_obs_estado_equipamento.disable()
            self.ltxt_local_intervencao.disable()
            self.ltxt_acessorios.disable()
            self.ltxt_senha.disable()
            if self.modo_entrega > 1:
                self.ltxt_morada_entrega.disable()
        else:
            widgets = ( self.ltxt_num_fatura_fornecedor,
                        self.ltxt_data_fatura_fornecedor,
                        self.ltxt_num_guia_rececao,
                        self.ltxt_data_entrada_stock,
                        self.ltxt_num_quebra_stock,
                        self.ltxt_nar)
            for widget in widgets:
                widget.disable()


    def mostrar_painel_principal(self):
        self.note.pack(side='top', expand=True, fill='both')
        self.note.enable_traversal()


    def montar_rodape(self):
        #TODO - obter dados da base de dados
        txt_esquerda = "Criado por Victor Domingos em 12/05/2021 18:01."
        txt_direita = "Fechado por Victor Domingos em 13/05/2021 17:01."

        self.rodapeFont = tk.font.Font(family="Lucida Grande", size=9)
        self.rodapeTxtColor = "grey22"

        self.esquerda = ttk.Label(self.bottomframe, anchor='w', text=txt_esquerda, font=self.rodapeFont, foreground=self.rodapeTxtColor)
        self.direita = ttk.Label(self.bottomframe, anchor='e', text=txt_direita, font=self.rodapeFont, foreground=self.rodapeTxtColor)
        self.esquerda.pack(side="left")
        self.direita.pack(side="right")


    def configurar_frames_e_estilos(self):
        self.master.minsize(W_DETALHE_REP_MIN_WIDTH, W_DETALHE_REP_MIN_HEIGHT)
        self.master.maxsize(W_DETALHE_REP_MAX_WIDTH, W_DETALHE_REP_MAX_HEIGHT)
        #self.master.geometry(W_DETALHE_REP_GEOMETRIA)
        self.master.title(f"Reparação nº{self.num_reparacao} ({self.tipo_processo})")

        self.mainframe = ttk.Frame(self.master)
        self.topframe = ttk.Frame(self.mainframe, padding="5 8 5 5")
        self.centerframe = ttk.Frame(self.mainframe)
        self.bottomframe = ttk.Frame(self.mainframe, padding="3 1 3 1")

        self.estilo = ttk.Style()
        self.estilo.configure("Panel_Title.TLabel", pady=10, foreground="grey25", font=("Helvetica Neue", 18, "bold"))
        self.estilo.configure("Panel_Body.TLabel", font=("Lucida Grande", 11))
        self.estilo.configure("TMenubutton", font=("Lucida Grande", 11))

        self.btnFont = tk.font.Font(family="Lucida Grande", size=10)
        self.btnTxtColor = "grey22"


    def composeFrames(self):
        self.topframe.pack(side=tk.TOP, fill=tk.X)
        self.centerframe.pack(side=tk.TOP, expand=True, fill=tk.BOTH)
        self.bottomframe.pack(side=tk.BOTTOM, fill=tk.X)
        self.mainframe.pack(side=tk.TOP, expand=True, fill=tk.BOTH)
