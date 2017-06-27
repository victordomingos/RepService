#!/usr/bin/env python3.6
# encoding: utf-8
"""
Este módulo é parte integrante da aplicação RepService, desenvolvida por
Victor Domingos e distribuída sob os termos da licença Creative Commons
Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)
"""
import tkinter as tk
import Pmw
from tkinter import ttk
from global_setup import *



class remessaDetailWindow(ttk.Frame):
    """ Classe de base para a janela de detalhes de remessa """
    def __init__(self, master, num_remessa, *args,**kwargs):
        super().__init__(master,*args,**kwargs)
        self.num_remessa = num_remessa
        self.master = master
        self.master.bind("<Command-w>", self.on_btn_fechar)
        self.master.focus()

        self.nome = "José Manuel da Cunha Fantástico"
        self.artigo = "Um artigo que se encontra em reparação"
        self.estado_atual = "Em processamento"
        self.resultado = "Orçamento aprovado"
        self.detalhe = "Texto completo do evento ou mensagem conforme escrito pelo utilizador."
        self.remetente = "Utilizador que registou o evento"
        self.data = "12/05/2021 18:01"

        self.tipo = "entrada"
        self.tipo = "saída"
        self.master.title(f'Remessa nº {self.num_remessa}')
        
        self.configurar_frames_e_estilos()
        self.montar_painel_principal()
        self.montar_barra_de_ferramentas()
        self.montar_rodape()
        self.composeFrames()
        self.desativar_campos()


    def on_btn_fechar(self, event):
        """ Fecha esta janela. """
        window = event.widget.winfo_toplevel()
        window.destroy()


    def montar_barra_de_ferramentas(self):
        self.lbl_titulo = ttk.Label(self.topframe, style="Panel_Title.TLabel", foreground=self.btnTxtColor, text=f"Remessa de {self.tipo} nº {self.num_remessa}")

        """
        self.btn_abrir_rep = ttk.Button(self.topframe, text="Ver Reparação", style="secondary.TButton", command=None)
        self.dicas.bind(self.btn_abrir_rep, 'Clique para abrir a janela de detalhes\nda reparação a que se refere esta mensagem.')
        self.btn_abrir_rep.bind("<ButtonRelease>", self.on_btn_abrir_rep)

        self.btn_apagar_msg = ttk.Button(self.topframe, text="Apagar", style="secondary.TButton", command=None)
        self.dicas.bind(self.btn_apagar_msg, 'Clique para fechar a janela\ne não voltar a mostrar esta mensagem.')
        self.btn_apagar_msg.bind("<ButtonRelease>", self.on_btn_apagar_msg)


        self.btn_fechar = ttk.Button(self.topframe, text="Fechar", style="secondary.TButton")
        self.dicas.bind(self.btn_fechar, 'Clique para fechar a janela e manter\nesta mensagem visível na lista de mensagens.')
        self.btn_fechar.bind("<ButtonRelease>", self.on_btn_fechar)
        """
        self.lbl_titulo.grid(column=0, row=0, rowspan=2, padx=10)
        #self.btn_abrir_rep.grid(column=7, row=0)
        #self.btn_apagar_msg.grid(column=8, row=0)
        #self.btn_fechar.grid(column=9, row=0)
        self.topframe.grid_columnconfigure(5, weight=1)


    def desativar_campos(self):
        # Desativar todos os campos de texto para não permitir alterações. ------------------------
        #self.ltxt_detalhe.disable()
        pass


    def montar_painel_principal(self):
        print(f"A mostrar detalhes da remessa nº {self.num_remessa}")


    def montar_rodape(self):
        #TODO - obter dados da base de dados
        txt = "Remessa criada por Victor Domingos em 12/05/2021 18:01."

        self.rodapeFont = tk.font.Font(family="Lucida Grande", size=9)
        self.rodapeTxtColor = "grey22"

        self.txt = ttk.Label(self.bottomframe, anchor='n', text=txt, font=self.rodapeFont, foreground=self.rodapeTxtColor)
        self.txt.pack(side="top")



    def configurar_frames_e_estilos(self):
        self.master.minsize(W_DETALHE_REMESSA_MIN_WIDTH, W_DETALHE_REMESSA_MIN_HEIGHT)
        self.master.maxsize(W_DETALHE_REMESSA_MAX_WIDTH, W_DETALHE_REMESSA_MAX_HEIGHT)
        self.master.geometry(W_DETALHE_REMESSA_GEOMETRIA)
        self.dicas = Pmw.Balloon(self.master, label_background='#f6f6f6',
                                 hull_highlightbackground='#b3b3b3',
                                 state='balloon',
                                 relmouse='both',
                                 yoffset=18,
                                 xoffset=-2,
                                 initwait=1300)
        self.mainframe = ttk.Frame(self.master)
        self.topframe = ttk.Frame(self.mainframe, padding="5 8 5 20")
        self.centerframe = ttk.Frame(self.mainframe, padding="5 8 5 5")
        self.bottomframe = ttk.Frame(self.mainframe, padding="3 1 3 1")

        self.estilo = ttk.Style()
        self.estilo.configure("Panel_Title.TLabel", pady=10, foreground="grey25", font=("Helvetica Neue", 18, "bold"))
        self.estilo.configure("Active.TButton", foreground="white")

        self.btnFont = tk.font.Font(family="Lucida Grande", size=10)
        self.btnTxtColor = "grey22"


    def composeFrames(self):
        self.topframe.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.bottomframe.pack(side=tk.BOTTOM, fill=tk.X)
        self.centerframe.pack(side=tk.TOP, fill=tk.X)
        self.mainframe.pack(side=tk.TOP, expand=True, fill=tk.BOTH)
