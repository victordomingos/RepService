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
from extra_tk_classes import *




class remessaDetailWindow(ttk.Frame):
    """ Classe de base para a janela de detalhes de remessa """
    def __init__(self, master, num_remessa, *args,**kwargs):
        super().__init__(master,*args,**kwargs)
        self.num_remessa = num_remessa
        self.master = master
        self.master.bind("<Command-w>", self.on_btn_fechar)
        self.master.focus()
        # Todo - obter da base de dados
        self.tipo = "entrada"
        self.tipo = "saída"
        self.numero_contacto = "90000" #TODO numero de fornecedor
        self.nome = "That International Provider of Great Stuff, Inc." #TODO Nome do fornecedor

        self.artigo = "Um artigo que se encontra em reparação"
        self.estado_atual = "Em processamento"
        self.resultado = "Orçamento aprovado"
        self.detalhe = "Texto completo do evento ou mensagem conforme escrito pelo utilizador."
        self.remetente = "Utilizador que registou o evento"
        self.data = "12/05/2021 18:01"

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
        self.lbl_titulo.grid(column=0, row=0, rowspan=2)
        #self.btn_abrir_rep.grid(column=7, row=0)
        #self.btn_apagar_msg.grid(column=8, row=0)
        #self.btn_fechar.grid(column=9, row=0)
        self.topframe.grid_columnconfigure(5, weight=1)


    def desativar_campos(self):
        # Desativar todos os campos de texto para não permitir alterações. ------------------------
        #self.ltxt_detalhe.disable()
        self.txt_numero_contacto.configure(state="disabled")
        self.txt_nome.configure(state="disabled")


    def montar_painel_principal(self):
        print(f"A mostrar detalhes da remessa nº {self.num_remessa}")
        self.txt_numero_contacto = ttk.Entry(self.centerframe, font=("Helvetica-Neue", 12), width=5)
        self.txt_nome = ttk.Entry(self.centerframe, font=("Helvetica-Neue", 12), width=35)

        # Preencher com dados da base de dados -------------------------------------------------
        self.txt_numero_contacto.insert(0, self.numero_contacto)
        self.txt_nome.insert(0, self.nome)


        self.tree = ttk.Treeview(self.treeframe, height=10, selectmode='browse')
        self.tree['columns'] = ('Nº', 'Cliente', 'Equipamento', 'Serviço')
        #self.tree.pack(side='top', expand=True, fill='both')
        self.tree.column('#0', anchor='w', minwidth=0, stretch=0, width=0)
        self.tree.column('Nº', anchor='e', minwidth=46, stretch=0, width=46)
        self.tree.column('Cliente', minwidth=80, stretch=1, width=120)
        self.tree.column('Equipamento', minwidth=80, stretch=1, width=170)
        self.tree.column('Serviço', minwidth=80, stretch=1, width=210)
        # Ordenar por coluna ao clicar no respetivo cabeçalho
        for col in self.tree['columns']:
            self.tree.heading(col, text=col.title(),
            command=lambda c=col: self.sortBy(self.tree, c, 0))

        # Barra de deslocação para a tabela
        self.tree.grid(column=0, row=0, sticky="nsew", in_=self.treeframe)
        self.vsb = AutoScrollbar(self.treeframe, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.vsb.set)
        self.vsb.grid(column=1, row=0, sticky="ns", in_=self.treeframe)

        #self.leftframe.grid_columnconfigure(0, weight=1)
        #self.leftframe.grid_columnconfigure(1, weight=0)
        #self.leftframe.grid_rowconfigure(0, weight=1)

        self.bind_tree()

        self.txt_numero_contacto.grid(row=1, column=0)
        self.txt_nome.grid(row=1, column=1, columnspan=2, sticky="we")

        self.treeframe.grid_columnconfigure(0, weight=1)
        self.treeframe.grid_rowconfigure(0, weight=1)

        self.centerframe.grid_columnconfigure(0, weight=0)
        self.centerframe.grid_columnconfigure(1, weight=1)
        self.centerframe.grid_columnconfigure(2, weight=1)
        self.desativar_campos()


    def bind_tree(self):
        self.tree.bind('<<TreeviewSelect>>', self.selectItem_popup)
        self.tree.bind('<Double-1>', lambda x: self.create_window_detalhe_remessa(num_remessa=self.remessa_selecionada))
        self.tree.bind("<Button-2>", self.popupMenu)
        self.tree.bind("<Button-3>", self.popupMenu)
        self.update_idletasks()


    def unbind_tree(self):
        self.tree.bind('<<TreeviewSelect>>', None)
        self.tree.bind('<Double-1>', None)
        self.tree.bind("<Button-2>", None)
        self.tree.bind("<Button-3>", None)
        self.update_idletasks()

    def selectItem_popup(self, event):
        """ # Hacking moment: Uma função que junta duas funções, para assegurar a sequência...
        """
        self.selectItem()
        self.popupMenu(event)


    def popupMenu(self, event):
        """action in event of button 3 on tree view"""
        # select row under mouse
        self.selectItem()

        iid = self.tree.identify_row(event.y)
        x, y = event.x_root, event.y_root
        if iid:
            if x!=0 and y!=0:
                # mouse pointer over item
                self.tree.selection_set(iid)
                self.tree.focus(iid)
                self.contextMenu.post(event.x_root, event.y_root)
                print("popupMenu(): x,y = ", event.x_root, event.y_root)
            else:
                print("popupMenu(): wrong values for event - x=0, y=0")
        else:
            print(iid)
            print("popupMenu(): Else - No code here yet! (mouse not over item)")
            # mouse pointer not over item
            # occurs when items do not fill frame
            # no action required
            pass


    def selectItem(self, *event):
        """
        Obter remessa selecionada (após clique de rato na linha correspondente)
        """
        curItem = self.tree.focus()
        tree_linha = self.tree.item(curItem)

        remessa = tree_linha["values"][0]
        destino =  tree_linha["values"][2]
        self.my_statusbar.set(f"{remessa} • {destino}")
        self.remessa_selecionada = remessa



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
        self.treeframe = ttk.Frame(self.centerframe, padding="0 8 0 0")
        self.bottomframe = ttk.Frame(self.mainframe, padding="3 1 3 1")

        self.estilo = ttk.Style()
        self.estilo.configure("Panel_Title.TLabel", pady=10, foreground="grey25", font=("Helvetica Neue", 18, "bold"))
        self.estilo.configure("Active.TButton", foreground="white")

        self.btnFont = tk.font.Font(family="Lucida Grande", size=10)
        self.btnTxtColor = "grey22"


    def composeFrames(self):
        self.topframe.pack(side=tk.TOP, fill=tk.X, expand=False)
        self.bottomframe.pack(side=tk.BOTTOM, fill=tk.X)
        self.treeframe.grid(column=0, row=3, columnspan=3, sticky="nsew")
        self.centerframe.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.mainframe.pack(side=tk.TOP, expand=True, fill=tk.BOTH)
