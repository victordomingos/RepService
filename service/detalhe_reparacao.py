#!/usr/bin/env python3.6
# encoding: utf-8
"""
Este módulo é parte integrante da aplicação RepService, desenvolvida por
Victor Domingos e distribuída sob os termos da licença Creative Commons
Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)
"""
import tkinter as tk
from tkinter import ttk
from global_setup import *



class repairDetailWindow(ttk.Frame):
    """ Classe de base para a janela de detalhes de reparações """
    def __init__(self, master, num_reparacao, *args,**kwargs):
        super().__init__(master,*args,**kwargs)
        self.num_reparacao = num_reparacao
        self.master = master

        self.configurar_frames_e_estilos()
        self.montar_barra_de_ferramentas()
        self.montar_painel_principal()
        self.montar_rodape()
        self.composeFrames()


    def montar_barra_de_ferramentas(self):
        self.btn_reincidencia = ttk.Button(self.topframe, text="➕", width=6, command=None)
        self.lbl_reincidencia = ttk.Label(self.topframe, font=self.btnFont, foreground=self.btnTxtColor, text="Criar reincidência")
        
        self.btn_entregar = ttk.Button(self.topframe, text="➕", width=6, command=None)
        self.lbl_entregar = ttk.Label(self.topframe, font=self.btnFont, foreground=self.btnTxtColor, text="Entregar")
        
        
        
        
        # ----------- Botão com menu "Alterar estado" --------------
        self.label_mbtn_alterar = ttk.Label(self.topframe, font=self.btnFont, foreground=self.btnTxtColor, text="Alterar estado")
        self.mbtn_alterar = ttk.Menubutton (self.topframe, text="•••")
        self.mbtn_alterar.menu  =  tk.Menu (self.mbtn_alterar, tearoff=0)
        self.mbtn_alterar["menu"] =  self.mbtn_alterar.menu

        self.mbtn_alterar.menu.add_command(label=ESTADOS[EM_PROCESSAMENTO], command=None)
        self.mbtn_alterar.menu.add_command(label=ESTADOS[AGUARDA_ENVIO], command=None)
        self.mbtn_alterar.menu.add_command(label=ESTADOS[AGUARDA_RESP_FORNECEDOR], command=None)
        self.mbtn_alterar.menu.add_command(label=ESTADOS[AGUARDA_RESP_CLIENTE], command=None)
        self.mbtn_alterar.menu.add_command(label=ESTADOS[AGUARDA_RECECAO], command=None)
        self.mbtn_alterar.menu.add_command(label=ESTADOS[RECEBIDO], command=None)
        self.mbtn_alterar.menu.add_command(label=ESTADOS[DISPONIVEL_P_LEVANTAMENTO], command=None)
        self.mbtn_alterar.menu.add_separator()
        self.mbtn_alterar.menu.add_command(label=ESTADOS[ENTREGUE], command=None)
        self.mbtn_alterar.menu.add_separator()
        self.mbtn_alterar.menu.add_command(label=ESTADOS[ANULADO], command=None)
        self.mbtn_alterar.menu.add_command(label=ESTADOS[ABANDONADO], command=None)
        self.mbtn_alterar.menu.add_command(label=ESTADOS[SEM_INFORMACAO], command=None)
        # ----------- fim de Botão com menu "Alterar estado" -------------


        # ----------- Botão com menu "Alterar Prioridade" --------------
        self.label_mbtn_alterar = ttk.Label(self.topframe, font=self.btnFont, foreground=self.btnTxtColor, text="Alterar Prioridade")
        self.mbtn_alterar = ttk.Menubutton (self.topframe, text="•••")
        self.mbtn_alterar.menu  =  tk.Menu (self.mbtn_alterar, tearoff=0)
        self.mbtn_alterar["menu"] =  self.mbtn_alterar.menu

        self.mbtn_alterar.menu.add_command(label=ESTADOS[EM_PROCESSAMENTO], command=None)
        self.mbtn_alterar.menu.add_command(label=ESTADOS[AGUARDA_ENVIO], command=None)
        self.mbtn_alterar.menu.add_command(label=ESTADOS[AGUARDA_RESP_FORNECEDOR], command=None)
        self.mbtn_alterar.menu.add_command(label=ESTADOS[AGUARDA_RESP_CLIENTE], command=None)
        self.mbtn_alterar.menu.add_command(label=ESTADOS[AGUARDA_RECECAO], command=None)
        self.mbtn_alterar.menu.add_command(label=ESTADOS[RECEBIDO], command=None)
        self.mbtn_alterar.menu.add_command(label=ESTADOS[DISPONIVEL_P_LEVANTAMENTO], command=None)
        self.mbtn_alterar.menu.add_separator()
        self.mbtn_alterar.menu.add_command(label=ESTADOS[ENTREGUE], command=None)
        self.mbtn_alterar.menu.add_separator()
        self.mbtn_alterar.menu.add_command(label=ESTADOS[ANULADO], command=None)
        self.mbtn_alterar.menu.add_command(label=ESTADOS[ABANDONADO], command=None)
        self.mbtn_alterar.menu.add_command(label=ESTADOS[SEM_INFORMACAO], command=None)
        # ----------- fim de Botão com menu "Alterar Prioridade" -------------


        # ----------- Botão com menu "Copiar" --------------
        self.label_mbtn_alterar = ttk.Label(self.topframe, font=self.btnFont, foreground=self.btnTxtColor, text="Copiar")
        self.mbtn_alterar = ttk.Menubutton (self.topframe, text="•••")
        self.mbtn_alterar.menu  =  tk.Menu (self.mbtn_alterar, tearoff=0)
        self.mbtn_alterar["menu"] =  self.mbtn_alterar.menu

        self.mbtn_alterar.menu.add_command(label=ESTADOS[EM_PROCESSAMENTO], command=None)
        self.mbtn_alterar.menu.add_command(label=ESTADOS[AGUARDA_ENVIO], command=None)
        self.mbtn_alterar.menu.add_command(label=ESTADOS[AGUARDA_RESP_FORNECEDOR], command=None)
        self.mbtn_alterar.menu.add_command(label=ESTADOS[AGUARDA_RESP_CLIENTE], command=None)
        self.mbtn_alterar.menu.add_command(label=ESTADOS[AGUARDA_RECECAO], command=None)
        self.mbtn_alterar.menu.add_command(label=ESTADOS[RECEBIDO], command=None)
        self.mbtn_alterar.menu.add_command(label=ESTADOS[DISPONIVEL_P_LEVANTAMENTO], command=None)
        self.mbtn_alterar.menu.add_separator()
        self.mbtn_alterar.menu.add_command(label=ESTADOS[ENTREGUE], command=None)
        self.mbtn_alterar.menu.add_separator()
        self.mbtn_alterar.menu.add_command(label=ESTADOS[ANULADO], command=None)
        self.mbtn_alterar.menu.add_command(label=ESTADOS[ABANDONADO], command=None)
        self.mbtn_alterar.menu.add_command(label=ESTADOS[SEM_INFORMACAO], command=None)
        # ----------- fim de Botão com menu "Copiar" -------------
        

        # ----------- Botão com menu "Imprimir" --------------
        self.label_mbtn_alterar = ttk.Label(self.topframe, font=self.btnFont, foreground=self.btnTxtColor, text="Imprimir")
        self.mbtn_alterar = ttk.Menubutton (self.topframe, text="•••")
        self.mbtn_alterar.menu  =  tk.Menu (self.mbtn_alterar, tearoff=0)
        self.mbtn_alterar["menu"] =  self.mbtn_alterar.menu

        self.mbtn_alterar.menu.add_command(label=ESTADOS[EM_PROCESSAMENTO], command=None)
        self.mbtn_alterar.menu.add_command(label=ESTADOS[AGUARDA_ENVIO], command=None)
        self.mbtn_alterar.menu.add_command(label=ESTADOS[AGUARDA_RESP_FORNECEDOR], command=None)
        self.mbtn_alterar.menu.add_command(label=ESTADOS[AGUARDA_RESP_CLIENTE], command=None)
        self.mbtn_alterar.menu.add_command(label=ESTADOS[AGUARDA_RECECAO], command=None)
        self.mbtn_alterar.menu.add_command(label=ESTADOS[RECEBIDO], command=None)
        self.mbtn_alterar.menu.add_command(label=ESTADOS[DISPONIVEL_P_LEVANTAMENTO], command=None)
        self.mbtn_alterar.menu.add_separator()
        self.mbtn_alterar.menu.add_command(label=ESTADOS[ENTREGUE], command=None)
        self.mbtn_alterar.menu.add_separator()
        self.mbtn_alterar.menu.add_command(label=ESTADOS[ANULADO], command=None)
        self.mbtn_alterar.menu.add_command(label=ESTADOS[ABANDONADO], command=None)
        self.mbtn_alterar.menu.add_command(label=ESTADOS[SEM_INFORMACAO], command=None)
        # ----------- fim de Botão com menu "Imprimir" -------------




        self.btn_comunicacao = ttk.Button(self.topframe, text="➕", width=6, command=None)
        self.lbl_comunicacao = ttk.Label(self.topframe, font=self.btnFont, foreground=self.btnTxtColor, text="Comunicação")


        self.btn_reincidencia.grid(column=3, row=0)
        self.lbl_reincidencia.grid(column=3, row=1)
        self.btn_entregar.grid(column=4, row=0)
        self.lbl_entregar.grid(column=4, row=1)

        self.mbtn_alterar.grid(column=7, row=0)
        self.label_mbtn_alterar.grid(column=7, row=1)

        self.btn_comunicacao.grid(column=10, row=0)
        self.lbl_comunicacao.grid(column=10, row=1)



    def montar_painel_principal(self):
        print(f"A mostrar detalhes da reparação nº {self.num_reparacao}")
        self.note = ttk.Notebook(self.centerframe)

        self.tab_geral = ttk.Frame(self.note, padding=10)
        self.tab_historico = ttk.Frame(self.note, padding=10)
        self.tab_orcamentos = ttk.Frame(self.note, padding=10)
        self.tab_emprestimos = ttk.Frame(self.note, padding=10)


        self.note.add(self.tab_geral, text = "Geral", compound='top')
        self.note.add(self.tab_historico, text = "Histórico")
        self.note.add(self.tab_orcamentos, text = "Orçamentos")
        self.note.add(self.tab_emprestimos, text = "Empréstimos")


        # TAB Geral ~~~~~~~~~~~~~~~~

        #ttk.Label(self.tab_credito, text=" ").grid(column=1, row=0, sticky=E)

        """
        ttk.Label(self.tab_credito, text="Tipo:").grid(column=1, row=1, sticky=E)
        self.combo_tipo_documento_cred = ttk.Combobox(self.tab_credito, width=33, textvariable=self.tipo_documento_cred, values=TIPOS_DOCUMENTO, state='readonly')
        self.combo_tipo_documento_cred.grid(column=2, columnspan=2, row=1, sticky=W+E)
        self.combo_tipo_documento_cred.current(0)
        self.combo_tipo_documento_cred.bind("<<ComboboxSelected>>", self.tipo_cred_select)

        self.lbl_numero_cred = ttk.Label(self.tab_credito, text="Nº Fatura:")
        self.lbl_numero_cred.grid(column=1, row=2, sticky=E)
        self.text_input_numero_cred = ttk.Entry(self.tab_credito, width=15)
        self.text_input_numero_cred.grid(column=2, row=2, sticky=W)
        self.text_input_numero_cred.bind("<Return>", lambda x: self.text_input_nome_cred.focus_set())


        self.lbl_nome_cred = ttk.Label(self.tab_credito, text="Nome ou descrição:")
        self.lbl_nome_cred.grid(column=1,  row=3, sticky=E)
        self.text_input_nome_cred = AutocompleteEntry(self.tab_credito, width=37)
        #self.text_input_nome_cred.set_completion_list(self.lista_destinatarios)
        self.text_input_nome_cred.grid(column=2, columnspan=2, row=3, sticky=W+E)

        self.lbl_montante_cred = ttk.Label(self.tab_credito, text="Montante:")
        self.lbl_montante_cred.grid(column=1, row=4, sticky=E)
        self.text_input_montante_cred = ttk.Entry(self.tab_credito, width=15)
        self.text_input_montante_cred.grid(column=2, row=4, sticky=W)        


        self.lbl_meiopag_cred = ttk.Label(self.tab_credito, text="Meio de pagamento:")
        self.lbl_meiopag_cred.grid(column=1, row=5, sticky=E)
        self.combo_meio_pagamento_cred = ttk.Combobox(self.tab_credito, textvariable=self.meio_pagamento, values=MEIOS_PAGAMENTO, state='readonly')
        self.combo_meio_pagamento_cred.current(0)
        self.combo_meio_pagamento_cred.grid(column=2, columnspan=2, row=5, sticky=W+E)
        self.combo_meio_pagamento_cred.bind("<<ComboboxSelected>>", self.meio_pag_cred_select)

        self.lbl_detalhes_cred = ttk.Label(self.tab_credito, text="Detalhes adicionais:")  # (nº de cheque, nota de crédito abatida, etc.)
        self.lbl_detalhes_cred.grid(column=1, row=6, sticky=E)
        self.text_input_detalhes_cred = ttk.Entry(self.tab_credito, width=35)
        self.text_input_detalhes_cred.grid(column=2, columnspan=2, row=6, sticky=W+E)


        ttk.Label(self.tab_credito, text="  ").grid(column=4, row=2)

        self.btn_adicionar_cred = ttk.Button(self.tab_credito, text="Adicionar", width=7, command=self.add_credito)
        self.btn_adicionar_cred.grid(column=5, row=1)

        self.btn_limpar_cred = ttk.Button(self.tab_credito, text="Limpar", width=7, command=self.limpar_cred)
        self.btn_limpar_cred.grid(column=5, row=2)

             
        for col in range(6):
            self.bottomframe.columnconfigure(col, weight=1)
        """


        # TAB Histórico ~~~~~~~~~~~~~~~


        # TAB Orçamentos ~~~~~~~~~~~~~~~~~~~~~~~~~~~ TODO


        # TAB Empréstimos ~~~~~~~~~~~~~~~~~~~~        


        self.note.pack(side='top', expand=True, fill='both')
        self.note.enable_traversal() 



    def montar_rodape(self):
        pass



    def configurar_frames_e_estilos(self):
        self.master.minsize(W_DETALHE_REP_MIN_WIDTH, W_DETALHE_REP_MIN_HEIGHT)
        self.master.maxsize(W_DETALHE_REP_MAX_WIDTH, W_DETALHE_REP_MAX_HEIGHT)
        self.master.geometry(W_DETALHE_REP_GEOMETRIA)
        self.mainframe = ttk.Frame(self.master)
        self.topframe = ttk.Frame(self.mainframe, padding="5 8 5 5")
        self.centerframe = ttk.Frame(self.mainframe)
        self.bottomframe = ttk.Frame(self.mainframe)

        style_label = ttk.Style()
        style_label.configure("BW.TLabel", pady=10, foreground="grey25", font=("Helvetica Neue", 18, "bold"))

        self.btnFont = tk.font.Font(family="Lucida Grande", size=10)
        self.btnTxtColor = "grey22"


    def composeFrames(self):
        self.topframe.pack(side=tk.TOP, fill=tk.X)
        self.centerframe.pack(side=tk.TOP, fill=tk.BOTH)
        self.bottomframe.pack(side=tk.BOTTOM, fill=tk.X)
        self.mainframe.pack(side=tk.TOP, expand=True, fill=tk.BOTH)
