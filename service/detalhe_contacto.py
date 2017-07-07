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

        self.tipo_processo = "Cliente" if bool((self.num_contacto%2)==0) else "Stock"  #TODO: Substituir isto por função que busca tipo na info da base de dados

        self.is_rep_cliente = (self.tipo_processo == "Cliente")  # i.e. True se for reparação de cliente
        self.estado = ESTADOS[EM_PROCESSAMENTO] #TODO: Obter estado a partir da base de dados

        self.is_garantia = True  # todo - verificar se é garantia
        self.modo_entrega = 2 # todo - obter da base de dados
        self.portes = 0 #todo - obter da base de dados

        self.dicas = Pmw.Balloon(self.master, label_background='#f6f6f6',
                                              hull_highlightbackground='#b3b3b3',
                                              state='balloon',
                                              relmouse='both',
                                              yoffset=18,
                                              xoffset=-2,
                                              initwait=1300)

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

        self.btn_nova_rep = ttk.Button(self.topframe, text="Nova reparação", style="secondary.TButton", command=None)
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
        self.tab_historico = ttk.Frame(self.note, padding=10)
        self.tab_notas = ttk.Frame(self.note, padding=10)
        self.note.add(self.tab_geral, text="Contactos")
        self.note.add(self.tab_historico, text="Morada")
        self.note.add(self.tab_notas, text="Notas")
        self.gerar_tab_geral()
        self.montar_tab_geral()
        self.gerar_tab_historico()
        self.montar_tab_historico()
        self.gerar_tab_notas()
        self.montar_tab_notas()

        if self.is_rep_cliente:
            self.tab_orcamentos = ttk.Frame(self.note, padding=10)
            self.note.add(self.tab_orcamentos, text="Reparações")
            self.gerar_tab_orcamentos()
            self.montar_tab_orcamentos()

        self.desativar_campos()


    def gerar_tab_geral(self):
        # TAB Geral ~~~~~~~~~~~~~~~~
        self.geral_fr1 = ttk.Frame(self.tab_geral)
        self.geral_fr2 = ttk.Frame(self.tab_geral)

        # TODO - obter valor da base de dados
        # Criar widgets para este separador -------------------------------------------------------
        self.txt_numero_contacto = ttk.Entry(self.geral_fr1, font=("Helvetica-Neue", 12), width=5)
        self.txt_nome = ttk.Entry(self.geral_fr1, font=("Helvetica-Neue", 12), width=35)


        # Preencher com dados da base de dados -------------------------------------------------
        self.txt_numero_contacto.insert(0, self.numero_contacto)
        self.txt_nome.insert(0, self.nome)


    def montar_tab_geral(self):
        # Montar todos os campos na grid -------------------------------------------------------------
        self.txt_numero_contacto.grid(column=0, row=0)
        self.txt_nome.grid(column=2, sticky='we', row=0)

        self.geral_fr1.grid_columnconfigure(4, weight=1)
        self.geral_fr1.grid_columnconfigure(3, weight=1)
        self.geral_fr1.grid_columnconfigure(2, weight=1)


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


    def gerar_tab_notas(self):
        self.notas_fr1 = ttk.Frame(self.tab_notas)
        self.notas_fr2 = ttk.Frame(self.tab_notas)


    def montar_tab_notas(self):
        self.notas_fr1.pack(side='top', expand=False, fill='x')
        ttk.Separator(self.tab_notas).pack(side='top', expand=False, fill='x', pady=10)
        self.notas_fr2.pack(side='top', expand=True, fill='both')


    def gerar_tab_orcamentos(self):
        self.orcamentos_fr1 = ttk.Frame(self.tab_orcamentos)
        self.orcamentos_fr2 = ttk.Frame(self.tab_orcamentos)


    def montar_tab_orcamentos(self):
        self.orcamentos_fr1.pack(side='top', expand=False, fill='x')
        ttk.Separator(self.tab_orcamentos).pack(side='top', expand=False, fill='x', pady=10)
        self.orcamentos_fr2.pack(side='top', expand=True, fill='both')


    def desativar_campos(self):
        # Desativar todos os campos de texto para não permitir alterações. ------------------------
        self.txt_numero_contacto.configure(state="disabled")
        self.txt_nome.configure(state="disabled")

        #widgets = (,)
        #for widget in widgets:
        #    widget.disable()


    def on_btn_fechar(self, event):
        """ will test for some condition before closing, save if necessary and
                then call destroy()
        """
        window = event.widget.winfo_toplevel()
        window.destroy()


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
        self.master.title(f"Contacto nº{self.num_contacto} ({self.tipo_processo})")

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
