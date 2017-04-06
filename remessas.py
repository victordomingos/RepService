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


class RemessasWindow(baseApp):
    """ base class for application """
    def __init__(self, master, estado, *args,**kwargs):
        super().__init__(master,*args,**kwargs)
        self.estado = estado
        self.master.minsize(REMESSAS_MIN_WIDTH, REMESSAS_MIN_HEIGTH)
        self.master.maxsize(REMESSAS_MAX_WIDTH, REMESSAS_MAX_HEIGTH)
        #self.centerframe = ttk.Frame(self.mainframe, padding="4 0 4 0") #apagar isto
        self.montar_barra_de_ferramentas()
        self.montar_tabela()

        #get status bar
        self.nremessas = 2345
        self.my_statusbar.set(f"{self.nremessas} remessas")

        self.gerar_painel_entrada()

        self.composeFrames()
        self.inserir_dados_de_exemplo()
        self.alternar_cores(self.tree)
        if self.estado.painel_nova_remessa_aberto:
            self.mostrar_painel_entrada()


    def montar_tabela(self):
        self.tree = ttk.Treeview(self.leftframe, height=60, selectmode='browse')
        self.tree['columns'] = ('ID', 'Destino', 'Qtd.', 'Data')
        self.tree.pack(side=tk.TOP, fill=tk.BOTH)
        self.tree.column('#0', anchor=tk.W, minwidth=0, stretch=0, width=0)
        self.tree.column('ID', anchor=tk.E, minwidth=37, stretch=0, width=37)
        self.tree.column('Destino', minwidth=110, stretch=1, width=110)
        self.tree.column('Qtd.', anchor=tk.E, minwidth=40, stretch=0, width=40)
        self.tree.column('Data', anchor=tk.E, minwidth=90, stretch=0, width=90)

        self.configurarTree()
        self.leftframe.grid_columnconfigure(0, weight=1)
        self.leftframe.grid_rowconfigure(0, weight=1)


    def montar_barra_de_ferramentas(self):
        # Barra de ferramentas / botões -------------------------------------------------------------------------------

        self.btn_entrada = ttk.Button(self.topframe, text="Entrada", command=None)
        self.btn_entrada.grid(column=0, row=0)

        self.btn_saida = ttk.Button(self.topframe, text="Saída", command=None)
        self.btn_saida.grid(column=1, row=0)

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
        self.estado.painel_nova_remessa_aberto = True
        #self.MenuFicheiro.entryconfig("Novo contacto", state="disabled")
        #root.unbind_all("<Command-n>")
        self.show_entryform()


    def fechar_painel_entrada(self, *event):
        self.estado.painel_nova_remessa_aberto = False
        #self.clear_text()
        self.hide_entryform()
        #root.bind_all("<Command-n>")


    def gerar_painel_entrada(self):

        #entryfr1-----------------------------
        #TODO:adicionar campos, notebook, etc
        #criar funções para usar esses campos, ora para adicionar, ora para editar, ora para visualizar registos
        self.ef_var_tipo = tk.IntVar()
        self.ef_var_tipo.set(0)
        self.ef_var_destino = tk.IntVar()
        self.ef_var_destino.set("Centro técnico N")

        self.ef_cabecalho = ttk.Frame(self.entryfr1, padding=4)
        self.ef_lbl_titulo = ttk.Label(self.ef_cabecalho, style="BW.TLabel", text="Adicionar Remessa:\n")
        self.ef_lbl_tipo = ttk.Label(self.ef_cabecalho, text="Tipo:")
        self.ef_radio_tipo_saida = ttk.Radiobutton(self.ef_cabecalho, text="Saída", variable=self.ef_var_tipo, value=TIPO_REMESSA_SAIDA, command=self.radio_tipo_command)
        self.ef_radio_tipo_entrada = ttk.Radiobutton(self.ef_cabecalho, text="Entrada", variable=self.ef_var_tipo, value=TIPO_REMESSA_ENTRADA, command=self.radio_tipo_command)
        self.btn_adicionar = ttk.Button(self.ef_cabecalho, text="Adicionar", command=None)
        self.btn_cancelar = ttk.Button(self.ef_cabecalho, text="Cancelar", command=self.fechar_painel_entrada)


        self.ef_lbl_titulo.grid(column=0, row=0, columnspan=3, sticky="w")
        self.ef_lbl_tipo.grid(column=0, row=1, sticky="e")
        self.ef_radio_tipo_saida.grid(column=1, row=1, sticky="w")
        self.ef_radio_tipo_entrada.grid(column=2, row=1, sticky="w")
        self.btn_adicionar.grid(column=3, row=1, sticky="we")
        self.btn_cancelar.grid(column=3, row=2, sticky="we")

        self.ef_cabecalho.grid(column=0,row=0, sticky='we')
        self.entryfr1.columnconfigure(0, weight=1)
        self.ef_cabecalho.columnconfigure(0, weight=0) 
        self.ef_cabecalho.columnconfigure(2, weight=1)

        # self.btn_adicionar.bind('<Button-1>', self.add_remessa)

        #entryfr2-----------------------------
        self.ef_lbl_destino = ttk.Label(self.entryfr2, width=27, text="Destino:")
        self.ef_combo_destino = ttk.Combobox(self.entryfr2,
                                             width=21,
                                             textvariable=self.ef_var_destino,
                                             values=("Loja X",
                                                     "Importador Nacional A",
                                                     "Distribuidor Ibérico Y",
                                                     "Centro de assistência N",
                                                     "Centro de assistência P",
                                                     "Centro de assistência K"),
                                             state='readonly')  # TODO: Obter estes valores a partir da base de dados, a utilizar também no formulário de Remessas.
        self.ef_lbl_destino.grid(column=0, row=0, padx=5, sticky='we')
        self.ef_combo_destino.grid(column=0, row=1, padx=5, sticky='we')

        # Entryfr3
        self.ef_lbl_num_rep = ttk.Label(self.entryfr3, text="\nNº reparação:")
        self.ef_txt_num_reparacao = ttk.Entry(self.entryfr3, width=10)
        self.ef_btn_adicionar_rep = ttk.Button(self.entryfr3, text="Inserir")
        self.ef_btn_selecionar_rep = ttk.Button(self.entryfr3, text="Selecionar...")  # TODO: substituir por combobox a ir buscar à base de dados os processos a aguardar envio?

        self.ef_lbl_num_rep.grid(column=0, row=0, padx=5, sticky='w')
        self.ef_txt_num_reparacao.grid(column=0, row=1, padx=5, sticky='w')
        self.ef_btn_adicionar_rep.grid(column=1, row=1, padx=5, sticky='w')
        self.ef_btn_selecionar_rep.grid(column=2, row=1,  padx=5, sticky='w')

        #  treeview entryfr4: Rep nº | Equip. | S/N

        # Rodapé entryfr5: Num. processos "a enviar" (tipo:saída)/ "recebidos" (tipo:Entrada): XXXXX (contar linhas treeview)

        #--- acabaram os 'entryfr', apenas código geral para o entryframe a partir daqui ---
        #self.entryframe.bind_all("<Command-Escape>", self.fechar_painel_entrada)


    def radio_tipo_command(self, *event):
        """
        Ajustes que devem ocorrer no formulário quando o utilizador altera o
        tipo de remessa.
        """
        pass


    def liga_desliga_menu_novo(self, *event):
        """
        Liga e desliga menus com base na configuração atual da janela. Por exemplo, ao
        abrir o painel de entrada de dados, desativa o menu "nova reparação", para evitar
        que o painel se feche inadvertidamente.
        """
        if self.is_entryform_visible == True:
            self.MenuFicheiro.entryconfigure("Nova remessa", state="disabled")
            # TODO - corrigir bug: o atalho de teclado só fica realmente inativo depois de acedermos ao menu ficheiro. Porquê??
            #root.unbind_all("<Command-Option-n>")
        else:
            self.MenuFicheiro.entryconfigure("Nova remessa", state="active")
            #root.bind_all("<Command-Option-n>")


    def inserir_dados_de_exemplo(self):
        for i in range(2560):
            self.tree.insert("", "end", text="", values=(str(i),"Fornecedor", "3", "2017-12-31"))
            self.tree.insert("", "end", text="", values=(str(i),"Centro técnico", "10", "2017-01-12"))
            self.tree.insert("", "end", text="", values=(str(i),"Distribuidor internacional", "10", "2017-02-01"))
