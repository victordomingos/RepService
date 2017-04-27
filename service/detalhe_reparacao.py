#!/usr/bin/env python3.6
# encoding: utf-8
"""
Este módulo é parte integrante da aplicação RepService, desenvolvida por
Victor Domingos e distribuída sob os termos da licença Creative Commons
Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)
"""
import tkinter as tk
from tkinter import ttk


class repairDetailWindow(ttk.Frame):
    """ Classe de base para a janela de remessas """
    def __init__(self, master, num_reparacao, *args,**kwargs):
        super().__init__(master,*args,**kwargs)
        self.num_reparacao = num_reparacao
        self.master.minsize(900, 600)
        self.master.maxsize(900, 600)
        #self.centerframe = ttk.Frame(self.mainframe, padding="4 0 4 0") #apagar isto
        print(f"A mostrar detalhes da reparação nº {self.num_reparacao}")
        self.mainframe = ttk.Frame(master)
        self.mainframe.pack()

        self.lbl_text = ttk.Label(self.mainframe,
                                  text=f"A mostrar detalhes da reparação nº {self.num_reparacao}")
        self.lbl_text.pack()
