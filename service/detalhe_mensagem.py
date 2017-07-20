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

from extra_tk_classes import *
from global_setup import *
from detalhe_reparacao import *


class msgDetailWindow(ttk.Frame):
    """ Classe de base para a janela de detalhes de mensagem """
    def __init__(self, master, num_mensagem, *args,**kwargs):
        super().__init__(master,*args,**kwargs)
        self.num_mensagem = num_mensagem
        self.master = master
        self.master.bind("<Command-w>", self.on_btn_fechar)
        self.master.focus()
        self.num_rep = 12345 # TODO - obter número da reparação
        self.nome = "José Manuel da Cunha Fantástico"
        self.artigo = "Um artigo que se encontra em reparação"
        self.estado_atual = "Em processamento"
        self.resultado = "Orçamento aprovado"
        self.detalhe = "Texto completo do evento ou mensagem conforme escrito pelo utilizador."
        self.remetente = "Utilizador que registou o evento"
        self.data = "12/05/2021 18:01"

        self.configurar_frames_e_estilos()
        self.montar_painel_principal()
        self.montar_barra_de_ferramentas()
        self.montar_rodape()
        self.composeFrames()
        self.desativar_campos()


    def on_btn_abrir_rep(self, event):
        """ Abre a janela de detalhes do processo a que se refere esta mensagem.
        """
        self.rep_DetailsWindow = tk.Toplevel()
        self.janela_detalhes_rep = repairDetailWindow(self.rep_DetailsWindow, self.num_rep)


    def on_btn_apagar_msg(self, event):
        """ Apaga a mensagem (remove-a da lista de mensagens) e fecha esta
            janela.
        """
        #TODO: Apagar a mensagem
        window = event.widget.winfo_toplevel()
        window.destroy()


    def on_btn_fechar(self, event):
        #self.master.close_detail_msg_window(event)
        """ Fecha esta janela. """
        window = event.widget.winfo_toplevel()
        window.destroy()


    def montar_barra_de_ferramentas(self):
        self.lbl_titulo = ttk.Label(self.topframe, style="Panel_Title.TLabel", foreground=self.btnTxtColor, text=f"Reparação nº {self.num_rep}")

        self.btn_abrir_rep = ttk.Button(self.topframe, text="Ver Reparação", style="secondary.TButton", command=None)
        self.dicas.bind(self.btn_abrir_rep, 'Clique para abrir a janela de detalhes\nda reparação a que se refere esta mensagem.')
        self.btn_abrir_rep.bind("<ButtonRelease>", self.on_btn_abrir_rep)

        self.btn_apagar_msg = ttk.Button(self.topframe, text="Apagar", style="secondary.TButton", command=None)
        self.dicas.bind(self.btn_apagar_msg, 'Clique para fechar a janela\ne não voltar a mostrar esta mensagem.')
        self.btn_apagar_msg.bind("<ButtonRelease>", self.on_btn_apagar_msg)

        """
        self.btn_fechar = ttk.Button(self.topframe, text="Fechar", style="secondary.TButton")
        self.dicas.bind(self.btn_fechar, 'Clique para fechar a janela e manter\nesta mensagem visível na lista de mensagens.')
        self.btn_fechar.bind("<ButtonRelease>", self.on_btn_fechar)
        """
        
        self.lbl_titulo.grid(column=0, row=0, rowspan=2)
        self.btn_abrir_rep.grid(column=7, row=0)
        self.btn_apagar_msg.grid(column=8, row=0)
        #self.btn_fechar.grid(column=9, row=0)
        self.topframe.grid_columnconfigure(5, weight=1)


    def montar_painel_principal(self):
        self.lbl_nome = ttk.Label(self.centerframe, text="Nome:", style="Panel_Body.TLabel")
        self.lbl_nome_ = ttk.Label(self.centerframe, text=self.nome, style="Panel_Body.TLabel")

        self.lbl_artigo = ttk.Label(self.centerframe, text="Artigo:", style="Panel_Body.TLabel")
        self.lbl_artigo_ = ttk.Label(self.centerframe, text=self.artigo, style="Panel_Body.TLabel")

        self.lbl_estado_atual = ttk.Label(self.centerframe, text="Estado atual:", style="Panel_Body.TLabel")
        self.lbl_estado_atual_ = ttk.Label(self.centerframe, text=self.estado_atual, style="Panel_Body.TLabel")

        self.lbl_resultado_evento = ttk.Label(self.centerframe, text="Resultado:", style="Panel_Body.TLabel")
        self.lbl_resultado_evento_ = ttk.Label(self.centerframe, text=self.resultado, style="Panel_Body.TLabel")

        self.ltxt_detalhe = LabelText(self.centerframe, "\n\nDetalhes:", width=35, height=3, style="Panel_Body.TLabel")
        self.ltxt_detalhe.set(self.detalhe)

        self.lbl_nome.grid(column=0, row=1, sticky='e')
        self.lbl_nome_.grid(column=1, row=1, sticky='w')
        self.lbl_artigo.grid(column=0, row=2, sticky='e')
        self.lbl_artigo_.grid(column=1, row=2, sticky='w')
        self.lbl_estado_atual.grid(column=0, row=3, sticky='e')
        self.lbl_estado_atual_.grid(column=1, row=3, sticky='w')
        self.lbl_resultado_evento.grid(column=0, row=4, sticky='e')
        self.lbl_resultado_evento_.grid(column=1, row=4, sticky='w')
        self.ltxt_detalhe.grid(column=0, row=5, columnspan=2, sticky='we')
        self.centerframe.grid_columnconfigure(0, weight=0)
        self.centerframe.grid_columnconfigure(1, weight=1)

        print(f"A mostrar detalhes da mensagem nº {self.num_mensagem}")


    def desativar_campos(self):
        # Desativar todos os campos de texto para não permitir alterações. ------------------------
        self.ltxt_detalhe.disable()


    def montar_rodape(self):
        #TODO - obter dados da base de dados
        txt = "Enviada por Victor Domingos em 12/05/2021 18:01."

        self.rodapeFont = tk.font.Font(family="Lucida Grande", size=9)
        self.rodapeTxtColor = "grey22"

        self.txt = ttk.Label(self.bottomframe, anchor='n', text=txt, font=self.rodapeFont, foreground=self.rodapeTxtColor)
        self.txt.pack(side="top")


    def configurar_frames_e_estilos(self):
        self.master.minsize(W_DETALHE_MSG_MIN_WIDTH, W_DETALHE_MSG_MIN_HEIGHT)
        self.master.maxsize(W_DETALHE_MSG_MAX_WIDTH, W_DETALHE_MSG_MAX_HEIGHT)
        self.master.geometry(W_DETALHE_MSG_GEOMETRIA)
        self.dicas = Pmw.Balloon(self.master, label_background='#f6f6f6',
                                 hull_highlightbackground='#b3b3b3',
                                 state='balloon',
                                 relmouse='both',
                                 yoffset=18,
                                 xoffset=-2,
                                 initwait=1300)

        self.master.title(f'Mensagem nº {self.num_mensagem}')
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
