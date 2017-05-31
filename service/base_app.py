#!/usr/bin/env python3.6
# encoding: utf-8
"""
Este módulo é parte integrante da aplicação RepService, desenvolvida por
Victor Domingos e distribuída sob os termos da licença Creative Commons
Attribution-ShareAlike 4.0 International (CC BY-SA 4.0).
"""

import tkinter as tk
from tkinter import ttk
import tkinter.font
import Pmw

from extra_tk_classes import *
from global_setup import *


class AppStatus:
    """ Classe com variáveis globais relativas ao estado atual da aplicação.
    """
    def __init__(self):
        self.janela_remessas = None   # Guarda referência para o objeto da janela de remessas
        self.janela_contactos = None  # Guarda referência para o objeto da janela de contactos
        self.janela_principal = None  # Guarda referência para o objeto da janela principal
        self.janela_remessas_aberta = False
        self.janela_contactos_aberta = False
        self.painel_mensagens_aberto = False
        self.painel_nova_reparacao_aberto = False
        self.painel_novo_contacto_aberto = False
        self.painel_nova_remessa_aberto = False
        self.contacto_para_nova_reparacao = None
        self.tipo_novo_contacto = None


class baseApp(ttk.Frame):
    """
    Classe de base para as janelas de aplicação. Inclui uma estrutura de vários frames:
        - topframe (Barra de ferramentas)
        - centerframe (organizador da área central), composto por:
          - leftframe (que recebe a tabela principal tree)
          - rightframe (painel escondido por defeito, que pode ser utilizado como inspetor,
            lista de mensagens, etc.)
        - bottomframe (área reservada à barra de estado)
        - tree (tabela com algumas predefinições, ordenação ao clicar nos
          cabeçalhos das colunas, scrollbar automática)
        - entryframe (painel que surge opcionalmente no rodapé da janela, para mostrar
          por exemplo detalhes ou formulários), composto por:
           - entryfr1...entryfr5 (5 frames para organizar widgets, empacotados
             verticalmente e ocupando a totalidade do entryframe)
           - todos os widgets devem ser criados como descendentes de um destes subframes

    São criados alguns objetos e métodos comuns às várias janelas da aplicação:
        - popupMsg() - mensagens breves dentro da janela (tipo notificações)
    """
    def __init__(self,master,*args,**kwargs):
        super().__init__(master,*args,**kwargs)
        self.master = master
        self.estilo = ttk.Style()
        self.is_entryform_visible = False

        self.dicas = Pmw.Balloon(self.master, label_background='#f6f6f6', hull_highlightbackground='#b3b3b3')

        self.mainframe = ttk.Frame(master)
        self.topframe = ttk.Frame(self.mainframe, padding="5 8 5 5")
        self.centerframe = ttk.Frame(self.mainframe)


        self.leftframe = ttk.Frame(self.centerframe)
        self.rightframe = ttk.Frame(self.centerframe)
        self.leftframe.grid(column=0, row=1, sticky="nsew")
        self.rightframe.grid(column=1, row=1, stick="nse")
        self.centerframe.grid_columnconfigure(0, weight=1)
        self.centerframe.grid_columnconfigure(1, weight=0)
        self.centerframe.grid_rowconfigure(1, weight=1)

        self.messagepane = ttk.Frame(self.rightframe, padding="5 5 5 0")

        self.bottomframe = ttk.Frame(self.mainframe)
        self.btnFont = tkinter.font.Font(family="Lucida Grande", size=10)
        self.btnTxtColor = "grey22"
        self.btnTxtColor_active = "white"

        self.tree = ttk.Treeview(self.leftframe, height=60, selectmode='browse')

        # Formulário de introdução de dados (aparece somente quando o utilizador solicita) ----------------------------
        self.entryframe = ttk.Frame(master, padding="4 8 4 10")
        self.estilo.configure("Panel_Title.TLabel", pady=10, foreground="grey25", font=("Helvetica Neue", 18, "bold"))
        self.estilo.configure("Panel_Section_Title.TLabelframe.Label", foreground="grey25", font=("Helvetica Neue", 14, "bold"))
        self.estilo.configure("Panel_Body.TLabel", font=("Lucida Grande", 11))
        self.estilo.configure("Panel_Body.TRadiobutton", font=("Lucida Grande", 11))

        self.estilo.layout('Panel_Body.Checkbutton', self.estilo.layout('TCheckbutton'))  # Copia o estilo padrão dos widgets Checkbutton.
        self.estilo.map('Panel_Body.Checkbutton', **self.estilo.map('TCheckbutton'))
        self.estilo.configure('Panel_Body.Checkbutton', **self.estilo.map('TCheckbutton'))
        self.estilo.configure('Panel_Body.Checkbutton', font=("Lucida Grande", 11))

        #self.estilo.configure(".TLabel", foreground="grey25", font=("Helvetica Neue", 18, "bold"))

        self.estilo.configure("Active.TButton", foreground="white")
        self.entryfr1 = ttk.Frame(self.entryframe)
        self.entryfr2 = ttk.Frame(self.entryframe)
        self.entryfr3 = ttk.Frame(self.entryframe)
        self.entryfr4 = ttk.Frame(self.entryframe)
        self.entryfr5 = ttk.Frame(self.entryframe)

        #get status bar
        self.my_statusbar = StatusBar(self.mainframe)

        self.estilo.configure('Treeview', font=("Lucida Grande", 11), foreground="grey22", rowheight=20)
        self.estilo.configure('Treeview.Heading', font=("Lucida Grande", 11), foreground="grey22")
        self.estilo.configure( 'Treeview', relief = 'flat', borderwidth = 0)

        self.composeFrames()


    def show_entryform(self, *event):
        if not self.is_entryform_visible:
            self.is_entryform_visible = True
            self.btn_add.configure(state="disabled")
            # Formulário de entrada de dados (fundo da janela)
            self.my_statusbar.lift()

            if SLOW_MACHINE:
                self.entryframe.place(in_=self.my_statusbar, relx=1,  y=0, anchor="se", relwidth=1, bordermode="outside")
            else:
                for y in range(-30,-12,6):
                    self.entryframe.update()
                    y = y**2
                    self.entryframe.place(in_=self.my_statusbar, relx=1,  y=y, anchor="se", relwidth=1, bordermode="outside")
                for y in range(-12,-3,3):
                    self.entryframe.update()
                    y = y**2
                    self.entryframe.place(in_=self.my_statusbar, relx=1,  y=y, anchor="se", relwidth=1, bordermode="outside")
                for y in range(-3,0,1):
                    self.entryframe.update()
                    y = y**2
                    self.entryframe.place(in_=self.my_statusbar, relx=1,  y=y, anchor="se", relwidth=1, bordermode="outside")


            self.entryframe.lift()
            #self.entryframe.bind_all("<Escape>", self.hide_entryform)


    def hide_entryform(self, *event):
        if self.is_entryform_visible:
            self.is_entryform_visible = False
            self.btn_add.configure(state="enabled")
            self.my_statusbar.lift()

            if not SLOW_MACHINE:
                for y in range(0,11,2):
                    self.entryframe.place(in_=self.my_statusbar, relx=1,  y=y**2, anchor="se", relwidth=1, bordermode="outside")
                    self.entryframe.update()

            self.entryframe.place_forget()
            


    def composeFrames(self):
        self.topframe.pack(side='top', fill='x')
        self.centerframe.pack(side='top', expand=True, fill='both')
        self.messagepane.pack(side='top', expand=True, fill='both')
        self.bottomframe.pack(side='bottom', fill='x')
        self.mainframe.pack(side='top', expand=True, fill='both')

        self.entryfr1.pack(side='top', expand=True, fill='both')
        self.entryfr2.pack(side='top', expand=True, fill='both')
        self.entryfr3.pack(side='top', expand=True, fill='both')
        self.entryfr4.pack(side='top', expand=True, fill='both')
        self.entryfr5.pack(side='top', expand=True, fill='both')
        self.estilo.configure("secondary.TButton", font=("Lucida Grande", 11))


    def popupMsg(self, msg):
        """
        Mostrar um painel de notificação com uma mensagem
        """
        self.update_idletasks()
        x, y = int(root.winfo_width()/2), 76
        self.popupframe = ttk.Frame(root, padding="15 15 15 15")
        self.msglabel = ttk.Label(self.popupframe, font=self.statusFont, foreground=self.btnTxtColor, text=msg)
        self.msglabel.pack()
        for i in range(1,10,2):
            self.popupframe.place(x=x,  y=y+i, anchor="n", bordermode="outside")
            self.popupframe.update()
        self.popupframe.after(1500, self.popupframe.destroy)


    # ------ Permitir que a tabela possa ser ordenada clicando no cabeçalho ----------------------
    def isNumeric(self, s):
        """
        test if a string s is numeric
        """
        for c in s:
            if c in "1234567890.":
                numeric = True
            else:
                return False
        return numeric

    def changeNumeric(self, data):
        """
        if the data to be sorted is numeric change to float
        """
        new_data = []
        if self.isNumeric(data[0][0]):
            # change child to a float
            for child, col in data:
                new_data.append((float(child), col))
            return new_data
        return data


    def sortBy(self, tree, col, descending):
        """
        sort tree contents when a column header is clicked
        """
        # grab values to sort
        data = [(tree.set(child, col), child) for child in tree.get_children('')]
        # if the data to be sorted is numeric change to float
        data =  self.changeNumeric(data)
        # now sort the data in place
        data.sort(reverse=descending)
        for ix, item in enumerate(data):
            tree.move(item[1], '', ix)
        # switch the heading so that it will sort in the opposite direction
        tree.heading(col, command=lambda col=col: self.sortBy(tree, col, int(not descending)))
        self.alternar_cores(tree)
    # ------ Fim das funções relacionadas c/ o ordenamento da tabela -----------------------------


    def alternar_cores(self, tree, inverso=False, fundo1='grey98', fundo2='white'):
        tree = tree
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


    def configurarTree(self):
        # Ordenar por coluna ao clicar no respetivo cabeçalho
        for col in self.tree['columns']:
            self.tree.heading(col, text=col.title(),
            command=lambda c=col: self.sortBy(self.tree, c, 0))

        # Barra de deslocação para a tabela
        self.tree.grid(column=0, row=0, sticky="nsew", in_=self.leftframe)
        self.vsb = AutoScrollbar(self.leftframe, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.vsb.set)
        self.vsb.grid(column=1, row=0, sticky="ns", in_=self.leftframe)
