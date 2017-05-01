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



class remessaDetailWindow(ttk.Frame):
    """ Classe de base para a janela de detalhes de remessa """
    def __init__(self, master, num_remessa, *args,**kwargs):
        super().__init__(master,*args,**kwargs)
        self.num_remessa = num_remessa
        self.master = master

        self.configurar_frames_e_estilos()
        self.montar_barra_de_ferramentas()
        self.montar_painel_principal()
        self.montar_rodape()
        self.composeFrames()
    
    
    def montar_barra_de_ferramentas(self):
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

    
    
    def montar_painel_principal(self):
        print(f"A mostrar detalhes da remessa nº {self.num_remessa}")

           
    def montar_rodape(self):
        pass
            
    

    def configurar_frames_e_estilos(self):
        self.master.minsize(W_DETALHE_REMESSA_MIN_WIDTH, W_DETALHE_REMESSA_MIN_HEIGHT)
        self.master.maxsize(W_DETALHE_REMESSA_MAX_WIDTH, W_DETALHE_REMESSA_MAX_HEIGHT)
        self.master.geometry(W_DETALHE_REMESSA_GEOMETRIA)
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
