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
import textwrap

import detalhe_contacto
from extra_tk_classes import AutoScrollbar, LabelEntry, LabelText
from global_setup import *


if USE_LOCAL_DATABASE:
    import db_local_main as db
else:
    import db_remote as db


class repairDetailWindow(ttk.Frame):
    """ Classe de base para a janela de detalhes de reparações """

    def __init__(self, master, num_reparacao, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master = master
        self.master.bind("<Command-w>", self.on_btn_fechar)
        self.contacto_newDetailsWindow = {}
        self.contact_detail_windows_count = 0
        self.master.focus()
        self.num_reparacao = num_reparacao
        self.repair = db.obter_reparacao(self.num_reparacao)
        self.cliente = self.repair.cliente
        self.fornecedor = self.repair.fornecedor
        self.prioridade = self.repair.prioridade
        self.tipo_processo = "Cliente" if (self.repair.is_stock == 0) else "Stock"
        self.is_rep_cliente = not self.repair.is_stock
        self.estado = self.repair.estado_reparacao
        self.is_garantia = self.repair.is_garantia
        self.modo_entrega = self.repair.modo_entrega  # todo - obter da base de dados
        self.portes = self.repair.cliente_pagou_portes  # todo - obter da base de dados

        if self.is_rep_cliente:
            self.numero_contacto = self.cliente.id
            self.nome = self.cliente.nome
            self.telefone = self.cliente.telefone
            self.email = self.cliente.email
            self.var_combo_artigos_emprest = tk.StringVar()
            self.var_combo_artigos_emprest.set("Selecionar artigo...")
            self.var_combo_artigos_emprest.trace(
                'w', self._on_combo_artigos_emprest_changed)
            self.var_combo_meio_pag_emprest = tk.StringVar()
            self.var_combo_meio_pag_emprest.set(
                "Selecionar forma de pagamento...")
            self.var_id_art_emprest = tk.StringVar()
            self.var_id_art_emprest.trace('w', self._on_id_art_emprest_changed)
        else:
            self.numero_contacto = self.fornecedor.id
            self.nome = self.fornecedor.nome
            self.telefone = self.fornecedor.telefone
            self.email = self.fornecedor.email

        self.configurar_frames_e_estilos()
        self.montar_barra_de_ferramentas()
        self.gerar_painel_principal()
        self.mostrar_painel_principal()

        self.montar_rodape()
        self.composeFrames()
        self.inserir_dados_de_exemplo()
        self.alternar_cores(self.tree_hist)
        if self.is_rep_cliente:
            self.alternar_cores(self.tree_emprest)

    def montar_barra_de_ferramentas(self):
        self.lbl_titulo = ttk.Label(self.topframe, style="Panel_Title.TLabel",
                                    foreground=self.btnTxtColor, text=f"Reparação nº {self.num_reparacao}")

        # Reincidência apenas aparece se reparação está entregue, anulado,
        # abandonado, sem_informacao
        if self.estado >= ENTREGUE:
            self.btn_reincidencia = ttk.Button(self.topframe, text="➕ Reincidência", width=4, command=None)
            self.dicas.bind(self.btn_reincidencia, 'Criar novo processo de reincidência\ncom base nesta reparação.')

        # Botão para registar entrega apenas aparece se reparação ainda não
        # está entregue
        if self.estado != ENTREGUE:
            self.btn_entregar = ttk.Button(
                self.topframe, text=" ✅", width=4, command=lambda:self._on_repair_state_change(ENTREGUE))
            self.dicas.bind(self.btn_entregar,
                            'Marcar esta reparação como entregue.')

        # ----------- Botão com menu "Alterar estado" --------------
        self.mbtn_alterar_estado = ttk.Menubutton(self.topframe, style="TMenubutton", text=ESTADOS[self.estado])
        self.mbtn_alterar_estado.menu = tk.Menu(self.mbtn_alterar_estado, tearoff=0)
        self.mbtn_alterar_estado["menu"] = self.mbtn_alterar_estado.menu

        self.mbtn_alterar_estado.menu.add_command(label=ESTADOS[EM_PROCESSAMENTO], command=lambda:self._on_repair_state_change(EM_PROCESSAMENTO))
        self.mbtn_alterar_estado.menu.add_command(label=ESTADOS[AGUARDA_ENVIO], command=lambda:self._on_repair_state_change(AGUARDA_ENVIO))
        self.mbtn_alterar_estado.menu.add_command(label=ESTADOS[AGUARDA_RESP_FORNECEDOR], command=lambda:self._on_repair_state_change(AGUARDA_RESP_FORNECEDOR))
        self.mbtn_alterar_estado.menu.add_command(label=ESTADOS[AGUARDA_RESP_CLIENTE], command=lambda:self._on_repair_state_change(AGUARDA_RESP_CLIENTE))
        self.mbtn_alterar_estado.menu.add_command(label=ESTADOS[AGUARDA_RECECAO], command=lambda:self._on_repair_state_change(AGUARDA_RECECAO))
        self.mbtn_alterar_estado.menu.add_command(label=ESTADOS[RECEBIDO], command=lambda:self._on_repair_state_change(RECEBIDO))
        self.mbtn_alterar_estado.menu.add_command(label=ESTADOS[DISPONIVEL_P_LEVANTAMENTO], command=lambda:self._on_repair_state_change(DISPONIVEL_P_LEVANTAMENTO))
        self.mbtn_alterar_estado.menu.add_separator()
        self.mbtn_alterar_estado.menu.add_command(label=ESTADOS[ENTREGUE], command=lambda:self._on_repair_state_change(ENTREGUE))
        self.mbtn_alterar_estado.menu.add_separator()
        self.mbtn_alterar_estado.menu.add_command(label=ESTADOS[ANULADO], command=lambda:self._on_repair_state_change(ANULADO))
        self.mbtn_alterar_estado.menu.add_command(label=ESTADOS[ABANDONADO], command=lambda:self._on_repair_state_change(ABANDONADO))
        self.mbtn_alterar_estado.menu.add_command(label=ESTADOS[SEM_INFORMACAO], command=lambda:self._on_repair_state_change(SEM_INFORMACAO))
        self.dicas.bind(self.mbtn_alterar_estado, 'Alterar o estado deste processo de reparação.')
        # ----------- fim de Botão com menu "Alterar estado" -------------

        # ----------- Botão com menu "Alterar Prioridade" --------------
        self.mbtn_alterar_prioridade = ttk.Menubutton(self.topframe, text=f"Prioridade: {PRIORIDADES[self.prioridade]}")
        self.mbtn_alterar_prioridade.menu = tk.Menu(self.mbtn_alterar_prioridade, tearoff=0)
        self.mbtn_alterar_prioridade["menu"] = self.mbtn_alterar_prioridade.menu
        self.mbtn_alterar_prioridade.menu.add_command(label=PRIORIDADES[0], command=lambda:self._on_priority_change(0))
        self.mbtn_alterar_prioridade.menu.add_command(label=PRIORIDADES[1], command=lambda:self._on_priority_change(1))
        self.mbtn_alterar_prioridade.menu.add_command(label=PRIORIDADES[2], command=lambda:self._on_priority_change(2))
        self.mbtn_alterar_prioridade.menu.add_command(label=PRIORIDADES[3], command=lambda:self._on_priority_change(3))

        self.dicas.bind(self.mbtn_alterar_prioridade,'Alterar a prioridade deste processo de reparação.')
        # ----------- fim de Botão com menu "Alterar Prioridade" -------------

        # ----------- Botão com menu "Copiar" --------------
        self.mbtn_copiar = ttk.Menubutton(self.topframe, text=" ⚡")
        self.mbtn_copiar.menu = tk.Menu(self.mbtn_copiar, tearoff=0)
        self.mbtn_copiar["menu"] = self.mbtn_copiar.menu

        if self.is_rep_cliente:
            self.mbtn_copiar.menu.add_command(label="Nome", command=None)
            self.mbtn_copiar.menu.add_command(label="NIF", command=None)
            self.mbtn_copiar.menu.add_command(label="Morada", command=None)
            self.mbtn_copiar.menu.add_command(
                label="Código Postal", command=None)
            self.mbtn_copiar.menu.add_command(label="Localidade", command=None)
            if self.modo_entrega >= 1:
                self.mbtn_copiar.menu.add_separator()
                self.mbtn_copiar.menu.add_command(
                    label="Morada para entrega", command=None)
                self.mbtn_copiar.menu.add_separator()

        self.mbtn_copiar.menu.add_command(label="Email", command=None)
        self.mbtn_copiar.menu.add_command(label="Telefone", command=None)
        self.mbtn_copiar.menu.add_separator()
        self.mbtn_copiar.menu.add_command(
            label="Descrição do equipamento", command=None)
        self.mbtn_copiar.menu.add_command(
            label="Número de série", command=None)
        self.dicas.bind(
            self.mbtn_copiar, 'Clique para selecionar e copiar\ndados referentes a este processo\npara a Área de Transferência.')
        # ----------- fim de Botão com menu "Copiar" -------------

        # ----------- Botão com menu "Imprimir" --------------
        self.mbtn_imprimir = ttk.Menubutton(self.topframe, text="Imprimir")
        self.mbtn_imprimir.menu = tk.Menu(self.mbtn_imprimir, tearoff=0)
        self.mbtn_imprimir["menu"] = self.mbtn_imprimir.menu

        self.mbtn_imprimir.menu.add_command(
            label="Guia de receção: loja e cliente", command=None)
        self.mbtn_imprimir.menu.add_command(
            label="Guia de receção: loja e serviço técnico", command=None)

        # TODO - Ocultar ou desativar estas opções se não houver um orçamento
        # criado para esta reparação
        self.mbtn_imprimir.menu.add_separator()
        self.mbtn_imprimir.menu.add_command(label="Orçamento", command=None)
        self.mbtn_imprimir.menu.add_command(
            label="Recibo de pagamento: orçamento", command=None)

        # TODO - Ocultar ou desativar estas opções se não houver um empréstimo
        # criado para esta reparação
        self.mbtn_imprimir.menu.add_separator()
        self.mbtn_imprimir.menu.add_command(
            label="Documento de empréstimo", command=None)
        self.mbtn_imprimir.menu.add_command(
            label="Recibo de pagamento: caução de empréstimo", command=None)
        self.dicas.bind(
            self.mbtn_imprimir, 'Clique para selecionar\no tipo de documento a imprimir.')
        # ----------- fim de Botão com menu "Imprimir" -------------

        self.btn_comunicacao = ttk.Button(
            self.topframe, text="✉️", width=4, command=None)
        self.dicas.bind(self.btn_comunicacao,
                        'Clique para selecionar\no tipo de comunicação a enviar e registar.')

        self.lbl_titulo.grid(column=0, row=0, rowspan=2)
        self.mbtn_alterar_estado.grid(column=4, row=0)
        self.mbtn_alterar_prioridade.grid(column=5, row=0)
        self.btn_comunicacao.grid(column=7, row=0)
        self.mbtn_copiar.grid(column=8, row=0)
        self.mbtn_imprimir.grid(column=9, row=0)

        # Reincidência apenas aparece se reparação está entregue, anulado,
        # abandonado, sem_informacao
        if self.estado >= ENTREGUE:
            self.btn_reincidencia.grid(column=10, row=0)

        # Botão para registar entrega apenas aparece se reparação ainda não
        # está entregue
        if self.estado != ENTREGUE:
            self.btn_entregar.grid(column=11, row=0)

        self.topframe.grid_columnconfigure(2, weight=1)

    def gerar_painel_principal(self):
        print(f"A mostrar detalhes da reparação nº {self.num_reparacao}")

        # Preparar o notebook da secção principal ------------------------
        self.note = ttk.Notebook(self.centerframe, padding="3 20 3 3")
        #self.note.bind_all("<<NotebookTabChanged>>", self._on_tab_changed)

        self.tab_geral = ttk.Frame(self.note, padding=10)
        self.tab_historico = ttk.Frame(self.note, padding=10)
        self.note.add(self.tab_geral, text="Geral")
        self.note.add(self.tab_historico, text="Histórico")
        self.gerar_tab_geral()
        self.montar_tab_geral()
        self.gerar_tab_historico()
        self.montar_tab_historico()

        # TODO

        if self.is_rep_cliente:
            self.tab_orcamentos = ttk.Frame(self.note, padding=10)
            self.tab_emprestimos = ttk.Frame(self.note, padding=10)
            #self.note.add(self.tab_orcamentos, text="Orçamentos")
            self.note.add(self.tab_emprestimos, text="Empréstimos")
            self.gerar_tab_orcamentos()
            self.gerar_tab_emprestimos()
            # self.montar_tab_orcamentos()
            self.montar_tab_emprestimos()

        self.desativar_campos()

    def atualizar_combo_artigos_emprest(self):
        """ Atualizar a lista de locais de artigos de empréstimo, obtendo info
            a partir da base de dados.
        """
        artigos = obter_lista_artigos_emprest()
        lista_strings = []
        for item in artigos.keys():
            if artigos[item][1] == "":
                linha = f'{item} - {artigos[item][0]}'
            else:
                linha = f'{item} - {artigos[item][0]} - {artigos[item][1]}'

            lista_strings.append(linha)
        self.combo_artigos_emprestimo['values'] = lista_strings

    def _on_tab_changed(self, event):
        event.widget.update_idletasks()
        tab = event.widget.nametowidget(event.widget.select())
        event.widget.configure(height=tab.winfo_reqheight(),
                               width=tab.winfo_reqwidth())

    def create_window_detalhe_contacto(self, *event):
        self.contact_detail_windows_count += 1
        self.contacto_newDetailsWindow[self.contact_detail_windows_count] = tk.Toplevel(
        )
        self.contacto_newDetailsWindow[self.contact_detail_windows_count].title(
            f'Detalhe de contacto: {self.numero_contacto}')
        self.janela_detalhes_contacto = detalhe_contacto.contactDetailWindow(
            self.contacto_newDetailsWindow[self.contact_detail_windows_count],
            self.numero_contacto)
        self.contacto_newDetailsWindow[self.contact_detail_windows_count].focus(
        )

    def gerar_tab_geral(self):
        # TAB Geral ~~~~~~~~~~~~~~~~
        self.geral_fr1 = ttk.Frame(self.tab_geral)
        self.geral_fr2 = ttk.Frame(self.tab_geral)

        # TODO - obter valor da base de dados
        # Criar widgets para este separador -----------------------------------
        self.txt_numero_contacto = ttk.Entry(
            self.geral_fr1, font=("Helvetica-Neue", 12), width=5)
        self.btn_buscar_contacto = ttk.Button(
            self.geral_fr1, width=1, text="+", command=self.create_window_detalhe_contacto)
        self.txt_nome = ttk.Entry(
            self.geral_fr1, font=("Helvetica-Neue", 12), width=35)
        self.lbl_telefone = ttk.Label(
            self.geral_fr1, style="Panel_Body.TLabel", text=f"Tel.:{self.telefone}")
        self.lbl_email = ttk.Label(
            self.geral_fr1, style="Panel_Body.TLabel", text=f"Email:{self.email}")

        self.ltxt_descr_equipamento = LabelText(
            self.geral_fr2, "Descrição:", style="Panel_Body.TLabel", height=2, width=40)

        if self.is_rep_cliente:
            # TODO: obter string do estado do equipamento
            estado = f'Estado: {"Marcas de acidente"}'
            self.ltxt_obs_estado_equipamento = LabelText(
                self.geral_fr2, estado, style="Panel_Body.TLabel", height=2)
            self.ltxt_local_intervencao = LabelEntry(
                self.geral_fr2, "Local da intervenção:", style="Panel_Body.TLabel", width=25)
            self.ltxt_acessorios = LabelText(
                self.geral_fr2, "Acessórios entregues:", style="Panel_Body.TLabel")
            if self.is_garantia:
                self.ltxt_data_compra = LabelEntry(
                    self.geral_fr2, "Data de compra:", style="Panel_Body.TLabel", width=10)
                self.ltxt_num_fatura = LabelEntry(
                    self.geral_fr2, "Nº da fatura:", style="Panel_Body.TLabel", width=15)
                self.ltxt_garantia = LabelEntry(
                    self.geral_fr2, "Garantia em:", style="Panel_Body.TLabel")
            else:
                self.lbl_garantia = ttk.Label(
                    self.geral_fr2, text="Garantia:\nFora de garantia", style="Panel_Body.TLabel")

        self.ltxt_cod_artigo = LabelEntry(
            self.geral_fr2, "Código de artigo:", style="Panel_Body.TLabel")
        self.ltxt_num_serie = LabelEntry(
            self.geral_fr2, "Nº de série:", style="Panel_Body.TLabel")

        self.ltxt_descr_avaria = LabelText(
            self.geral_fr2, "Avaria/Serviço:", style="Panel_Body.TLabel")
        self.ltxt_notas = LabelText(
            self.geral_fr2, "Notas:", style="Panel_Body.TLabel")

        if self.is_rep_cliente:
            self.ltxt_senha = LabelEntry(
                self.geral_fr2, "Senha:", style="Panel_Body.TLabel", width=22)
            varias_linhas = "• Avaria reproduzida na loja"
            varias_linhas += "\n• Find my iPhone ativo"
            varias_linhas += "\n• Efetuar cópia de segurança"

            if self.modo_entrega == 0:
                varias_linhas += "\n• Levantamento nas n/ instalações"
            elif self.modo_entrega == 1:
                varias_linhas += "\n• Enviar para a morada da ficha de cliente"
            else:
                varias_linhas += "\n• Enviar para a morada abaixo indicada"
                self.ltxt_morada_entrega = LabelText(
                    self.geral_fr2, "Morada a utilizar na entrega:", style="Panel_Body.TLabel")

            if self.modo_entrega != 0:
                if self.portes == 0:
                    varias_linhas += "\n• Cliente ainda não pagou portes"
                elif self.portes == 1:
                    varias_linhas += "\n• Cliente já pagou portes"
                elif self.portes == 2:
                    varias_linhas += "\n• Oferta de portes grátis"

            self.lbl_varias_linhas = ttk.Label(
                self.geral_fr2, style="Panel_Body.TLabel", text=varias_linhas)

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
            self.ltxt_num_fatura_fornecedor = LabelEntry(
                self.geral_fr2, "Nº fatura fornecedor:", style="Panel_Body.TLabel", width=15)
            self.ltxt_data_fatura_fornecedor = LabelEntry(
                self.geral_fr2, "Data fatura fornecedor:", style="Panel_Body.TLabel", width=10)
            self.ltxt_nar = LabelEntry(
                self.geral_fr2, "NAR:", style="Panel_Body.TLabel", width=7)
            self.ltxt_num_guia_rececao = LabelEntry(
                self.geral_fr2, "Guia de receção:", style="Panel_Body.TLabel", width=6)
            self.ltxt_data_entrada_stock = LabelEntry(
                self.geral_fr2, "Data de entrada em stock:", style="Panel_Body.TLabel", width=15)
            self.ltxt_num_quebra_stock = LabelEntry(
                self.geral_fr2, "Nº de quebra de stock:", style="Panel_Body.TLabel", width=6)

        # Preencher com dados da base de dados --------------------------------
        self.txt_numero_contacto.insert(0, self.numero_contacto)
        self.txt_nome.insert(0, self.nome)

        self.ltxt_descr_equipamento.set(
            'Texto de exemplo para experimentar como sai na prática.\nIsto fica noutra linha...')
        if self.is_rep_cliente:
            self.ltxt_obs_estado_equipamento.set(
                'Texto de exemplo para experimentar como sai na prática.\n Equipamentos em excelente estado.')
            self.ltxt_local_intervencao.set('Aquele Tal Centro Técnico')
            self.ltxt_acessorios.set(
                'Texto de exemplo para experimentar como sai na prática.\nIsto fica noutra linha...')
            self.ltxt_senha.set('12343112121')
            if self.is_garantia:
                self.ltxt_data_compra.set('29-07-2035')
                self.ltxt_num_fatura.set('FCR 1234567890/2035')
                self.ltxt_garantia.set('NPK International Online Store')
            if self.modo_entrega > 1:
                self.ltxt_morada_entrega.set(
                    "José manuel da silva fictício\nRua imaginária da conceição esplendorosa, nº 31, 3º andar frente\n1234-567 CIDADE MARAVILHOSA BRG\nPortugal")
        else:
            self.ltxt_num_fatura_fornecedor.set('C23918237323812371237/2017')
            self.ltxt_data_fatura_fornecedor.set('01-04-1974')
            self.ltxt_num_guia_rececao.set('231454')
            self.ltxt_data_entrada_stock.set('01-01-1984')
            self.ltxt_num_quebra_stock.set('321123')
            self.ltxt_nar.set('2139467')

        self.ltxt_cod_artigo.set('Z0GV2345623P')
        self.ltxt_num_serie.set('C02G387HJG7865BNFV')
        self.ltxt_descr_avaria.set(
            'Texto de exemplo para experimentar como sai na prática.\nIsto fica noutra linha...')
        self.ltxt_notas.set(
            'Texto de exemplo para experimentar como sai na prática.\nIsto fica noutra linha...')

    def montar_tab_geral(self):
        # Montar todos os campos na grid --------------------------------------
        self.txt_numero_contacto.grid(column=0, row=0)
        self.btn_buscar_contacto.grid(column=1, row=0)
        self.txt_nome.grid(column=2, sticky='we', row=0)
        self.lbl_telefone.grid(column=3, sticky='w', row=0)
        self.lbl_email.grid(column=4, sticky='we', row=0)

        self.geral_fr1.grid_columnconfigure(4, weight=1)
        self.geral_fr1.grid_columnconfigure(3, weight=1)
        self.geral_fr1.grid_columnconfigure(2, weight=1)

        self.geral_fr2.grid_rowconfigure(3, weight=1)
        self.geral_fr2.grid_rowconfigure(10, weight=1)
        self.geral_fr2.grid_rowconfigure(10, weight=1)
        self.geral_fr2.grid_rowconfigure(15, weight=1)

        if self.is_rep_cliente:
            self.ltxt_descr_equipamento.grid(
                column=0, row=0, columnspan=2, rowspan=4, sticky='nwes', padx=4)
            self.ltxt_obs_estado_equipamento.grid(
                column=2, row=0, columnspan=2, rowspan=4, sticky='nwes', padx=4)
            self.ltxt_cod_artigo.grid(
                column=4, row=0, rowspan=2, sticky='nwe', padx=4)
            self.ltxt_num_serie.grid(
                column=4, row=2, rowspan=2, sticky='nwe', padx=4)
            ttk.Separator(self.geral_fr2).grid(column=0, row=4,
                                               columnspan=5, sticky='nwe', pady=10)

            if self.is_garantia:
                self.ltxt_garantia.grid(
                    column=0, row=5, columnspan=2, rowspan=2, sticky='nwe', padx=4)
                self.ltxt_data_compra.grid(
                    column=2, row=5, rowspan=2, sticky='nwe', padx=4)
                self.ltxt_num_fatura.grid(
                    column=3, row=5, rowspan=2, sticky='nwe', padx=4)

            self.ltxt_local_intervencao.grid(
                column=4, row=5, rowspan=2, sticky='nwe', padx=4)
            ttk.Separator(self.geral_fr2).grid(
                column=0, row=7, columnspan=5, sticky='we', pady=10)
            self.ltxt_descr_avaria.grid(
                column=0, row=8, columnspan=3, rowspan=5, sticky='wesn', padx=4)

            self.ltxt_senha.grid(
                column=3, row=8, rowspan=2, sticky='nwe', padx=4)

            self.lbl_varias_linhas.grid(
                column=4, row=9, columnspan=2, rowspan=4, sticky='wen', padx=4)
            """
            self.lbl_avaria_reprod_loja.grid(column=4, row=8, columnspan=2, sticky='we', padx=4)
            self.lbl_efetuar_copia.grid(column=4, row=9, columnspan=2, sticky='we', padx=4)
            self.lbl_find_my.grid(column=4, row=10, columnspan=2, sticky='we', padx=4)
            self.lbl_modo_entrega.grid(column=4, row=11, columnspan=2, sticky='we', padx=4)
            """
            ttk.Separator(self.geral_fr2).grid(
                column=0, row=13, columnspan=5, sticky='we', pady=10)

            if self.modo_entrega <= 1:
                self.ltxt_acessorios.grid(
                    column=0, row=14, columnspan=2, rowspan=3, sticky='wesn', padx=4)
                self.ltxt_notas.grid(
                    column=2, row=14, columnspan=3, rowspan=3, sticky='wesn', padx=4)
            else:
                self.ltxt_acessorios.grid(
                    column=0, row=14, columnspan=1, rowspan=3, sticky='wesn', padx=4)
                self.ltxt_notas.grid(
                    column=1, row=14, columnspan=3, rowspan=3, sticky='wesn', padx=4)
                self.ltxt_morada_entrega.grid(
                    column=4, row=14, columnspan=1, rowspan=3, sticky='wesn', padx=4)

            for i in range(5):
                self.geral_fr2.grid_columnconfigure(i, weight=1)

        else:
            self.ltxt_descr_equipamento.grid(
                column=0, row=0, columnspan=2, rowspan=6, sticky='wens', padx=4)
            self.ltxt_cod_artigo.grid(
                column=2, row=0, rowspan=2, sticky='nwe', padx=4)
            self.ltxt_num_serie.grid(
                column=2, row=2, rowspan=2, sticky='nwe', padx=4)
            self.ltxt_num_fatura_fornecedor.grid(
                column=3, row=0, rowspan=2, sticky='nwe', padx=4)
            self.ltxt_data_fatura_fornecedor.grid(
                column=3, row=2, rowspan=2, sticky='nwe', padx=4)
            self.ltxt_nar.grid(column=3, row=4, rowspan=2,
                               sticky='nwe', padx=4)
            self.ltxt_num_guia_rececao.grid(
                column=4, row=0, rowspan=2, sticky='nwe', padx=4)
            self.ltxt_data_entrada_stock.grid(
                column=4, row=2, rowspan=2, sticky='nwe', padx=4)
            self.ltxt_num_quebra_stock.grid(
                column=4, row=4, rowspan=2, sticky='nwe', padx=4)

            ttk.Separator(self.geral_fr2).grid(
                column=0, row=7, columnspan=5, sticky='we', pady=10)
            self.ltxt_descr_avaria.grid(
                column=0, row=8, columnspan=5, rowspan=4, sticky='wesn', padx=4)
            ttk.Separator(self.geral_fr2).grid(
                column=0, row=12, columnspan=5, sticky='we', pady=10)
            self.ltxt_notas.grid(column=0, row=13, columnspan=5,
                                 rowspan=3, sticky='wesn', padx=4)

            self.geral_fr2.grid_columnconfigure(0, weight=2)

            for i in range(1, 5):
                self.geral_fr2.grid_columnconfigure(i, weight=1)
            self.geral_fr2.grid_columnconfigure(2, weight=1)
            self.geral_fr2.grid_columnconfigure(3, weight=1)

        self.geral_fr1.pack(side='top', expand=False, fill='x')
        ttk.Separator(self.tab_geral).pack(
            side='top', expand=False, fill='x', pady=10)
        self.geral_fr2.pack(side='top', expand=True, fill='both')

    def gerar_tab_historico(self):
        self.var_notificar = tk.IntVar()
        self.var_notificar.set(0)
        self.var_resultado = tk.StringVar()
        self.var_resultado.set(RESULTADOS[SEM_INFORMACAO])

        self.historico_fr1 = ttk.Frame(self.tab_historico)
        self.historico_fr2 = ttk.Frame(self.tab_historico)

        self.treeframe_hist = ttk.Frame(self.historico_fr2, padding="0 8 0 0")
        self.tree_hist = ttk.Treeview(
            self.treeframe_hist, height=5, selectmode='browse', style="Reparacoes_Historico.Treeview")
        self.tree_hist['columns'] = (
            'Nº', 'Descrição do evento', 'Estado', 'Utilizador', 'Data')
        self.tree_hist.column('#0', anchor='w', minwidth=0, stretch=0, width=0)
        self.tree_hist.column(
            'Nº', anchor='ne', minwidth=46, stretch=0, width=46)
        self.tree_hist.column('Descrição do evento',
                              anchor='nw', minwidth=260, stretch=1, width=260)
        self.tree_hist.column('Estado', anchor='nw',
                              minwidth=200, stretch=1, width=200)
        self.tree_hist.column('Utilizador', anchor='nw',
                              minwidth=140, stretch=1, width=140)
        self.tree_hist.column('Data', anchor='nw',
                              minwidth=80, stretch=1, width=80)

        # Ordenar por coluna ao clicar no respetivo cabeçalho
        # for col in self.tree['columns']:
        #    self.tree.heading(col, text=col.title(),
        #    command=lambda c=col: self.sortBy(self.tree, c, 0))

        for col in self.tree_hist['columns']:
            self.tree_hist.heading(col, text=col.title())

        # Barra de deslocação para a tabela
        self.tree_hist.grid(column=0, row=0, sticky="nsew",
                            in_=self.treeframe_hist)
        self.vsb_hist = AutoScrollbar(
            self.treeframe_hist, orient="vertical", command=self.tree_hist.yview)
        self.tree_hist.configure(yscrollcommand=self.vsb_hist.set)
        self.vsb_hist.grid(column=1, row=0, sticky="ns",
                           in_=self.treeframe_hist)

        self.bind_tree_hist()
        self.alternar_cores(self.tree_hist)

        self.hfr1_lbl_titulo = ttk.Label(
            self.historico_fr1, style="Panel_Title.TLabel", text="Adicionar Evento:\n")

        self.hfr1_lbl_resultado = ttk.Label(
            self.historico_fr1, style="Panel_Body.TLabel", text="Definir resultado:")
        self.ef_combo_resultado = ttk.Combobox(self.historico_fr1,
                                               textvariable=self.var_resultado,
                                               values=RESULTADOS,
                                               width=32,
                                               state='readonly')  # TODO: Obter estes valores a partir da base de dados, a utilizar também no formulário de Remessas.

        self.ef_combo_resultado.bind(
            '<<ComboboxSelected>>', self._on_combo_resultado_select)
        self.dicas.bind(self.ef_combo_resultado,
                        'Clique para selecionar o resultado do novo evento.')

        self.hfr1_chkbtn_notificar = ttk.Checkbutton(
            self.historico_fr1, variable=self.var_notificar, style="Panel_Body.Checkbutton", text="Notificar equipa")
        self.dicas.bind(self.hfr1_chkbtn_notificar,
                        'Assinale esta opção para enviar uma mensagem\ncom o conteúdo deste evento ao resto da sua equipa.')

        self.ef_ltxt_detalhes_evento = LabelText(
            self.historico_fr1, "\nDetalhes:", style="Panel_Body.TLabel", width=30, height=2)

        self.btn_adicionar = ttk.Button(self.historico_fr1, default="active",
                                        style="Active.TButton", text="Adicionar", command=self._on_save_evento)
        self.btn_cancelar = ttk.Button(
            self.historico_fr1, text="Cancelar", command=self._on_cancel_evento)

        self.bind_tree_hist()
        # self.desativar_campos()

    def montar_tab_historico(self):
        self.treeframe_hist.grid(column=0, row=0, sticky="nsew")
        self.treeframe_hist.grid_columnconfigure(0, weight=1)
        self.treeframe_hist.grid_rowconfigure(0, weight=1)
        self.historico_fr2.grid_columnconfigure(0, weight=1)
        self.historico_fr2.grid_rowconfigure(0, weight=1)

        self.hfr1_lbl_titulo.grid(column=0, row=0, sticky="nw", pady="15 3")
        self.hfr1_lbl_resultado.grid(column=0, row=1, sticky="nw")
        self.ef_combo_resultado.grid(column=0, row=2, sticky="nw")
        self.hfr1_chkbtn_notificar.grid(column=1, row=2, sticky="nw")
        self.ef_ltxt_detalhes_evento.grid(
            column=0, row=3, columnspan=3, rowspan=3, sticky="nwe")

        self.btn_adicionar.grid(column=2, row=1, sticky="nwe")
        self.btn_cancelar.grid(column=2, row=2, sticky="nwe")

        self.historico_fr1.grid_columnconfigure(0, weight=0)
        self.historico_fr1.grid_columnconfigure(1, weight=1)
        self.historico_fr1.grid_columnconfigure(2, weight=0)

        #ttk.Separator(self.tab_historico).pack(side='top', expand=False, fill='x', pady=10)
        self.historico_fr2.pack(side='top', expand=True, fill='both')
        self.historico_fr1.pack(side='bottom', expand=False, fill='x')

    def _on_combo_resultado_select(self, event):
        if self.var_resultado.get() == RESULTADOS[GARANTIA_APROVADA_REPARADO]:
            self.ef_ltxt_detalhes_evento.set_label(
                "\nDetalhes (serviço realizado, descrição e número de série das peças substituídas, etc.):")
        elif self.var_resultado.get() == RESULTADOS[GARANTIA_APROVADA_SUBSTITUIDO]:
            self.ef_ltxt_detalhes_evento.set_label(
                "\nDetalhes (número de série do novo artigo, etc.):")
        elif self.var_resultado.get() == RESULTADOS[GARANTIA_APROVADA_NOTA_DE_CREDITO]:
            self.ef_ltxt_detalhes_evento.set_label(
                "\nDetalhes (números das notas de crédito do fornecedor e da loja):")
        elif self.var_resultado.get() == RESULTADOS[GARANTIA_RECUSADA]:
            self.ef_ltxt_detalhes_evento.set_label(
                "\nDetalhes (motivo indicado pelo fornecedor ou centro técnico):")
        elif self.var_resultado.get() == RESULTADOS[ORCAMENTO_ACEITE]:
            self.ef_ltxt_detalhes_evento.set_label("\nDetalhes:")
        elif self.var_resultado.get() == RESULTADOS[ORCAMENTO_RECUSADO]:
            self.ef_ltxt_detalhes_evento.set_label(
                "\nDetalhes (motivo apontado pelo cliente):")
        else:
            self.ef_ltxt_detalhes_evento.set_label("\nDetalhes:")

        # TODO: criar regras para atribuição automática de novos estados do processo.
        # P. ex.: se orçamento aceite, perguntar utilizador se centro técnico
        # foi notificado. Se sim, AGUARDA_RESP_FORNECEDOR, se não cria email
        # modelo a informar centro técnico da decisão.

    def _on_combo_artigos_emprest_changed(self, index, value, op):
        if self.var_combo_artigos_emprest.get(
        ) != "O ID introduzido não corresponde a nenhum artigo existente.":
            id_artigo = self.var_combo_artigos_emprest.get().split(" - ")[0]
            self.var_id_art_emprest.set(id_artigo)

    def _on_id_art_emprest_changed(self, index, value, op):
        id_artigo_introduzido = self.ltxt_id_art.get()
        artigos = obter_lista_artigos_emprest()

        if id_artigo_introduzido in artigos.keys():
            if artigos[id_artigo_introduzido][1] == "":
                self.var_combo_artigos_emprest.set(
                    f"{id_artigo_introduzido} - {artigos[id_artigo_introduzido][0]}")
            else:
                self.var_combo_artigos_emprest.set(
                    f"{id_artigo_introduzido} - {artigos[id_artigo_introduzido][0]} - {artigos[id_artigo_introduzido][1]}")
        else:
            self.combo_artigos_emprestimo.set(
                "O ID introduzido não corresponde a nenhum artigo existente.")

    def _on_save_evento(self, *event):
        print(f"Guardando novo evento...")

    def _on_cancel_evento(self, *event):
        print(f"Cancelando introdução de dados...")

    def _on_save_emprest(self, *event):
        print(f"Guardando novo empréstimo...")

    def _on_cancel_emprest(self, *event):
        print(f"Cancelando introdução de dados de empréstimo...")


    def _on_repair_state_change(self, new_status):
        if self.estado == new_status:
            return
        else:
            self.estado = new_status
            self.mbtn_alterar_estado.configure(text=ESTADOS[self.estado])
            db.update_repair_status(self.num_reparacao, new_status)

    def _on_priority_change(self, new_priority):
        if self.prioridade == new_priority:
            return
        else:
            self.prioridade = new_priority
            self.mbtn_alterar_prioridade.configure(text=f"Prioridade: {PRIORIDADES[self.prioridade]}")
            db.update_repair_priority(self.num_reparacao, new_priority)


    def gerar_tab_orcamentos(self):
        self.orcamentos_fr1 = ttk.Frame(self.tab_orcamentos)
        self.orcamentos_fr2 = ttk.Frame(self.tab_orcamentos)
        """
        self.treeframe = ttk.Frame(self.orcamentos_fr1, padding="0 8 0 0")
        self.tree = ttk.Treeview(self.treeframe, height=6, selectmode='browse', style="Reparacoes_Historico.Treeview")
        self.tree['columns'] = ('Nº', 'Descrição do evento', 'Estado', 'Utilizador', 'Data')
        self.tree.column('#0', anchor='w', minwidth=0, stretch=0, width=0)
        self.tree.column('Nº', anchor='ne', minwidth=46, stretch=0, width=46)
        self.tree.column('Descrição do evento', anchor='nw', minwidth=260, stretch=1, width=260)
        self.tree.column('Estado', anchor='nw', minwidth=200, stretch=1, width=200)
        self.tree.column('Utilizador', anchor='nw', minwidth=140, stretch=1, width=140)
        self.tree.column('Data', anchor='nw', minwidth=80, stretch=1, width=80)

        # Ordenar por coluna ao clicar no respetivo cabeçalho
        #for col in self.tree['columns']:
        #    self.tree.heading(col, text=col.title(),
        #    command=lambda c=col: self.sortBy(self.tree, c, 0))

        for col in self.tree['columns']:
            self.tree.heading(col, text=col.title())


        # Barra de deslocação para a tabela
        self.tree.grid(column=0, row=0, sticky="nsew", in_=self.treeframe)
        self.vsb = AutoScrollbar(self.treeframe, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.vsb.set)
        self.vsb.grid(column=1, row=0, sticky="ns", in_=self.treeframe)


        self.hfr1_lbl_titulo = ttk.Label(self.historico_fr1, style="Panel_Title.TLabel", text="Adicionar Evento:\n")

        self.hfr1_lbl_resultado = ttk.Label(self.historico_fr1, style="Panel_Body.TLabel",  text="Definir resultado:")
        self.ef_combo_resultado = ttk.Combobox(self.historico_fr1,
              textvariable=self.var_resultado,
              values = RESULTADOS,
              width=32,
              state='readonly')  # TODO: Obter estes valores a partir da base de dados, a utilizar também no formulário de Remessas.

        self.ef_combo_resultado.bind('<<ComboboxSelected>>', self._on_combo_resultado_select)
        self.dicas.bind(self.ef_combo_resultado, 'Clique para selecionar o resultado do novo evento.')

        self.hfr1_chkbtn_notificar = ttk.Checkbutton(self.historico_fr1, variable=self.var_notificar, style="Panel_Body.Checkbutton", text="Notificar equipa")
        self.dicas.bind(self.hfr1_chkbtn_notificar, 'Assinale esta opção para enviar uma mensagem\ncom o conteúdo deste evento ao resto da sua equipa.')

        self.ef_ltxt_detalhes_evento = LabelText(self.historico_fr1, "\nDetalhes:", style="Panel_Body.TLabel", width=30, height=2)

        self.btn_adicionar = ttk.Button(self.historico_fr1, default="active", style="Active.TButton", text="Adicionar", command=self._on_save_evento)
        self.btn_cancelar = ttk.Button(self.historico_fr1, text="Cancelar", command=self._on_cancel_evento)

        #self.bind_tree()
        #self.desativar_campos()
        """

    def montar_tab_orcamentos(self):
        self.orcamentos_fr1.pack(side='top', expand=False, fill='x')
        ttk.Separator(self.tab_orcamentos).pack(
            side='top', expand=False, fill='x', pady=10)
        self.orcamentos_fr2.pack(side='top', expand=True, fill='both')

    def gerar_tab_emprestimos(self):
        self.emprestimos_fr1 = ttk.Frame(self.tab_emprestimos)
        self.emprestimos_fr2 = ttk.Frame(self.tab_emprestimos)
        self.emprestimos_fr3 = ttk.Frame(self.tab_emprestimos)
        self.emprestimos_fr4 = ttk.Frame(
            self.tab_emprestimos, padding="0 20 0 0")
        self.emprestimos_lblfr_pag = ttk.LabelFrame(
            self.emprestimos_fr4, text="Pagamento de caução")

        self.ltxt_id_art = LabelEntry(
            self.emprestimos_fr1, "ID:", style="Panel_Body.TLabel", width=10)
        self.ltxt_id_art.entry.config(textvariable=self.var_id_art_emprest)

        self.lbl_combo_artigos_emprestimo = ttk.Label(
            self.emprestimos_fr1, style="Panel_Body.TLabel", text="Artigo a adicionar:")
        self.combo_artigos_emprestimo = ttk.Combobox(self.emprestimos_fr1,
                                                     textvariable=self.var_combo_artigos_emprest,
                                                     postcommand=self.atualizar_combo_artigos_emprest,
                                                     state="readonly"
                                                     )  # TODO: Obter estes valores a partir da base de dados, a utilizar também no formulário de Remessas.

        self.ltxt_qtd = LabelEntry(
            self.emprestimos_fr1, "Qtd.:", style="Panel_Body.TLabel", width=3)
        self.ltxt_qtd.entry.config(justify="right")
        self.ltxt_qtd.set("1")

        self.btn_inserir_art_emprest = ttk.Button(
            self.emprestimos_fr1, text="Inserir", command=self._on_btn_inserir_art_emprest)
        self.btn_ver_artigos_emprest = ttk.Button(
            self.emprestimos_fr1, text="Ver artigos", command=self._on_btn_ver_artigos_emprest)

        self.treeframe_emprest = ttk.Frame(
            self.emprestimos_fr2, padding="0 8 0 0")
        self.tree_emprest = ttk.Treeview(
            self.treeframe_emprest, height=3, selectmode='browse', style="Reparacoes_Emprestimo.Treeview")
        self.tree_emprest['columns'] = (
            'ID', 'Cód.', 'Descrição', 'S/N', 'Qtd.')
        self.tree_emprest.column(
            '#0', anchor='w', minwidth=0, stretch=0, width=0)
        self.tree_emprest.column(
            'ID', anchor='e', minwidth=35, stretch=0, width=35)
        self.tree_emprest.column(
            'Cód.', anchor='w', minwidth=60, stretch=1, width=65)
        self.tree_emprest.column(
            'Descrição', anchor='w', minwidth=300, stretch=1, width=400)
        self.tree_emprest.column(
            'S/N', anchor='w', minwidth=85, stretch=1, width=100)
        self.tree_emprest.column(
            'Qtd.', anchor='e', minwidth=35, stretch=0, width=35)

        # Ordenar por coluna ao clicar no respetivo cabeçalho
        # for col in self.tree_emprest['columns']:
        #    self.tree_emprest.heading(col, text=col.title(),
        #    command=lambda c=col: self.sortBy(self.tree_emprest, c, 0))

        for col in self.tree_emprest['columns']:
            self.tree_emprest.heading(col, text=col.title())

        # Barra de deslocação para a tabela
        self.tree_emprest.grid(
            column=0, row=0, sticky="nsew", in_=self.treeframe_emprest)
        self.vsb_emprest = AutoScrollbar(
            self.treeframe_emprest, orient="vertical", command=self.tree_emprest.yview)
        self.tree_emprest.configure(yscrollcommand=self.vsb_emprest.set)
        self.vsb_emprest.grid(column=1, row=0, sticky="ns",
                              in_=self.treeframe_emprest)

        self.ltxt_obs_estado_equipamentos_emprest = LabelText(
            self.emprestimos_fr3, "Estado dos artigos emprestados", style="Panel_Body.TLabel")
        self.ltxt_acessorios_emprest = LabelText(
            self.emprestimos_fr3, "Acessórios entregues:", style="Panel_Body.TLabel")

        self.ltxt_valor_caucao_emprest = LabelEntry(
            self.emprestimos_lblfr_pag, "Montante pago:", style="Panel_Body.TLabel", width=12)

        self.lbl_combo_meio_pag_emprest = ttk.Label(
            self.emprestimos_lblfr_pag, text="Forma de pagamento:", style="Panel_Body.TLabel", )
        self.combo_meio_pag_emprest = ttk.Combobox(self.emprestimos_lblfr_pag,
                                                   textvariable=self.var_combo_meio_pag_emprest,
                                                   values=("Numerário", "Transferência", "Multibanco", "Referência Multibanco",
                                                           "Cheque (indicar banco e nº de cheque)", "Outra (especificar)"),
                                                   state="readonly",
                                                   width=25
                                                   )

        self.ltxt_detalhes_pagamento_emprest = LabelEntry(
            self.emprestimos_lblfr_pag, "Detalhes:", style="Panel_Body.TLabel", width=25)
        self.ltxt_data_pagamento_emprest = LabelEntry(
            self.emprestimos_lblfr_pag, "Data pagamento:", style="Panel_Body.TLabel", width=12)

        self.btn_guardar_emprest = ttk.Button(
            self.emprestimos_fr4, text="Guardar", default="active", style="Active.TButton", command=self._on_save_emprest)
        self.btn_cancelar_emprest = ttk.Button(
            self.emprestimos_fr4, text="Cancelar", command=self._on_cancel_emprest)

        """
        self.hfr1_lbl_titulo = ttk.Label(self.historico_fr1, style="Panel_Title.TLabel", text="Adicionar Evento:\n")

        self.hfr1_lbl_resultado = ttk.Label(self.historico_fr1, style="Panel_Body.TLabel",  text="Definir resultado:")
        self.ef_combo_resultado = ttk.Combobox(self.historico_fr1,
                    textvariable=self.var_resultado,
                    values = RESULTADOS,
                    width=32,
                    state='readonly')  # TODO: Obter estes valores a partir da base de dados, a utilizar também no formulário de Remessas.

        self.ef_combo_resultado.bind('<<ComboboxSelected>>', self._on_combo_resultado_select)
        self.dicas.bind(self.ef_combo_resultado, 'Clique para selecionar o resultado do novo evento.')

        self.hfr1_chkbtn_notificar = ttk.Checkbutton(self.historico_fr1, variable=self.var_notificar, style="Panel_Body.Checkbutton", text="Notificar equipa")
        self.dicas.bind(self.hfr1_chkbtn_notificar, 'Assinale esta opção para enviar uma mensagem\ncom o conteúdo deste evento ao resto da sua equipa.')

        self.ef_ltxt_detalhes_evento = LabelText(self.historico_fr1, "\nDetalhes:", style="Panel_Body.TLabel", width=30, height=2)

        self.btn_adicionar = ttk.Button(self.historico_fr1, default="active", style="Active.TButton", text="Adicionar", command=self._on_save_evento)
        self.btn_cancelar = ttk.Button(self.historico_fr1, text="Cancelar", command=self._on_cancel_evento)
        """
        # self.bind_tree()
        # self.desativar_campos()

    def montar_tab_emprestimos(self):
        self.ltxt_id_art.grid(column=0, row=1, rowspan=2, sticky='nw')
        self.lbl_combo_artigos_emprestimo.grid(column=1, row=1, sticky='nw')
        self.combo_artigos_emprestimo.grid(column=1, row=2, sticky='new')
        self.ltxt_qtd.grid(column=2, row=1, rowspan=2, sticky='nw')
        self.btn_inserir_art_emprest.grid(column=3, row=2, sticky='new')
        self.btn_ver_artigos_emprest.grid(
            column=4, row=2, sticky='new', padx="45 0")

        self.treeframe_emprest.grid(column=0, row=0, sticky="nsew")
        self.treeframe_emprest.grid_columnconfigure(0, weight=1)
        self.treeframe_emprest.grid_rowconfigure(0, weight=1)

        self.ltxt_acessorios_emprest.grid(
            column=0, row=0, sticky='wesn', pady=14, padx=4)
        self.ltxt_obs_estado_equipamentos_emprest.grid(
            column=1, row=0, sticky='nwes', pady=14, padx=4)

        self.ltxt_valor_caucao_emprest.grid(
            column=0, row=1, rowspan=2, sticky='new')
        self.lbl_combo_meio_pag_emprest.grid(column=1, row=1, sticky='new')
        self.combo_meio_pag_emprest.grid(column=1, row=2, sticky='new')
        self.ltxt_detalhes_pagamento_emprest.grid(
            column=2, row=1, rowspan=2, sticky='new')
        self.ltxt_data_pagamento_emprest.grid(
            column=0, row=3, rowspan=2, sticky='new')

        self.emprestimos_lblfr_pag.grid(
            column=0, row=0, rowspan=5, padx=4, sticky='new')

        self.btn_guardar_emprest.grid(column=2, row=1, sticky='sew', padx=4)
        self.btn_cancelar_emprest.grid(column=2, row=2, sticky='sew', padx=4)

        self.emprestimos_fr1.grid_columnconfigure(1, weight=1)

        self.emprestimos_fr2.grid_columnconfigure(0, weight=1)
        self.emprestimos_fr2.grid_rowconfigure(0, weight=1)

        self.emprestimos_fr3.grid_columnconfigure(0, weight=1)
        self.emprestimos_fr3.grid_columnconfigure(1, weight=1)
        self.emprestimos_fr3.grid_rowconfigure(0, weight=1)

        #self.emprestimos_fr4.grid_columnconfigure(0, weight=1)
        self.emprestimos_fr4.grid_columnconfigure(0, weight=1)
        self.emprestimos_fr4.grid_columnconfigure(1, weight=1)
        self.emprestimos_fr4.grid_columnconfigure(2, weight=0)

        self.emprestimos_fr4.grid_rowconfigure(0, weight=1)

        self.emprestimos_lblfr_pag.grid_columnconfigure(1, weight=1)
        self.emprestimos_lblfr_pag.grid_columnconfigure(2, weight=1)

        self.emprestimos_fr1.pack(side='top', expand=False, fill='x')
        self.emprestimos_fr2.pack(side='top', expand=True, fill='both')
        self.emprestimos_fr3.pack(side='top', expand=True, fill='both')
        #ttk.Separator(self.tab_emprestimos).pack(side='top', expand=False, fill='x', pady=10)
        self.emprestimos_fr4.pack(side='top', expand=False, fill='x')

    def desativar_campos(self):
        # Desativar todos os campos de texto para não permitir alterações. ----
        self.txt_numero_contacto.configure(state="disabled")
        self.txt_nome.configure(state="disabled")

        widgets = (self.ltxt_descr_equipamento,
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
            widgets = (self.ltxt_num_fatura_fornecedor,
                       self.ltxt_data_fatura_fornecedor,
                       self.ltxt_num_guia_rececao,
                       self.ltxt_data_entrada_stock,
                       self.ltxt_num_quebra_stock,
                       self.ltxt_nar)
            for widget in widgets:
                widget.disable()

    def on_btn_fechar(self, event):
        """ will test for some condition before closing, save if necessary and
            then call destroy()
        """
        window = event.widget.winfo_toplevel()
        window.destroy()

    def _on_btn_inserir_art_emprest(self):
        print("verificando se há artigo selecionado e se houver adicionando o artigo à tabela.")

    def _on_btn_ver_artigos_emprest(self):
        print("Abrindo a lista de artigos de empréstimos")

    def bind_tree_hist(self):
        self.tree_hist.bind('<<TreeviewSelect>>', self.selectItem_hist_popup)
        #self.tree_hist.bind('<Double-1>', lambda x: self.create_window_detalhe_rep(num_reparacao=self.reparacao_selecionada))
        self.tree_hist.bind("<Button-2>", self.popupMenu_hist)
        self.tree_hist.bind("<Button-3>", self.popupMenu_hist)
        self.update_idletasks()

    def unbind_tree_hist(self):
        self.tree_hist.bind('<<TreeviewSelect>>', None)
        self.tree_hist.bind('<Double-1>', None)
        self.tree_hist.bind("<Button-2>", None)
        self.tree_hist.bind("<Button-3>", None)
        self.update_idletasks()

    def selectItem_hist_popup(self, event):
        """ # Hacking moment: Uma função que junta duas funções, para assegurar a sequência...
        """
        self.selectItem_hist()
        self.popupMenu_hist(event)

    def popupMenu_hist(self, event):
        """action in event of button 3 on tree view"""
        # select row under mouse
        self.selectItem_hist()

        iid = self.tree_hist.identify_row(event.y)
        x, y = event.x_root, event.y_root
        if iid:
            if x != 0 and y != 0:
                # mouse pointer over item
                self.tree_hist.selection_set(iid)
                self.tree_hist.focus(iid)
                self.contextMenu.post(event.x_root, event.y_root)
                print("popupMenu_hist(): x,y = ", event.x_root, event.y_root)
            else:
                print("popupMenu_hist(): wrong values for event - x=0, y=0")
        else:
            print(iid)
            print("popupMenu_hist(): Else - No code here yet! (mouse not over item)")
            # mouse pointer not over item
            # occurs when items do not fill frame
            # no action required
            pass

    def selectItem_hist(self, *event):
        """
        Obter reparação selecionada (após clique de rato na linha correspondente)
        """
        curItem = self.tree_hist.focus()
        tree_linha = self.tree_hist.item(curItem)

        linha = tree_linha["values"][0]
        print("Detalhe_reparação > Histórico > Linha selecionada:", linha)
        #equipamento =  tree_linha["values"][2]
        #self.my_statusbar.set(f"{num_reparacao} • {equipamento}")
        #self.reparacao_selecionada = num_reparacao

    def alternar_cores(self, tree, inverso=False,
                       fundo1='grey98', fundo2='white'):
        if inverso == False:
            impar = True
        else:
            impar = False

        for i in tree.get_children():
            if impar == True:
                tree.item(i, tags=("par",))
                impar = False
            else:
                tree.item(i, tags=("impar",))
                impar = True

        tree.tag_configure('par', background=fundo1)
        tree.tag_configure('impar', background=fundo2)
        self.update_idletasks()

    def mostrar_painel_principal(self):
        self.note.pack(side='top', expand=True, fill='both')
        self.note.enable_traversal()

    def montar_rodape(self):
        # TODO - obter dados da base de dados
        txt_esquerda = "Criado por Victor Domingos em 12/05/2021 18:01."
        txt_direita = "Fechado por Victor Domingos em 13/05/2021 17:01."

        self.rodapeFont = tk.font.Font(family="Lucida Grande", size=9)
        self.rodapeTxtColor = "grey22"

        self.esquerda = ttk.Label(self.bottomframe, anchor='w', text=txt_esquerda,
                                  font=self.rodapeFont, foreground=self.rodapeTxtColor)
        self.direita = ttk.Label(self.bottomframe, anchor='e', text=txt_direita,
                                 font=self.rodapeFont, foreground=self.rodapeTxtColor)
        self.esquerda.pack(side="left")
        self.direita.pack(side="right")

    def configurar_frames_e_estilos(self):
        self.master.minsize(W_DETALHE_REP_MIN_WIDTH, W_DETALHE_REP_MIN_HEIGHT)
        self.master.maxsize(W_DETALHE_REP_MAX_WIDTH, W_DETALHE_REP_MAX_HEIGHT)
        # self.master.geometry(W_DETALHE_REP_GEOMETRIA)  # Se ativada esta
        # linha, deixa de atualizar as medidas da janela ao mudar de separador
        self.master.title(
            f"Reparação nº{self.num_reparacao} ({self.tipo_processo})")

        self.dicas = Pmw.Balloon(self.master, label_background='#f6f6f6',
                                 hull_highlightbackground='#b3b3b3',
                                 state='balloon',
                                 relmouse='both',
                                 yoffset=18,
                                 xoffset=-2,
                                 initwait=1300)

        self.mainframe = ttk.Frame(self.master)
        self.topframe = ttk.Frame(self.mainframe, padding="5 8 5 5")
        self.centerframe = ttk.Frame(self.mainframe)
        self.bottomframe = ttk.Frame(self.mainframe, padding="3 1 3 1")

        self.estilo = ttk.Style()
        self.estilo.configure("Panel_Title.TLabel", pady=10, foreground="grey25", font=(
            "Helvetica Neue", 18, "bold"))
        self.estilo.configure("Panel_Body.TLabel", font=("Lucida Grande", 11))
        self.estilo.configure("TMenubutton", font=("Lucida Grande", 11))
        self.estilo.configure('Reparacoes_Historico.Treeview', rowheight=42)
        self.estilo.configure('Reparacoes_Emprestimo.Treeview', rowheight=20)

        self.btnFont = tk.font.Font(family="Lucida Grande", size=10)
        self.btnTxtColor = "grey22"

    def composeFrames(self):
        self.topframe.pack(side=tk.TOP, fill=tk.X)
        self.centerframe.pack(side=tk.TOP, expand=True, fill=tk.BOTH)
        self.bottomframe.pack(side=tk.BOTTOM, fill=tk.X)
        self.mainframe.pack(side=tk.TOP, expand=True, fill=tk.BOTH)

    def inserir_dados_de_exemplo(self):
        for i in range(1, 36, 4):
            self.tree_hist.insert("", "end", text="", values=(str(i), textwrap.fill(
                "Cliente informou que já desativou Find My iPhone.", 45), "Em processamento", "Victor Domingos", "12/07/2021"))
            self.tree_hist.insert("", "end", text="", values=(str(i + 1), textwrap.fill(
                "Cliente aprovou orçamento.", 45), "Em processamento", "Victor Domingos", "12/07/2021"))
            self.tree_hist.insert("", "end", text="", values=(str(i + 2), textwrap.fill(
                "Cliente recusou o orçamento porque vai optar por comprar novo.", 45), "Em processamento", "Victor Domingos", "12/07/2021"))
            self.tree_hist.insert("", "end", text="", values=(str(i + 3), textwrap.fill(
                "Centro técnico informou que não é possível reparar pois já não há peças originais.", 45), "Em processamento", "Victor Domingos", "12/07/2021"))

        if self.is_rep_cliente:
            for i in range(1):
                self.tree_emprest.insert("", "end", text="", values=(
                    "1", "MN0234PO/A", "Equipamento de substituição a utilizar enquanto a reparação não fica concluída", "SF1325FVWt5654", "91"))
                self.tree_emprest.insert("", "end", text="", values=(
                    "100", "GHTGAFVABS56152", "Equipamentos genéricos de substituição", "", "231"))
                self.tree_emprest.insert("", "end", text="", values=(
                    "1", "GHTGAFVABS56152", "Outro equipamento de substituição", "351456789012345678901", "1"))

            self.ltxt_obs_estado_equipamentos_emprest.set(
                'Texto de exemplo para experimentar como sai na prática.\n Equipamento muito danificado!...')
            self.ltxt_acessorios_emprest.set(
                'Texto de exemplo para experimentar como sai na prática.\nIsto fica noutra linha...')
