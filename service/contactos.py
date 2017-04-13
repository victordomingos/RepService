#!/usr/bin/env python3.6
# encoding: utf-8
"""
Este módulo é parte integrante da aplicação RepService, desenvolvida por
Victor Domingos e distribuída sob os termos da licença Creative Commons
Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)
"""

import tkinter as tk
from tkinter import ttk
from extra_tk_classes import *
from base_app import *
from service import *


class ContactsWindow(baseApp):
    """ base class for application """
    def __init__(self, master, estado, *args, **kwargs):
        super().__init__(master,*args,**kwargs)
        self.estado = estado
        self.master.minsize(CONTACTOS_MIN_WIDTH, CONTACTOS_MIN_HEIGTH)
        self.master.maxsize(CONTACTOS_MAX_WIDTH, CONTACTOS_MAX_HEIGTH)
        #self.centerframe = ttk.Frame(self.mainframe, padding="4 0 4 0")  #apagar isto
        self.montar_barra_de_ferramentas()
        self.montar_tabela()

        #get status bar
        self.ncontactos = 2345
        self.my_statusbar.set(f"{self.ncontactos} contactos")

        self.gerar_painel_entrada()
        self.composeFrames()
        self.inserir_dados_de_exemplo()
        self.alternar_cores(self.tree)
        if self.estado.painel_novo_contacto_aberto:
            self.mostrar_painel_entrada()


    def montar_tabela(self):
        self.tree = ttk.Treeview(self.leftframe, height=60, selectmode='browse')
        self.tree['columns'] = ('ID', 'Nome', 'Telefone','Email')
        self.tree.pack(side=tk.TOP, fill=tk.BOTH)
        self.tree.column('#0', anchor=tk.W, minwidth=0, stretch=0, width=0)
        self.tree.column('ID', anchor=tk.E, minwidth=37, stretch=0, width=37)
        self.tree.column('Nome', minwidth=140, stretch=1, width=140)
        self.tree.column('Telefone', anchor=tk.E, minwidth=90, stretch=1, width=90)
        self.tree.column('Email', anchor=tk.E, minwidth=130, stretch=1, width=130)

        self.configurarTree()

        self.leftframe.grid_columnconfigure(0, weight=1)
        self.leftframe.grid_rowconfigure(0, weight=1)


    def montar_barra_de_ferramentas(self):
        self.btn_clientes = ttk.Button(self.topframe, text="Clientes", command=None)
        self.btn_clientes.grid(column=0, row=0)

        self.btn_fornecedores = ttk.Button(self.topframe, text="Fornecedores", command=None)
        self.btn_fornecedores.grid(column=1, row=0)

        self.btn_add = ttk.Button(self.topframe, text=" ➕", width=3, command=self.show_entryform)
        self.btn_add.grid(column=3, row=0)

        self.text_input_pesquisa = ttk.Entry(self.topframe, width=12)
        self.text_input_pesquisa.grid(column=4, row=0)

        #letras_etc = ascii_letters + "01234567890-., "
        #for char in letras_etc:
        #    keystr = '<KeyRelease-' + char + '>'
        #    self.text_input_pesquisa.bind(keystr, self.ativar_pesquisa)
        #self.text_input_pesquisa.bind('<Button-1>', self.clique_a_pesquisar)
        #self.text_input_pesquisa.bind('<KeyRelease-Escape>', self.cancelar_pesquisa)
        #self.text_input_pesquisa.bind('<KeyRelease-Mod2-a>', self.text_input_pesquisa.select_range(0, END))

        for col in range(1,4):
            self.topframe.columnconfigure(col, weight=0)
        self.topframe.columnconfigure(2, weight=1)


    def mostrar_painel_entrada(self, *event):
        self.estado.painel_novo_contacto_aberto = True
        #self.MenuFicheiro.entryconfig("Novo contacto", state="disabled")
        #root.unbind_all("<Command-t>")
        self.show_entryform()
        self.ef_ltxt_nome.entry.focus()


    def fechar_painel_entrada(self, *event):
        self.estado.painel_novo_contacto_aberto = False
        #self.clear_text()
        self.hide_entryform()
        #root.bind_all("<Command-n>")


    def gerar_painel_entrada(self):

        #entryfr1-----------------------------
        #TODO:adicionar campos, notebook, etc
        #criar funções para usar esses campos, ora para adicionar, ora para editar, ora para visualizar registos

        self.ef_var_tipo_is_cliente = tk.IntVar()
        self.ef_var_tipo_is_cliente.set(True)
        self.ef_var_tipo_is_fornecedor = tk.IntVar()
        if self.estado.tipo_novo_contacto == "Fornecedor":
            self.ef_var_tipo_is_fornecedor.set(True)
            self.ef_var_tipo_is_cliente.set(False)
        self.ef_var_tipo_is_loja = tk.IntVar()

        self.ef_cabecalho = ttk.Frame(self.entryfr1, padding=4)
        self.ef_lbl_titulo = ttk.Label(self.ef_cabecalho, style="BW.TLabel", text="Adicionar Contacto:\n")
        self.ef_lbl_tipo = ttk.Label(self.ef_cabecalho, text="Tipo:")

        self.ef_chkbtn_tipo_cliente = ttk.Checkbutton(self.ef_cabecalho, text="Cliente", variable=self.ef_var_tipo_is_cliente)
        self.ef_chkbtn_tipo_fornecedor = ttk.Checkbutton(self.ef_cabecalho, text="Fornecedor ou centro técnico", variable=self.ef_var_tipo_is_fornecedor)
        self.ef_chkbtn_tipo_loja = ttk.Checkbutton(self.ef_cabecalho, text="Loja do nosso grupo", variable=self.ef_var_tipo_is_loja)

        self.btn_adicionar = ttk.Button(self.ef_cabecalho, text="Adicionar", command=self.adicionar_contacto)
        self.btn_cancelar = ttk.Button(self.ef_cabecalho, text="Cancelar", command=self.fechar_painel_entrada)


        self.ef_lbl_titulo.grid(column=0, row=0, columnspan=3, sticky='w')
        self.ef_lbl_tipo.grid(column=0, row=1, sticky='e')
        self.ef_chkbtn_tipo_cliente.grid(column=1, row=1, sticky='w')
        self.ef_chkbtn_tipo_fornecedor.grid(column=1, row=2, sticky='w')
        self.ef_chkbtn_tipo_loja.grid(column=1, row=3, sticky='w')

        self.btn_adicionar.grid(column=3, row=1, sticky='we')
        self.btn_cancelar.grid(column=3, row=2, sticky='we')

        self.ef_cabecalho.grid(column=0,row=0, sticky='we')
        self.entryfr1.columnconfigure(0, weight=1)
        self.ef_cabecalho.columnconfigure(2, weight=1)

        #self.btn_adicionar.bind('<Button-1>', self.add_remessa)


        #entryfr2-----------------------------
        self.ef_lf_top = ttk.Labelframe(self.entryfr2, padding=4, text="")
        self.ef_ltxt_nome = LabelEntry(self.ef_lf_top, "Nome")
        self.ef_ltxt_empresa = LabelEntry(self.ef_lf_top, "Empresa")
        self.ef_ltxt_nif = LabelEntry(self.ef_lf_top, "NIF")
        self.ef_ltxt_telefone = LabelEntry(self.ef_lf_top, "\nTel.", width=14)
        self.ef_ltxt_tlm = LabelEntry(self.ef_lf_top, "\nTlm.", width=14)
        self.ef_ltxt_tel_empresa = LabelEntry(self.ef_lf_top, "\nTel. empresa", width=14)

        self.ef_ltxt_email = LabelEntry(self.ef_lf_top, "Email")
        self.ef_lstxt_morada = LabelText(self.ef_lf_top, "\nMorada", height=2)

        self.ef_ltxt_cod_postal = LabelEntry(self.ef_lf_top, "Código Postal")
        self.ef_ltxt_localidade = LabelEntry(self.ef_lf_top, "Localidade")

        self.ef_lbl_pais = ttk.Label(self.ef_lf_top, text="País")
        with open(f"{APP_PATH}/paises.txt", 'r', encoding='utf-8') as f:
            linhas = f.readlines()
        self.paises = [linha.strip() for linha in linhas]
        self.paises_value = tk.StringVar()

        self.ef_combo_pais = ttk.Combobox(self.ef_lf_top, textvariable=self.paises_value, state='readonly')
        self.ef_combo_pais['values'] = self.paises
        self.ef_combo_pais.current(178)
        self.ef_combo_pais.bind("<Key>", self.procurar_em_combobox)

        self.ef_lstxt_notas = LabelText(self.ef_lf_top, "\nNotas:", height=3)

        self.ef_ltxt_nome.grid(column=0, row=0, columnspan=3, padx=5, sticky='we')
        self.ef_ltxt_empresa.grid(column=0, row=1, columnspan=2, padx=5, sticky='we')
        self.ef_ltxt_nif.grid(column=2, row=1, padx=5, sticky='we')

        self.ef_ltxt_telefone.grid(column=0, row=2, padx=5, sticky='we')
        self.ef_ltxt_tlm.grid(column=1, row=2, padx=5, sticky='we')
        self.ef_ltxt_tel_empresa.grid(column=2, row=2, padx=5, sticky='we')
        self.ef_ltxt_email.grid(column=0, row=3, columnspan=3, padx=5, sticky='we')
        self.ef_lstxt_morada.grid(column=0, row=4, columnspan=3, rowspan=2, padx=5, sticky='we')

        self.ef_ltxt_cod_postal.grid(column=0, row=6, padx=5, sticky='we')
        self.ef_ltxt_localidade.grid(column=1, row=6, columnspan=2, padx=5, sticky='we')

        self.ef_lbl_pais.grid(column=0, columnspan=3, row=7, padx=5, sticky='we')
        self.ef_combo_pais.grid(column=0, columnspan=3, row=8, padx=5, sticky='we')
        self.ef_lstxt_notas.grid(column=0, row=9, columnspan=3, rowspan=4, padx=5, sticky='we')

        self.ef_lf_top.grid(column=0,row=0, sticky='we')
        self.ef_lf_top.columnconfigure(0, weight=1)
        self.ef_lf_top.columnconfigure(1, weight=1)
        self.ef_lf_top.columnconfigure(2, weight=1)
        self.entryfr2.columnconfigure(0, weight=1)


        #--- acabaram os 'entryfr', apenas código geral para o entryframe a partir daqui ---
        self.entryframe.bind_all("<Command-Escape>", self.fechar_painel_entrada)

    def procurar_em_combobox(self, event):
        """
        Saltar para o primeiro país da lista (combobox) começado pela letra
        correspondente à tecla pressionada.
        """
        tecla_pressionada = event.char.upper()
        if tecla_pressionada in ascii_uppercase:
            for index, pais in enumerate(self.paises):
                if pais[0] == tecla_pressionada:
                    self.ef_combo_pais.current(index)
                    break


    def adicionar_contacto(self, *event):
        """
        Guarda o contacto acabado de criar. Caso o utilizador esteja a criar uma
        reparação, adiciona o contacto ao campo correspondente.
        """
        # guardar na base de dados e obter o nº do último contacto adicionado

        if self.estado.tipo_novo_contacto == "Cliente":
            print("Usar este cliente")
            self.estado.contacto_para_nova_reparacao = "123"
            self.estado.janela_principal.close_window_contactos()
            pass  # preencher o campo do nº de cliente com o último contacto de cliente criado; depois atribuir foco ao formulário da reparação e fechar a janela
        elif self.estado.tipo_novo_contacto == "Fornecedor":
            print("Usar este fornecedor")
            self.estado.janela_principal.close_window_contactos()
            pass  # preencher o campo do nº de fornecedor com o último contacto de fornecedor criado; depois atribuir foco ao formulário da reparação e fechar a janela
        else:
            print("guardar e nao fazer mais nada")
            pass  # atualizar a lista de contactos nesta janela fechar o formulário


    def liga_desliga_menu_novo(self, *event):
        """
        Liga e desliga menus com base na configuração atual da janela. Por exemplo, ao
        abrir o painel de entrada de dados, desativa o menu "nova reparação", para evitar
        que o painel se feche inadvertidamente.
        """
        if self.is_entryform_visible:
            self.MenuFicheiro.entryconfigure("Novo contacto", state="disabled")
            # TODO - corrigir bug: o atalho de teclado só fica realmente inativo depois de acedermos ao menu ficheiro. Porquê??
            #root.unbind_all("<Command-Option-n>")
        else:
            self.MenuFicheiro.entryconfigure("Novo contacto", state="active")
            #root.bind_all("<Command-Option-n>")


    def inserir_dados_de_exemplo(self):
        for i in range(560):
            self.tree.insert("", "end", text="", values=(str(i),"Nome do cliente", "+351000000000", "endereco@emaildocliente.com"))
