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


class contactDetailWindow(ttk.Frame):
    """ Classe de base para a janela de detalhes de reparações """
    def __init__(self, master, num_contacto, *args,**kwargs):
        super().__init__(master,*args,**kwargs)
        self.master = master
        self.master.bind("<Command-w>", self.on_btn_fechar)
        self.master.focus()
        self.num_contacto = num_contacto

        self.var_tipo_is_cliente = tk.IntVar()
        self.var_tipo_is_loja = tk.IntVar()
        self.var_tipo_is_fornecedor = tk.IntVar()
        
        
        
        self.nome = "Nome do contacto"
        self.empresa = ""
        self.nif = "999999990"
        self.telefone = "253000000"
        self.tlm = "900000000"
        self.telef_empresa = "253000000"
        self.email = "TestContact@NetworkProjectForKnowledge.org"
        self.morada = "Rua Imaginária do Código sem Bugs, ∞, 2002º Esquerdo-e-Meio\nUrbanização da Consola Negra"
        self.cod_postal = "0101-101"
        self.localidade = "Vila Nova de Milcódigos-Fonte"
        self.pais = "Portugal"
        
        self.notas = "Alguns apontamentos adicionais sobre este contacto.\nEtc."
        
        
        
        self.var_tipo_is_cliente.set(True)  # Todo
        self.var_tipo_is_fornecedor.set(True)  # TODO
        self.var_tipo_is_loja.set(False)  # TODO







        self.configurar_frames_e_estilos()
        self.montar_barra_de_ferramentas()
        self.gerar_painel_principal()
        self.mostrar_painel_principal()

        self.montar_rodape()
        self.composeFrames()


    def montar_barra_de_ferramentas(self):
        self.lbl_titulo = ttk.Label(self.topframe, style="Panel_Title.TLabel", foreground=self.btnTxtColor, text=f"Contacto nº {self.num_contacto}")

        # ----------- Botão com menu "Copiar" --------------
        self.mbtn_copiar = ttk.Menubutton(self.topframe, text=" ⚡")
        self.mbtn_copiar.menu = tk.Menu(self.mbtn_copiar, tearoff=0)
        self.mbtn_copiar["menu"] = self.mbtn_copiar.menu
        self.mbtn_copiar.menu.add_command(label="Nome", command=None)
        self.mbtn_copiar.menu.add_command(label="NIF", command=None)
        self.mbtn_copiar.menu.add_command(label="Morada", command=None)
        self.mbtn_copiar.menu.add_command(label="Código Postal", command=None)
        self.mbtn_copiar.menu.add_command(label="Localidade", command=None)
        self.mbtn_copiar.menu.add_command(label="Email", command=None)
        self.mbtn_copiar.menu.add_command(label="Telefone", command=None)
        self.dicas.bind(self.mbtn_copiar, 'Clique para selecionar e copiar\ndados referentes a este contacto\npara a Área de Transferência.')
        # ----------- fim de Botão com menu "Copiar" -------------

        self.btn_nova_rep = ttk.Button(self.topframe, text="Criar reparação", style="secondary.TButton", command=None)
        self.dicas.bind(self.btn_nova_rep, 'Criar um novo processo de reparação.')

        self.btn_guardar_alteracoes = ttk.Button(self.topframe, text="Guardar", style="secondary.TButton", command=None)
        self.dicas.bind(self.btn_guardar_alteracoes, 'Clique para guardar quaisquer alterações\nefetuadas a esta ficha de contacto.')

        self.lbl_titulo.grid(column=0, row=0, rowspan=2)
        self.mbtn_copiar.grid(column=7, row=0)
        self.btn_nova_rep.grid(column=8, row=0)
        self.btn_guardar_alteracoes.grid(column=9, row=0)

        self.topframe.grid_columnconfigure(2, weight=1)


    def gerar_painel_principal(self):
        print(f"A mostrar detalhes da reparação nº {self.num_contacto}")

        # Preparar o notebook da secção principal ------------------------
        self.note = ttk.Notebook(self.centerframe, padding="3 20 3 3")
        self.tab_geral = ttk.Frame(self.note, padding=10)
        self.tab_morada = ttk.Frame(self.note, padding=10)
        self.tab_notas = ttk.Frame(self.note, padding=10)
        self.note.add(self.tab_geral, text="Contactos")
        self.note.add(self.tab_morada, text="Morada")
        self.note.add(self.tab_notas, text="Notas")
        self.gerar_tab_geral()
        self.montar_tab_geral()
        self.gerar_tab_morada()
        self.montar_tab_morada()
        self.gerar_tab_notas()
        self.montar_tab_notas()

        if self.var_tipo_is_cliente.get():
            self.tab_reparacoes = ttk.Frame(self.note, padding=10)
            self.note.add(self.tab_reparacoes, text="Reparações")
            self.gerar_tab_reparacoes()
            self.montar_tab_reparacoes()

        self.desativar_campos()


    def gerar_tab_geral(self):
        # TAB Geral ~~~~~~~~~~~~~~~~
        self.geral_fr1 = ttk.Frame(self.tab_geral)
        #self.geral_fr2 = ttk.Frame(self.tab_geral)

        # TODO - obter valor da base de dados
        # Criar widgets para este separador -------------------------------------------------------
        #self.txt_numero_contacto = ttk.Entry(self.geral_fr1, font=("Helvetica-Neue", 12), width=5)
        #self.txt_nome = ttk.Entry(self.geral_fr1, font=("Helvetica-Neue", 12), width=35)



        #entryfr2-----------------------------
        self.ef_ltxt_nome = LabelEntry(self.geral_fr1, "Nome", style="Panel_Body.TLabel")
        self.ef_ltxt_empresa = LabelEntry(self.geral_fr1, "Empresa", style="Panel_Body.TLabel")
        self.ef_ltxt_nif = LabelEntry(self.geral_fr1, "NIF", style="Panel_Body.TLabel")
        self.ef_ltxt_telefone = LabelEntry(self.geral_fr1, "\nTel.", width=14, style="Panel_Body.TLabel")
        self.ef_ltxt_tlm = LabelEntry(self.geral_fr1, "\nTlm.", width=14, style="Panel_Body.TLabel")
        self.ef_ltxt_tel_empresa = LabelEntry(self.geral_fr1, "\nTel. empresa", width=14, style="Panel_Body.TLabel")

        self.ef_ltxt_email = LabelEntry(self.geral_fr1, "Email", style="Panel_Body.TLabel")

        # Preencher com dados da base de dados -------------------------------------------------
        self.ef_ltxt_nome.set(self.nome)
        #TODO - preencher o resto dos campos do formulário...
        

    def montar_tab_geral(self):
        # Montar todos os campos na grid -------------------------------------------------------------
        self.ef_ltxt_nome.grid(column=0, row=0, columnspan=3, padx=5, sticky='we')
        self.ef_ltxt_empresa.grid(column=0, row=1, columnspan=2, padx=5, sticky='we')
        self.ef_ltxt_nif.grid(column=2, row=1, padx=5, sticky='we')

        self.ef_ltxt_telefone.grid(column=0, row=2, padx=5, sticky='we')
        self.ef_ltxt_tlm.grid(column=1, row=2, padx=5, sticky='we')
        self.ef_ltxt_tel_empresa.grid(column=2, row=2, padx=5, sticky='we')
        self.ef_ltxt_email.grid(column=0, row=3, columnspan=3, padx=5, sticky='we')

        self.geral_fr1.grid_columnconfigure(0, weight=1)
        self.geral_fr1.grid_columnconfigure(1, weight=1)
        self.geral_fr1.grid_columnconfigure(2, weight=1)

        self.geral_fr1.pack(side='top', expand=False, fill='x')
        #ttk.Separator(self.tab_geral).pack(side='top', expand=False, fill='x', pady=10)
        #self.geral_fr2.pack(side='top', expand=True, fill='both')


    def gerar_tab_morada(self):
        self.morada_fr1 = ttk.Frame(self.tab_morada)
        self.ef_lstxt_morada = LabelText(self.morada_fr1, "Morada", height=2, style="Panel_Body.TLabel")

        self.ef_ltxt_cod_postal = LabelEntry(self.morada_fr1, "Código Postal", style="Panel_Body.TLabel", width=10)
        self.ef_ltxt_localidade = LabelEntry(self.morada_fr1, "Localidade", style="Panel_Body.TLabel", width=35)

        self.ef_lbl_pais = ttk.Label(self.morada_fr1, text="País", style="Panel_Body.TLabel")
        self.paises_value = tk.StringVar()
        self.ef_combo_pais = ttk.Combobox(self.morada_fr1, values=TODOS_OS_PAISES,
                                                           textvariable=self.paises_value,
                                                           state='readonly')
        self.ef_combo_pais.current(178) #TODO!
        self.ef_combo_pais.bind("<Key>", self.procurar_em_combobox)



    def montar_tab_morada(self):
        self.ef_lstxt_morada.grid(column=0, row=4, columnspan=3, rowspan=2, padx=5, sticky='we')

        self.ef_ltxt_cod_postal.grid(column=0, row=6, padx=5, sticky='we')
        self.ef_ltxt_localidade.grid(column=1, row=6, columnspan=2, padx=5, sticky='we')

        self.ef_lbl_pais.grid(column=0, columnspan=3, row=7, padx=5, sticky='we')
        self.ef_combo_pais.grid(column=0, columnspan=3, row=8, padx=5, sticky='we')

        self.morada_fr1.grid_columnconfigure(0, weight=1)
        self.morada_fr1.grid_columnconfigure(1, weight=1)
        self.morada_fr1.grid_columnconfigure(2, weight=1)

        self.morada_fr1.pack(side='top', expand=False, fill='x')



    def gerar_tab_notas(self):
        self.notas_fr1 = ttk.Frame(self.tab_notas)
        #self.notas_fr2 = ttk.Frame(self.tab_notas)
        self.ef_cabecalho = ttk.Frame(self.notas_fr1, padding=4)
        self.ef_lbl_tipo = ttk.Label(self.ef_cabecalho, text="Tipo:", style="Panel_Body.TLabel")
        self.ef_chkbtn_tipo_cliente = ttk.Checkbutton(self.ef_cabecalho, text="Cliente", style="Panel_Body.Checkbutton", variable=self.var_tipo_is_cliente)
        self.ef_chkbtn_tipo_fornecedor = ttk.Checkbutton(self.ef_cabecalho, text="Fornecedor ou centro técnico", style="Panel_Body.Checkbutton", variable=self.var_tipo_is_fornecedor)
        self.ef_chkbtn_tipo_loja = ttk.Checkbutton(self.ef_cabecalho, text="Loja do nosso grupo", style="Panel_Body.Checkbutton", variable=self.var_tipo_is_loja)
        
        self.ef_lstxt_notas = LabelText(self.notas_fr1, "\nNotas:", height=3, style="Panel_Body.TLabel")


    def montar_tab_notas(self):
        self.ef_lstxt_notas.grid(column=0, row=9, columnspan=3, rowspan=4, padx=5, sticky='we')
        self.ef_cabecalho.columnconfigure(2, weight=1)
        #self.notas_fr1.columnconfigure(0, weight=1)
 
        self.ef_lbl_tipo.grid(column=0, row=1, sticky='e')
        self.ef_chkbtn_tipo_cliente.grid(column=1, row=1, sticky='w')
        self.ef_chkbtn_tipo_fornecedor.grid(column=1, row=2, sticky='w')
        self.ef_chkbtn_tipo_loja.grid(column=1, row=3, sticky='w')

        self.ef_cabecalho.grid(column=0,row=0, sticky='we')

        self.notas_fr1.columnconfigure(0, weight=1)
        self.notas_fr1.pack(side='top', expand=False, fill='x')
        #ttk.Separator(self.tab_notas).pack(side='top', expand=False, fill='x', pady=10)
        #self.notas_fr2.pack(side='top', expand=True, fill='both')


    def gerar_tab_reparacoes(self):
        self.reparacoes_fr1 = ttk.Frame(self.tab_reparacoes)
        self.reparacoes_fr2 = ttk.Frame(self.tab_reparacoes)


    def montar_tab_reparacoes(self):
        self.reparacoes_fr1.pack(side='top', expand=False, fill='x')
        ttk.Separator(self.tab_reparacoes).pack(side='top', expand=False, fill='x', pady=10)
        self.reparacoes_fr2.pack(side='top', expand=True, fill='both')


    def desativar_campos(self):
        # Desativar todos os campos de texto para não permitir alterações. ------------------------
        #self.txt_numero_contacto.configure(state="disabled")
        #self.txt_nome.configure(state="disabled")
        pass
        #widgets = (,)
        #for widget in widgets:
        #    widget.disable()


    def on_btn_fechar(self, event):
        """ will test for some condition before closing, save if necessary and
                then call destroy()
        """
        window = event.widget.winfo_toplevel()
        window.destroy()


    def procurar_em_combobox(self, event):
        """
        Saltar para o primeiro país da lista (combobox) começado pela letra
        correspondente à tecla pressionada.
        """
        tecla_pressionada = event.char.upper()
        if tecla_pressionada in ascii_uppercase:
            for index, pais in enumerate(TODOS_OS_PAISES):
                if pais[0] == tecla_pressionada:
                    self.ef_combo_pais.current(index)
                    break



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
        #self.master.minsize(W_DETALHE_REP_MIN_WIDTH, W_DETALHE_REP_MIN_HEIGHT)
        #self.master.maxsize(W_DETALHE_REP_MAX_WIDTH, W_DETALHE_REP_MAX_HEIGHT)
        #self.master.geometry(W_DETALHE_REP_GEOMETRIA)
        self.master.title(f"Contacto nº{self.num_contacto}")
        
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
