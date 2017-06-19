#!/usr/bin/env python3.6
# encoding: utf-8
"""
Este módulo é parte integrante da aplicação RepService, desenvolvida por
Victor Domingos e distribuída sob os termos da licença Creative Commons
Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)
"""
import tkinter as tk
from tkinter import ttk
import tkinter.font
from global_setup import *


class contactDetailWindow(ttk.Frame):
    """ Classe de base para a janela de detalhes de contactos """
    def __init__(self, master, num_contacto, *args,**kwargs):
        super().__init__(master,*args,**kwargs)
        self.num_contacto = num_contacto
        self.master = master
        self.master.bind("<Command-w>", self.on_btn_fechar)
        self.master.focus()

        self.configurar_frames_e_estilos()
        self.montar_barra_de_ferramentas()
        self.montar_painel_principal()
        self.montar_rodape()
        self.composeFrames()


    def on_btn_fechar(self, event):
        """ will test for some condition before closing, save if necessary and
            then call destroy()
        """
        window = event.widget.winfo_toplevel()
        window.destroy()


    def montar_barra_de_ferramentas(self):
        ttk.Label(self.topframe, text="12345").grid(column=0, row=0, sticky='w')
        ttk.Label(self.topframe, text="José Manuel da Silva Costa Ferreira").grid(column=0, row=1, sticky='w')

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
        self.mbtn_alterar.grid(column=7, row=0)
        self.label_mbtn_alterar.grid(column=7, row=1)
        # ----------- fim de Botão com menu "Alterar estado" -------------

        self.topframe.grid_columnconfigure(1, weight=1)


    def montar_painel_principal(self):
        print(f"A mostrar detalhes do contacto nº {self.num_contacto}")


    def montar_rodape(self):
        #TODO - obter dados da base de dados
        txt_esquerda = "Criado por Victor Domingos em 12/05/2021 18:01."
        txt_direita = "Atualizado por Victor Domingos em 13/05/2021 17:01."

        self.rodapeFont = tk.font.Font(family="Lucida Grande", size=9)
        self.rodapeTxtColor = "grey22"

        self.esquerda = ttk.Label(self.bottomframe, anchor='w', text=txt_esquerda, font=self.rodapeFont, foreground=self.rodapeTxtColor)
        self.direita = ttk.Label(self.bottomframe, anchor='e', text=txt_direita, font=self.rodapeFont, foreground=self.rodapeTxtColor)
        self.esquerda.pack(side="left")
        self.direita.pack(side="right")


    def configurar_frames_e_estilos(self):
        self.master.minsize(W_DETALHE_CONTACTO_MIN_WIDTH, W_DETALHE_CONTACTO_MIN_HEIGHT)
        self.master.maxsize(W_DETALHE_CONTACTO_MAX_WIDTH, W_DETALHE_CONTACTO_MAX_HEIGHT)
        self.master.geometry(W_DETALHE_CONTACTO_GEOMETRIA)
        self.mainframe = ttk.Frame(self.master)
        self.topframe = ttk.Frame(self.mainframe, padding="5 8 5 5")
        self.centerframe = ttk.Frame(self.mainframe)
        self.bottomframe = ttk.Frame(self.mainframe, padding="3 1 3 1")

        self.estilo = ttk.Style()
        self.estilo.configure("Panel_Title.TLabel", pady=10, foreground="grey25", font=("Helvetica Neue", 18, "bold"))
        self.estilo.configure("Active.TButton", foreground="white")

        self.btnFont = tk.font.Font(family="Lucida Grande", size=10)
        self.btnTxtColor = "grey22"

        self.statusFont = tkinter.font.Font(family="Lucida Grande", size=11)
        self.status_left = ttk.Label(self.bottomframe,anchor='w', text="" , font=self.statusFont, foreground=self.btnTxtColor)
        self.status_right = ttk.Label(self.bottomframe,anchor='e', font=self.statusFont, foreground=self.btnTxtColor)
        self.status_left.pack(side="left")
        self.status_right.pack(side="right")


    def composeFrames(self):
        self.topframe.pack(side=tk.TOP, fill=tk.X)
        self.centerframe.pack(side=tk.TOP, fill=tk.BOTH)
        self.bottomframe.pack(side=tk.BOTTOM, fill=tk.X)
        self.mainframe.pack(side=tk.TOP, expand=True, fill=tk.BOTH)
