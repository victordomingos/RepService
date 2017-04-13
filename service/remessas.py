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
        self.tree['columns'] = ('ID', 'Origem', 'Destino', 'Qtd.', 'Data')
        self.tree.pack(side=tk.TOP, fill=tk.BOTH)
        self.tree.column('#0', anchor=tk.W, minwidth=0, stretch=0, width=0)
        self.tree.column('ID', anchor=tk.E, minwidth=37, stretch=0, width=37)
        self.tree.column('Origem', minwidth=60, stretch=1, width=60)
        self.tree.column('Destino', minwidth=60, stretch=1, width=60)
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
        self.str_num_processos = tk.StringVar()
        self.num_processos = 0
        self.str_num_processos.set(f"Número de processos a enviar: {self.num_processos}")
        self.ef_var_reparacoes_a_enviar = tk.IntVar()
        self.ef_var_reparacoes_a_enviar.set("Selecionar reparações...")

        self.ef_var_destino.set("Centro técnico N")

        self.ef_cabecalho = ttk.Frame(self.entryfr1, padding=4)
        self.ef_lbl_titulo = ttk.Label(self.ef_cabecalho, style="BW.TLabel", text="Adicionar Remessa:\n")
        self.ef_lbl_tipo = ttk.Label(self.ef_cabecalho, text="Tipo:")
        self.ef_radio_tipo_saida = ttk.Radiobutton(self.ef_cabecalho, text="Envio", variable=self.ef_var_tipo, value=TIPO_REMESSA_ENVIO, command=self.radio_tipo_command)
        self.ef_radio_tipo_entrada = ttk.Radiobutton(self.ef_cabecalho, text="Receção", variable=self.ef_var_tipo, value=TIPO_REMESSA_RECECAO, command=self.radio_tipo_command)
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
        self.ef_lbl_num_rep = ttk.Label(self.entryfr3, text="\nNº rep.:")
        self.ef_txt_num_reparacao = ttk.Entry(self.entryfr3, width=7)
        self.ef_btn_adicionar_rep = ttk.Button(self.entryfr3, text="Inserir")

        # TODO:Ir buscar à base de dados os processos a aguardar envio/receção?
        # Atualizar lista quando um dos processos é selecionado e quando é alterado o tipo de remessa.
        self.ef_combo_selecionar_rep = ttk.Combobox(self.entryfr3,
                                                    textvariable=self.ef_var_reparacoes_a_enviar,
                                                    values=("12234 - iPhone 7 128GB Space grey - José manuel da Silva Castro",
                                                            "85738 - MacBook Pro 15\" Retina - Manuel José de Castro Silva",
                                                            "32738 - iPod shuffle 2GB - Laranjas e Limões, Lda.",
                                                            "25720 - Beats X - NPK - Network Project for Knowledge",
                                                            "85738 - MacBook Pro 15\" Retina - Manuel José de Castro Silva",
                                                            "32738 - iPod shuffle 2GB - Laranjas e Limões, Lda.",
                                                            "25720 - Beats X - NPK - Network Project for Knowledge",
                                                            "85738 - MacBook Pro 15\" Retina - Manuel José de Castro Silva",
                                                            "32738 - iPod shuffle 2GB - Laranjas e Limões, Lda.",
                                                            "25720 - Beats X - NPK - Network Project for Knowledge",
                                                            "85738 - MacBook Pro 15\" Retina - Manuel José de Castro Silva",
                                                            "32738 - iPod shuffle 2GB - Laranjas e Limões, Lda.",
                                                            "25720 - Beats X - NPK - Network Project for Knowledge",
                                                            ),
                                                    state='readonly')


        self.ef_lbl_num_rep.grid(column=0, row=0, padx=5, sticky='we')
        self.ef_txt_num_reparacao.grid(column=0, row=1, padx=5, sticky='we')
        self.ef_btn_adicionar_rep.grid(column=1, row=1, padx=5, sticky='w')
        self.ef_combo_selecionar_rep.grid(column=2, row=1,  padx=5, sticky='we')
        self.entryfr3.grid_columnconfigure(0, weight=0)
        self.entryfr3.grid_columnconfigure(1, weight=0)
        self.entryfr3.grid_columnconfigure(2, weight=1)



        #  treeview entryfr4:
        self.ef_lista = ttk.Frame(self.entryfr4, padding=4)
        self.tree_lista_processos_remessa = ttk.Treeview(self.ef_lista, height=15, selectmode='browse')
        self.tree_lista_processos_remessa['columns'] = ('Nº', 'Equipamento', 'S/N')
        self.tree_lista_processos_remessa.pack(side=tk.TOP, expand=True, fill='both')
        self.tree_lista_processos_remessa.column('#0', anchor=tk.W, minwidth=0, stretch=0, width=0)
        self.tree_lista_processos_remessa.column('Nº', anchor=tk.E, minwidth=46, stretch=0, width=46)
        self.tree_lista_processos_remessa.column('Equipamento', minwidth=180, stretch=1, width=180)
        self.tree_lista_processos_remessa.column('S/N', anchor=tk.E, minwidth=140, stretch=0, width=140)
        self.configurarTree_lista_processos_remessa()
        self.ef_lista.grid(column=0, row=0, sticky='we')
        self.ef_lista.grid_columnconfigure(0, weight=1)
        self.entryfr4.grid_columnconfigure(0, weight=1)
        self.entryfr4.grid_rowconfigure(0, weight=1)
        self.configurarTree_lista_processos_remessa()

        # Rodapé entryfr5: Num. processos "a enviar" (tipo:saída)/ "recebidos" (tipo:Entrada): XXXXX (contar linhas treeview)
        self.lbl_num_processos = ttk.Label(self.entryfr5, textvariable=self.str_num_processos)
        self.lbl_num_processos.pack()

        #--- acabaram os 'entryfr', apenas código geral para o entryframe a partir daqui ---
        #self.entryframe.bind_all("<Command-Escape>", self.fechar_painel_entrada)

    def configurarTree_lista_processos_remessa(self):
        # Ordenar por coluna ao clicar no respetivo cabeçalho
        for col in self.tree_lista_processos_remessa['columns']:
            self.tree_lista_processos_remessa.heading(col, text=col.title(),
            command=lambda c=col: self.sortBy(self.tree_lista_processos_remessa, c, 0))

        # Barra de deslocação para a tabela
        self.tree_lista_processos_remessa.grid(column=0, row=0, sticky=tk.N+tk.W+tk.E, in_=self.ef_lista)
        self.vsb_lista = AutoScrollbar(self.ef_lista, orient="vertical", command=self.tree_lista_processos_remessa.yview)
        self.tree_lista_processos_remessa.configure(yscrollcommand=self.vsb_lista.set)
        self.vsb_lista.grid(column=1, row=0, sticky=tk.N+tk.S, in_=self.ef_lista)


    def radio_tipo_command(self, *event):
        """
        Ajustes que devem ocorrer no formulário quando o utilizador altera o
        tipo de remessa.
        """
        tipo = self.ef_var_tipo.get()
        if tipo == TIPO_REMESSA_RECECAO:
            self.ef_lbl_destino.configure(text="Origem:")
            self.str_num_processos.set(f"Número de processos a receber: {self.num_processos}")
        else:
            self.ef_lbl_destino.configure(text="Destino:")
            self.str_num_processos.set(f"Número de processos a enviar: {self.num_processos}")


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
            self.tree.insert("", "end", text="", values=(str(i), "Loja X", "Fornecedor", "3", "2017-12-31"))
            self.tree.insert("", "end", text="", values=(str(i), "Centro técnico", "Loja X", "10", "2017-01-12"))
            self.tree.insert("", "end", text="", values=(str(i), "Loja X", "Distribuidor internacional", "10", "2017-02-01"))
