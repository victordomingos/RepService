#!/usr/bin/env python3.6
# encoding: utf-8
"""
Aplicação de base de dados para registo de processos de garantia e reparações.
Permite manter um registo dos artigos entregues pelos clientes, do seu
percurso durante a tramitação do processo e da comunicação realizada.

Os processos que requerem atenção, devido a atrasos na entrega ou na receção
de comunicação de cliente são destacados na lista principal, por forma a
permitir uma intervenção em conformidade.

Desenvolvido em Python 3 (com muitas noites passadas em claro), a partir de
uma ideia original de Márcio Araújo, por:

    Victor Domingos
    http://victordomingos.com


© 2017 Victor Domingos
Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)
"""

import tkinter as tk
import tkinter.font
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
import datetime
import textwrap
from string import ascii_uppercase


from about_window import *
from base_app import *
from extra_tk_classes import *
from global_setup import *
from contactos import *
from remessas import *


__app_name__ = "RepService 2017"
__author__ = "Victor Domingos"
__copyright__ = "Copyright 2017 Victor Domingos"
__license__ = "Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)"
__version__ = "v.0.5 development"
__email__ = "web@victordomingos.com"
__status__ = "Development"


class App(baseApp):
    """ base class for application """
    def __init__(self,master,*args,**kwargs):
        super().__init__(master,*args,**kwargs)
        self.master = master
        self.master.minsize(MASTER_MIN_WIDTH, MASTER_MIN_HEIGTH)
        self.master.maxsize(MASTER_MAX_WIDTH, MASTER_MAX_HEIGTH)
        self.a_editar_reparacao = False

        self.gerar_menu()
        self.montar_barra_de_ferramentas()
        self.montar_tabela()
        self.gerar_painel_entrada()

        self.nprocessos = 1232 #TODO - contar processos em curso
        self.my_statusbar.set(f"{self.nprocessos} processos")

        self.composeFrames()
        self.inserir_dados_de_exemplo()
        self.alternar_cores(self.tree)
        #self.after(5000, self.teste_GUI)


    def teste_GUI(self):
        for i in range(10):
            print(i)
            self.create_window_contacts()
            self.create_window_remessas()
            self.abrir_painel_mensagens()
            self.mostrar_painel_entrada()

            self.close_window_contactos()
            self.close_window_remessas()
            self.fechar_painel_mensagens()
            self.fechar_painel_entrada()


    def bind_tree(self):
        self.tree.bind('<<TreeviewSelect>>', self.selectItem_popup)
        self.tree.bind('<Double-1>', None)
        #self.tree.bind("<Button-2>", self.popupMenu)
        #self.tree.bind("<Button-3>", self.popupMenu)


    def unbind_tree(self):
        self.tree.bind('<<TreeviewSelect>>', None)
        self.tree.bind('<Double-1>', None)
        self.tree.bind("<Button-2>", None)
        self.tree.bind("<Button-3>", None)


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

        processo = tree_linha["values"][0]
        equipamento =  tree_linha["values"][2]
        num_serie =  "S/N: CK992737632POT234B" #TODO: obter num serie
        self.my_statusbar.set(f"{equipamento} • {num_serie}")
        self.reparacao_selecionada = processo


    def montar_tabela(self):
        self.tree['columns'] = ('Nº', 'Cliente', 'Equipamento', 'Serviço', 'Estado', 'Dias')
        self.tree.pack(side=tk.TOP, fill=tk.BOTH)
        self.tree.column('#0', anchor=tk.W, minwidth=0, stretch=0, width=0)
        self.tree.column('Nº', anchor=tk.E, minwidth=46, stretch=0, width=46)
        self.tree.column('Cliente', minwidth=120, stretch=1, width=120)
        self.tree.column('Equipamento', minwidth=170, stretch=1, width=170)
        self.tree.column('Serviço', minwidth=210, stretch=1, width=210)
        self.tree.column('Estado', minwidth=145, stretch=0, width=145)
        self.tree.column('Dias', anchor=tk.E, minwidth=35, stretch=0, width=35)
        self.configurarTree()
        self.leftframe.grid_columnconfigure(0, weight=1)
        self.leftframe.grid_rowconfigure(0, weight=1)

        self.bind_tree()


    def montar_barra_de_ferramentas(self):
        self.btn_add = ttk.Button(self.topframe, text="➕", width=6, command=self.show_entryform)
        self.btn_add.grid(column=0, row=0)
        self.label_add = ttk.Label(self.topframe, font=self.btnFont, foreground=self.btnTxtColor, text="Nova reparação")
        self.label_add.grid(column=0, row=1)


        # ----------- Botão com menu "Mostrar" --------------
        self.label_mbtn_mostrar = ttk.Label(self.topframe, font=self.btnFont, foreground=self.btnTxtColor, text="Mostrar processos…")
        self.mbtn_mostrar = ttk.Menubutton (self.topframe, text="Processos", width=18)
        self.mbtn_mostrar.menu  =  tk.Menu (self.mbtn_mostrar, tearoff=0)
        self.mbtn_mostrar["menu"] =  self.mbtn_mostrar.menu

        self.mbtn_mostrar.menu.add_command(label="Processos em curso", command=None, accelerator="Command+Option+1")
        self.mbtn_mostrar.menu.add_command(label="Processos finalizados", command=None, accelerator="Command+Option+2")
        self.mbtn_mostrar.menu.add_command(label="Todos os processos", command=None, accelerator="Command+Option+3")
        self.mbtn_mostrar.menu.add_separator()
        self.mbtn_mostrar.menu.add_command(label=ESTADOS[EM_PROCESSAMENTO], command=None, accelerator="Command+Option+4")
        self.mbtn_mostrar.menu.add_command(label=ESTADOS[AGUARDA_ENVIO], command=None, accelerator="Command+Option+5")
        self.mbtn_mostrar.menu.add_command(label=ESTADOS[AGUARDA_RESP_FORNECEDOR], command=None, accelerator="Command+Option+6")
        self.mbtn_mostrar.menu.add_command(label=ESTADOS[AGUARDA_RESP_CLIENTE], command=None, accelerator="Command+Option+7")
        self.mbtn_mostrar.menu.add_command(label=ESTADOS[AGUARDA_RECECAO], command=None, accelerator="Command+Option+8")
        self.mbtn_mostrar.menu.add_command(label=ESTADOS[RECEBIDO], command=None, accelerator="Command+Option+9")
        self.mbtn_mostrar.menu.add_command(label=ESTADOS[DISPONIVEL_P_LEVANTAMENTO], command=None, accelerator="Command+Option+0")

        self.mbtn_mostrar.grid(column=1, row=0)
        self.label_mbtn_mostrar.grid(column=1, row=1)
        # ----------- fim de Botão com menu "Mostrar" -------------


        self.btn_hoje = ttk.Button(self.topframe, text=" ℹ️️", width=3, command=None)
        self.btn_hoje.grid(column=6, row=0)
        ttk.Label(self.topframe, font=self.btnFont, foreground=self.btnTxtColor, text="Detalhes").grid(column=6, row=1)


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


        self.btn_pag = ttk.Button(self.topframe, text=" ✅", width=3, command=None)
        self.btn_pag.grid(column=8, row=0)
        self.label_pag = ttk.Label(self.topframe, font=self.btnFont, foreground=self.btnTxtColor, text="Entregar")
        self.label_pag.grid(column=8, row=1)

        self.btn_messages = ttk.Button(self.topframe, text=" ☝️️", width=3, command=self.abrir_painel_mensagens)
        self.label_messages = ttk.Label(self.topframe, font=self.btnFont, foreground=self.btnTxtColor, text="Mensagens")
        self.btn_messages.grid(row=0, column=13)
        self.label_messages.grid(column=13, row=1)

        self.btn_contacts = ttk.Button(self.topframe, text=" ✉️️", width=3, command=self.create_window_contacts)
        self.label_contacts = ttk.Label(self.topframe, font=self.btnFont, foreground=self.btnTxtColor, text="Contactos")
        self.btn_contacts.grid(row=0, column=14)
        self.label_contacts.grid(column=14, row=1)


        self.btn_remessas = ttk.Button(self.topframe,text=" ⬆️️", width=3, command=self.create_window_remessas)
        self.label_remessas = ttk.Label(self.topframe, font=self.btnFont, foreground=self.btnTxtColor, text="Remessas")
        self.btn_remessas.grid(row=0,column=15)
        self.label_remessas.grid(column=15, row=1)


        self.text_input_pesquisa = ttk.Entry(self.topframe, width=12)

        self.text_input_pesquisa.grid(column=16, row=0)
        ttk.Label(self.topframe, font=self.btnFont, foreground=self.btnTxtColor, text="Pesquisar").grid(column=16, row=1)

        #letras_etc = ascii_letters + "01234567890-., "
        #for char in letras_etc:
        #    keystr = '<KeyRelease-' + char + '>'
        #    self.text_input_pesquisa.bind(keystr, self.ativar_pesquisa)
        #self.text_input_pesquisa.bind('<Button-1>', self.clique_a_pesquisar)
        #self.text_input_pesquisa.bind('<KeyRelease-Escape>', self.cancelar_pesquisa)
        #self.text_input_pesquisa.bind('<KeyRelease-Mod2-a>', self.text_input_pesquisa.select_range(0, END))

        for col in range(1,16):
            self.topframe.columnconfigure(col, weight=0)
        #self.topframe.columnconfigure(3, weight=1)
        self.topframe.columnconfigure(5, weight=1)
        self.topframe.columnconfigure(11, weight=1)


    def create_window_remessas(self, *event, criar_nova_remessa=None):
        #TODO: as janelas de contactos e remesas não são destruídas corretamente, ficam sempre na memória e no menu. Como resolver?

        if not estado.janela_remessas_aberta:
            if criar_nova_remessa:
                print("A abrir a janela de remessas, vamos lá criar uma nova remessa!")
                estado.painel_nova_remessa_aberto = True
            #self.newWindow2 = tk.Toplevel(self.master)
            estado.janela_remessas = tk.Toplevel(self.master)
            estado.janela_remessas.geometry(WREMESSAS_GEOMETRIA)
            estado.janela_remessas.title('Remessas')
            self.janela_remessas = RemessasWindow(estado.janela_remessas, estado)
            estado.janela_remessas_aberta = True
            estado.janela_remessas.wm_protocol("WM_DELETE_WINDOW", lambda: self.close_window_remessas())
        else:
            if not criar_nova_remessa:
                self.close_window_remessas()
            else:
                estado.painel_nova_remessa_aberto = True
                self.janela_remessas.mostrar_painel_entrada()


    def close_window_remessas(self, *event):
        root.update_idletasks()
        print("a fechar janela")
        estado.janela_remessas_aberta = False
        estado.painel_nova_remessa_aberto = False
        estado.janela_remessas.destroy()


    def create_window_contacts(self, *event, criar_novo_contacto=None):
        #estado.contacto_para_nova_reparacao = nova_reparacao
        estado.tipo_novo_contacto = criar_novo_contacto

        if not estado.janela_contactos_aberta:
            if criar_novo_contacto in ["Cliente", "Fornecedor"]:
                print("Sim:", criar_novo_contacto)
                estado.painel_novo_contacto_aberto = True
            estado.janela_contactos = tk.Toplevel(self.master)
            estado.janela_contactos.geometry(WCONTACTOS_GEOMETRIA)
            estado.janela_contactos.title('Contactos')
            self.janela_contactos = ContactsWindow(estado.janela_contactos, estado)
            estado.janela_contactos_aberta = True
            estado.janela_contactos.wm_protocol("WM_DELETE_WINDOW", lambda: self.close_window_contactos())
        else:
            if not criar_novo_contacto:
                self.close_window_contactos()
            else:
                estado.painel_novo_contacto_aberto = True
                self.janela_contactos.mostrar_painel_entrada()


    def close_window_contactos(self, *event):
        root.update_idletasks()
        if estado.contacto_para_nova_reparacao:
            if estado.tipo_novo_contacto == "Cliente":
                self.ef_txt_num_cliente.delete(0, tk.END)
                self.ef_txt_num_cliente.insert(0, estado.contacto_para_nova_reparacao)
            elif estado.tipo_novo_contacto == "Fornecedor":
                self.ef_txt_num_fornecedor.delete(0, tk.END)
                self.ef_txt_num_fornecedor.insert(0, estado.contacto_para_nova_reparacao)
            else:
                print("Qual é afinal o tipo de contacto a criar???")

        estado.janela_contactos_aberta = False
        estado.painel_novo_contacto_aberto = False
        estado.janela_contactos.destroy()
        self.ef_ltxt_descr_equipamento.scrolledtext.focus()


    def abrir_painel_mensagens(self, *event):
        root.update_idletasks()

        if estado.painel_mensagens_aberto == False:
            self.estilo = ttk.Style()

            self.mensagens_frame = ttk.Frame(self.messagepane)
            self.mensagens_frame.pack()

            self.mensagens_frame_top = ttk.Frame(self.mensagens_frame, padding="4 10 4 4")

            contar_mensagens = 36 #TODO: implementar método para obter o número de mensagens do utilizador
            self.lbl_mensagens_titulo = ttk.Label(self.mensagens_frame, text=f"{contar_mensagens} mensagens", anchor='center', font=("Lucida Grande", 18)).pack()
            #ttk.Separator(self.messagepane, orient=tk.HORIZONTAL).pack(fill="x")
            self.mensagens_frame_btn = ttk.Frame(self.mensagens_frame, padding="2 4 2 2")
            self.mensagens_frame_tree = ttk.Frame(self.mensagens_frame, padding="2 5 2 2")

            self.btn_msg_mostrar = ttk.Button(self.mensagens_frame_btn, text="Mostrar")
            self.btn_msg_mostrar.grid(column=0, sticky=tk.W, row=1, in_=self.mensagens_frame_btn)

            self.btn_msg_apagar_um = ttk.Button(self.mensagens_frame_btn, text="Apagar")
            self.btn_msg_apagar_um.grid(column=1, sticky=tk.E, row=1, in_=self.mensagens_frame_btn)

            self.btn_msg_apagar_tudo = ttk.Button(self.mensagens_frame_btn, text="Apagar tudo")
            self.btn_msg_apagar_tudo.grid(column=3, sticky=tk.E, row=1, in_=self.mensagens_frame_btn)

            self.mensagens_frame_btn.grid_columnconfigure(0, weight=0)
            self.mensagens_frame_btn.grid_columnconfigure(1, weight=0)
            self.mensagens_frame_btn.grid_columnconfigure(2, weight=1)
            self.mensagens_frame_btn.grid_columnconfigure(3, weight=0)

            self.lblFrame_mensagens = ttk.LabelFrame(self.mensagens_frame_tree,labelanchor="s", padding="4 4 4 4")

            self.msgtree = ttk.Treeview(self.lblFrame_mensagens, height=31, selectmode='browse', show='', style='Msg.Treeview')
            self.msgtree['columns'] = ('ico','Processo', 'Mensagem')
            #self.msgtree.pack(side=tk.TOP, fill=tk.BOTH)
            self.msgtree.column('#0', anchor='w', minwidth=0, stretch=0, width=0)
            self.msgtree.column('ico', anchor='ne', minwidth=20, stretch=0, width=20)
            self.msgtree.column('Processo', anchor='ne', minwidth=40, stretch=0, width=40)
            self.msgtree.column('Mensagem', anchor='nw', minwidth=235, stretch=1, width=235)
            self.lblFrame_mensagens.grid_columnconfigure(2, weight=1)

            self.bind_tree()


            self.msgtree.grid(column=0, columnspan=4, row=2, sticky=tk.N+tk.W+tk.E)
            # Barra de deslocação para a tabela
            #self.vsb2 = AutoScrollbar(self.tab_mensagens, orient="vertical", command=self.msgtree.yview)
            #self.msgtree.configure(yscrollcommand=self.vsb2.set)
            #self.vsb2.grid(column=1, row=0, sticky=tk.N+tk.S, in_=self.tab_mensagens)


            self.estilo.configure('Msg.Treeview', font=("Lucida Grande", 10), foreground="grey22", fieldbackground="grey89", anchor='n', background='grey91', rowheight=72)

            #estilo.configure('Msg.Treeview.Heading', font=("Lucida Grande", 9), foreground="grey22")
            #estilo.configure( 'Msg.Treeview', relief = 'flat', borderwidth = 0)

            self.mensagens_frame_top.pack(side=tk.TOP)
            self.mensagens_frame_btn.pack(side=tk.TOP)
            self.mensagens_frame_tree.pack(side=tk.TOP)
            self.lblFrame_mensagens.pack()
            self.mensagens_frame.pack()
            self.messagepane.pack()
            self.rightframe.grid()

            self.inserir_msgs_de_exemplo()
            self.alternar_cores(self.msgtree, inverso=False, fundo1='grey96')
            estado.painel_mensagens_aberto = True
        else:
            self.fechar_painel_mensagens()


    def fechar_painel_mensagens(self, *event):
        root.update_idletasks()
        self.messagepane.pack_forget()
        self.mensagens_frame.destroy()
        self.rightframe.grid_remove()
        estado.painel_mensagens_aberto = False


    def mostrar_painel_entrada(self, *event):
        self.MenuFicheiro.entryconfig("Nova reparação", state="disabled")
        #root.unbind_all("<Command-n>")
        self.show_entryform()
        estado.painel_nova_reparacao_aberto = self.is_entryform_visible
        self.ef_txt_num_cliente.focus()
        self.entryframe.bind_all("<Command-Escape>", self.fechar_painel_entrada)


    def fechar_painel_entrada(self, *event):
        #self.clear_text()
        self.hide_entryform()
        estado.painel_nova_reparacao_aberto = self.is_entryform_visible
        #root.bind_all("<Command-n>")


    def gerar_painel_entrada(self):

        #entryfr1-----------------------------
        #TODO:adicionar campos, notebook, etc
        #criar funções para usar esses campos, ora para adicionar, ora para editar, ora para visualizar registos
        self.ef_var_tipo = tk.IntVar()
        self.ef_var_estado = tk.IntVar()
        self.ef_var_garantia = tk.IntVar()
        self.ef_var_repr_loja = tk.IntVar()
        self.ef_var_repr_loja.set(0)
        self.ef_var_efetuar_copia = tk.IntVar()
        self.ef_var_find_my = tk.IntVar()
        self.ef_var_local_intervencao = tk.IntVar()
        self.ef_var_local_intervencao.set("Loja X")

        self.ef_cabecalho = ttk.Frame(self.entryfr1, padding=4)
        self.ef_lbl_titulo = ttk.Label(self.ef_cabecalho, style="BW.TLabel", text="Adicionar Reparação:\n")
        self.ef_lbl_tipo = ttk.Label(self.ef_cabecalho, text="Tipo de processo:")
        self.ef_radio_tipo_cliente = ttk.Radiobutton(self.ef_cabecalho, text="Cliente", variable=self.ef_var_tipo, value=TIPO_REP_CLIENTE, command=self.radio_tipo_command)
        self.ef_radio_tipo_stock = ttk.Radiobutton(self.ef_cabecalho, text="Stock", variable=self.ef_var_tipo, value=TIPO_REP_STOCK, command=self.radio_tipo_command)
        self.btn_adicionar = ttk.Button(self.ef_cabecalho, text="Adicionar", command=None)
        self.btn_cancelar = ttk.Button(self.ef_cabecalho, text="Cancelar", command=self.fechar_painel_entrada)


        self.ef_lbl_titulo.grid(column=0, row=0, columnspan=3, sticky='w')
        self.ef_lbl_tipo.grid(column=0, row=1, sticky='e')
        self.ef_radio_tipo_cliente.grid(column=1, row=1, sticky='w')
        self.ef_radio_tipo_stock.grid(column=2, row=1, sticky='w')
        self.btn_adicionar.grid(column=3, row=1, sticky='we')
        self.btn_cancelar.grid(column=3, row=2, sticky='we')

        self.ef_cabecalho.grid(column=0,row=0, sticky='we')
        self.entryfr1.columnconfigure(0, weight=1)
        #self.ef_cabecalho.columnconfigure(0, weight=0)
        self.ef_cabecalho.columnconfigure(2, weight=1)

        #self.btn_adicionar.bind('<Button-1>', self.add_remessa)


        #entryfr2-----------------------------
        self.ef_lf_cliente = ttk.Labelframe(self.entryfr2, padding=4, text="Dados do cliente")
        self.ef_txt_num_cliente = ttk.Entry(self.ef_lf_cliente, width=5)
        self.ef_btn_buscar_cliente = ttk.Button(self.ef_lf_cliente, width=1, text="+", command=lambda *x: self.create_window_contacts(criar_novo_contacto="Cliente"))
        self.ef_txt_nome_cliente = ttk.Entry(self.ef_lf_cliente, width=45)
        self.ef_lbl_telefone_lbl = ttk.Label(self.ef_lf_cliente, text="Tel.:")
        self.ef_lbl_telefone_info = ttk.Label(self.ef_lf_cliente, text="00 351 000 000 000")
        self.ef_lbl_email_lbl = ttk.Label(self.ef_lf_cliente, text="Email:")
        self.ef_lbl_email_info = ttk.Label(self.ef_lf_cliente, text="email.address@portugalmail.com")

        self.ef_lf_fornecedor = ttk.Labelframe(self.entryfr2, padding=4, text="Dados do fornecedor")
        self.ef_txt_num_fornecedor = ttk.Entry(self.ef_lf_fornecedor, width=5)
        self.ef_btn_buscar_fornecedor = ttk.Button(self.ef_lf_fornecedor, width=1, text="+", command=lambda *x: self.create_window_contacts(criar_novo_contacto="Fornecedor"))
        self.ef_txt_nome_fornecedor = ttk.Entry(self.ef_lf_fornecedor, width=45)
        self.ef_lbl_telefone_lbl_fornecedor = ttk.Label(self.ef_lf_fornecedor, text="Tel.:")
        self.ef_lbl_telefone_info_fornecedor = ttk.Label(self.ef_lf_fornecedor, text="00 351 000 000 000")
        self.ef_lbl_email_lbl_fornecedor = ttk.Label(self.ef_lf_fornecedor, text="Email:")
        self.ef_lbl_email_info_fornecedor = ttk.Label(self.ef_lf_fornecedor, text="email.address@portugalmail.com")

        self.ef_txt_num_cliente.grid(column=0, row=0, padx=5, sticky='w')
        self.ef_btn_buscar_cliente.grid(column=2, row=0, sticky='w')
        self.ef_txt_nome_cliente.grid(column=3, row=0,  padx=5, sticky='w')
        self.ef_lbl_telefone_lbl.grid(column=5, row=0, padx=5, sticky='e')
        self.ef_lbl_telefone_info.grid(column=6, row=0, padx=5,  sticky='w')
        self.ef_lbl_email_lbl.grid(column=7, row=0,  padx=5, sticky='e')
        self.ef_lbl_email_info.grid(column=8, row=0,  padx=5, sticky='w')

        self.ef_txt_num_fornecedor.grid(column=0, row=0, padx=5, sticky='w')
        self.ef_btn_buscar_fornecedor.grid(column=2, row=0, sticky='w')
        self.ef_txt_nome_fornecedor.grid(column=3, row=0,  padx=5, sticky='w')
        self.ef_lbl_telefone_lbl_fornecedor.grid(column=5, row=0,  padx=5, sticky='e')
        self.ef_lbl_telefone_info_fornecedor.grid(column=6, row=0,  padx=5, sticky='w')
        self.ef_lbl_email_lbl_fornecedor.grid(column=7, row=0,  padx=5, sticky='e')
        self.ef_lbl_email_info_fornecedor.grid(column=8, row=0,  padx=5, sticky='w')

        self.ef_lf_cliente.grid(column=0,row=0, sticky='we')
        self.entryfr2.columnconfigure(0, weight=1)

        self.ef_lf_cliente.columnconfigure(2, weight=0)
        self.ef_lf_cliente.columnconfigure(3, minsize=50, weight=1)
        self.ef_lf_cliente.columnconfigure(4, weight=1)
        self.ef_lf_cliente.columnconfigure(6, weight=1)
        self.ef_lf_cliente.columnconfigure(8, weight=1)

        self.ef_lf_fornecedor.columnconfigure(2, weight=0)
        self.ef_lf_fornecedor.columnconfigure(3, minsize=50, weight=1)
        self.ef_lf_fornecedor.columnconfigure(4, weight=1)
        self.ef_lf_fornecedor.columnconfigure(6, weight=1)
        self.ef_lf_fornecedor.columnconfigure(8, weight=1)


        #entryfr3-----------------------------
            #estabelecimento_compra (mostrar apenas se garantia for "sim, outro estabelecimento") c4
        self.ef_lf_equipamento = ttk.Labelframe(self.entryfr3, padding=4, text="\nDados do equipamento")
        self.ef_ltxt_descr_equipamento = LabelText(self.ef_lf_equipamento, "Descrição:", width=30, height=2)
        self.ef_lbl_estado_equipamento = ttk.Label(self.ef_lf_equipamento, text="Estado:")
        self.ef_radio_estado_marcas_uso = ttk.Radiobutton(self.ef_lf_equipamento, text="Marcas de uso", variable=self.ef_var_estado, value=0, command=self.radio_estado_command)
        self.ef_radio_estado_bom = ttk.Radiobutton(self.ef_lf_equipamento, text="Bom estado geral", variable=self.ef_var_estado, value=1, command=self.radio_estado_command)
        self.ef_radio_estado_marcas_acidente = ttk.Radiobutton(self.ef_lf_equipamento, text="Marcas de acidente", variable=self.ef_var_estado, value=2, command=self.radio_estado_command)
        self.ef_radio_estado_faltam_pecas = ttk.Radiobutton(self.ef_lf_equipamento, text="Faltam peças", variable=self.ef_var_estado, value=3, command=self.radio_estado_command)
        self.ef_ltxt_obs_estado_equipamento = LabelText(self.ef_lf_equipamento, "Observações acerca do estado:", width=27, height=2)

        self.ef_lbl_garantia = ttk.Label(self.ef_lf_equipamento, text="Garantia:")
        self.ef_radio_garantia_fora_garantia = ttk.Radiobutton(self.ef_lf_equipamento, text="Fora de garantia", variable=self.ef_var_garantia, value=0, command=self.radio_garantia_command)
        self.ef_radio_garantia_neste = ttk.Radiobutton(self.ef_lf_equipamento, text="Sim, neste estabelecimento", variable=self.ef_var_garantia, value=1, command=self.radio_garantia_command)
        self.ef_radio_garantia_noutro = ttk.Radiobutton(self.ef_lf_equipamento, text="Sim, noutro estabelecimento", variable=self.ef_var_garantia, value=2, command=self.radio_garantia_command)

        self.ef_ltxt_cod_artigo = LabelEntry(self.ef_lf_equipamento, "\nCódigo de artigo:", width=15)
        self.ef_ltxt_num_serie = LabelEntry(self.ef_lf_equipamento, "\nNº de série:", width=15)
        self.ef_ltxt_data_compra = LabelEntry(self.ef_lf_equipamento, "\nData de compra:", width=15)
        self.ef_ltxt_num_fatura = LabelEntry(self.ef_lf_equipamento, "\nNº da fatura:", width=15)
        self.ef_ltxt_local_compra = LabelEntry(self.ef_lf_equipamento, "\nEstabelecimento:", width=15)

        self.ef_ltxt_num_fatura_fornecedor = LabelEntry(self.ef_lf_equipamento, "Nº fatura fornecedor:", width=15)
        self.ef_ltxt_data_fatura_fornecedor = LabelEntry(self.ef_lf_equipamento, "Data fatura fornecedor:", width=15)
        self.ef_ltxt_nar = LabelEntry(self.ef_lf_equipamento, "NAR:", width=15)
        self.ef_ltxt_num_guia_rececao = LabelEntry(self.ef_lf_equipamento, "Guia de receção:", width=15)
        self.ef_ltxt_data_entrada_stock = LabelEntry(self.ef_lf_equipamento, "Data de entrada em stock:", width=15)
        self.ef_ltxt_num_quebra_stock = LabelEntry(self.ef_lf_equipamento, "Nº de quebra de stock:", width=15)

        self.ef_ltxt_descr_equipamento.grid(column=0, columnspan=2, rowspan=5, row=0, padx=5, sticky='wen')
        self.ef_lbl_estado_equipamento.grid(column=2, row=0, padx=5, sticky='w')
        self.ef_radio_estado_marcas_uso.grid(column=2, row=1, padx=5, sticky='w')
        self.ef_radio_estado_bom.grid(column=2, row=2, padx=5, sticky='w')
        self.ef_radio_estado_marcas_acidente.grid(column=2, row=3, padx=5, sticky='w')
        self.ef_radio_estado_faltam_pecas.grid(column=2, row=4, padx=5, sticky='w')
        self.ef_ltxt_obs_estado_equipamento.grid(column=3, row=0, rowspan=5, padx=5, sticky='wen')
        self.ef_lbl_garantia.grid(column=4, row=0, padx=5, sticky='w')
        self.ef_radio_garantia_fora_garantia.grid(column=4, row=1, padx=5, sticky='w')
        self.ef_radio_garantia_neste.grid(column=4, row=2, padx=5, sticky='w')
        self.ef_radio_garantia_noutro.grid(column=4, row=3, padx=5, sticky='w')
        self.ef_ltxt_cod_artigo.grid(column=0, row=5, padx=5, sticky='we')
        self.ef_ltxt_num_serie.grid(column=1, row=5, padx=5, sticky='we')
        self.ef_ltxt_data_compra.grid(column=2, row=5, padx=5, sticky='we')
        self.ef_ltxt_num_fatura.grid(column=3, row=5, padx=5, sticky='we')

        self.ef_lf_equipamento.grid(column=0,row=0, sticky='we')
        self.entryfr3.columnconfigure(0, weight=1)

        self.ef_lf_equipamento.columnconfigure(0, weight=1)
        self.ef_lf_equipamento.columnconfigure(1, weight=1)
        self.ef_lf_equipamento.columnconfigure(2, weight=1)
        self.ef_lf_equipamento.columnconfigure(3, weight=1)
        self.ef_lf_equipamento.columnconfigure(4, weight=1)


        #entryfr4-----------------------------
        self.ef_lf_servico = ttk.Labelframe(self.entryfr4, padding=4, text="\nAvaria e/ou serviço a realizar")
        self.ef_text_descr_avaria_servico = ScrolledText(self.ef_lf_servico, highlightcolor="LightSteelBlue2", width=20, height=4)
        self.ef_chkbtn_avaria_reprod_loja = ttk.Checkbutton(self.ef_lf_servico, variable=self.ef_var_repr_loja, width=27, text="Avaria reproduzida na loja")
        self.ef_ltxt_senha = LabelEntry(self.ef_lf_servico, "Senha:", width=22)
        self.ef_lbl_find_my = ttk.Label(self.ef_lf_servico, width=27, text="Find my iPhone ativo?")
        self.ef_radio_find_my_sim = ttk.Radiobutton(self.ef_lf_servico, text="Sim", variable=self.ef_var_find_my, value=1, command=self.radio_find_my)
        self.ef_radio_find_my_nao = ttk.Radiobutton(self.ef_lf_servico, text="Não", variable=self.ef_var_find_my, value=0, command=self.radio_find_my)
        self.ef_radio_find_my_nao_aplic = ttk.Radiobutton(self.ef_lf_servico, text="Não aplicável", variable=self.ef_var_find_my, value=2, command=self.radio_find_my)
        self.ef_lbl_espaco = ttk.Label(self.ef_lf_servico, text=" ")
        self.ef_lbl_efetuar_copia = ttk.Label(self.ef_lf_servico, text="Efetuar cópia de segurança?")
        self.ef_radio_efetuar_copia_sim = ttk.Radiobutton(self.ef_lf_servico, text="Sim", variable=self.ef_var_efetuar_copia, value=1, command=self.radio_copia_command)
        self.ef_radio_efetuar_copia_nao = ttk.Radiobutton(self.ef_lf_servico, text="Não", variable=self.ef_var_efetuar_copia, value=0, command=self.radio_copia_command)
        self.ef_radio_efetuar_copia_n_aplic = ttk.Radiobutton(self.ef_lf_servico, text="Não aplicável", variable=self.ef_var_efetuar_copia, value=2, command=self.radio_copia_command)

        self.ef_text_descr_avaria_servico.grid(column=0, row=0, columnspan=3, rowspan=5, padx=5, sticky='wens')
        self.ef_chkbtn_avaria_reprod_loja.grid(column=3, row=0, columnspan=3, padx=5, sticky='nw')
        self.ef_ltxt_senha.grid(column=3, row=3, rowspan=2, columnspan=3, padx=5, sticky='w')
        self.ef_lbl_find_my.grid(column=6, row=0, columnspan=3, padx=5, sticky='nw')
        self.ef_radio_find_my_sim.grid(column=6, row=1, padx=5, sticky='nw')
        self.ef_radio_find_my_nao.grid(column=7, row=1, sticky='nw')
        self.ef_radio_find_my_nao_aplic.grid(column=8, row=1, sticky='nw')
        self.ef_lbl_espaco.grid(column=8, row=2, sticky='w')
        self.ef_lbl_efetuar_copia.grid(column=6, row=3, columnspan=3, padx=5, sticky='w')
        self.ef_radio_efetuar_copia_sim.grid(column=6, row=4, padx=5, sticky='w')
        self.ef_radio_efetuar_copia_nao.grid(column=7, row=4, sticky='w')
        self.ef_radio_efetuar_copia_n_aplic.grid(column=8, row=4, sticky='w')

        self.ef_lf_servico.grid(column=0,row=0, sticky='we')
        self.entryfr4.columnconfigure(0, weight=1)

        self.ef_lf_servico.columnconfigure(0, weight=1)

        #entryfr5-----------------------------
            #Notas: text 3 linhas
            # local intervenção lbl + combobox(contactos>fornecedores)
        self.ef_lf_outros_dados = ttk.Labelframe(self.entryfr5, padding=4, text="\nOutros dados")
        self.ef_ltxt_acessorios_entregues = LabelText(self.ef_lf_outros_dados, "Acessórios entregues:", height=3)
        #self.ef_lbl_espaco = ttk.Label(self.ef_lf_outros_dados, text="  ")
        self.ef_ltxt_notas = LabelText(self.ef_lf_outros_dados, "Notas:", height=3)
        self.ef_lbl_local_intervencao = ttk.Label(self.ef_lf_outros_dados, width=27,  text="Local de intervenção:")
        self.ef_combo_local_intervencao = ttk.Combobox(self.ef_lf_outros_dados,
                                                       width=21,
                                                       textvariable=self.ef_var_local_intervencao,
                                                       values=("Loja X",
                                                               "Importador Nacional A",
                                                               "Distribuidor Ibérico Y",
                                                               "Centro de assistência N",
                                                               "Centro de assistência P",
                                                               "Centro de assistência K"),
                                                       state='readonly')  # TODO: Obter estes valores a partir da base de dados, a utilizar também no formulário de Remessas.

        self.ef_ltxt_acessorios_entregues.grid(column=0, row=0, rowspan=3, padx=5, sticky='wen')
        self.ef_ltxt_notas.grid(column=1, row=0, rowspan=3, padx=5, sticky='wen')
        self.ef_lbl_local_intervencao.grid(column=2, row=0, padx=5, sticky='nw')
        self.ef_combo_local_intervencao.grid(column=2, row=1, padx=5, sticky='nwe')

        self.ef_lf_outros_dados.grid(column=0,row=0, sticky='we')
        self.entryfr5.columnconfigure(0, weight=1)

        self.ef_lf_outros_dados.columnconfigure(0, weight=1)
        self.ef_lf_outros_dados.columnconfigure(1, weight=1)
        self.ef_lf_outros_dados.columnconfigure(2, weight=0)

        #--- acabaram os 'entryfr', apenas código geral para o entryframe a partir daqui ---
        self.entryframe.bind_all("<Command-Escape>", self.fechar_painel_entrada)


    def radio_tipo_command(self, *event):
        """
        Ajustes que devem ocorrer no formulário quando o utilizador altera o tipo de
        reparação (artigo de cliente ou de stock).
        """
        tipo = self.ef_var_tipo.get()
        if tipo == TIPO_REP_STOCK:
            self.ef_lf_cliente.grid_remove()
            self.ef_lf_fornecedor.grid(column=0,row=0, sticky='we')

            self.ef_ltxt_descr_equipamento.scrolledtext.configure(height=7)
            self.ef_ltxt_descr_equipamento.grid_configure(rowspan=8)
            
            self.ef_lbl_estado_equipamento.grid_remove()
            self.ef_radio_estado_marcas_uso.grid_remove()
            self.ef_radio_estado_bom.grid_remove()
            self.ef_radio_estado_marcas_acidente.grid_remove()
            self.ef_radio_estado_faltam_pecas.grid_remove()
            self.ef_ltxt_obs_estado_equipamento.grid_remove()
            self.ef_lbl_garantia.grid_remove()
            self.ef_radio_garantia_fora_garantia.grid_remove()
            self.ef_radio_garantia_neste.grid_remove()
            self.ef_radio_garantia_noutro.grid_remove()
            self.ef_ltxt_data_compra.grid_remove()
            self.ef_ltxt_num_fatura.grid_remove()
            self.ef_ltxt_local_compra.grid_remove()

            self.ef_chkbtn_avaria_reprod_loja.grid_remove()
            self.ef_ltxt_senha.grid_remove()
            self.ef_lbl_find_my.grid_remove()
            self.ef_radio_find_my_sim.grid_remove()
            self.ef_radio_find_my_nao.grid_remove()
            self.ef_radio_find_my_nao_aplic.grid_remove()
            self.ef_lbl_efetuar_copia.grid_remove()
            self.ef_radio_efetuar_copia_nao.grid_remove()
            self.ef_radio_efetuar_copia_sim.grid_remove()
            self.ef_radio_efetuar_copia_n_aplic.grid_remove()

            self.ef_ltxt_acessorios_entregues.grid_remove()
            self.ef_lbl_local_intervencao.grid_remove()
            self.ef_combo_local_intervencao.grid_remove()

            self.ef_ltxt_notas.grid(column=0, row=0, columnspan=3, rowspan=3, padx=5, sticky='wens')
            self.ef_lf_outros_dados.configure(text="\nNotas")
            self.ef_ltxt_notas.label.pack_forget()
            
            self.ef_ltxt_num_serie.label.configure(text="Nº de série")
            self.ef_ltxt_cod_artigo.label.configure(text="Código de artigo")
            self.ef_ltxt_cod_artigo.grid(column=2, row=0, rowspan=2, padx=5, sticky='we')
            self.ef_ltxt_num_serie.grid(column=2, row=2, rowspan=2, padx=5, sticky='we')
            self.ef_ltxt_num_fatura_fornecedor.grid(column=3, rowspan=2, row=0, padx=5, sticky='we')
            self.ef_ltxt_data_fatura_fornecedor.grid(column=3, row=2, rowspan=2, padx=5, sticky='we')
            self.ef_ltxt_nar.grid(column=3, row=4, rowspan=2, padx=5, sticky='we')
            self.ef_ltxt_num_guia_rececao.grid(column=4, row=0, rowspan=2, padx=5, sticky='we')
            self.ef_ltxt_data_entrada_stock.grid(column=4, row=2, rowspan=2, padx=5, sticky='we')
            self.ef_ltxt_num_quebra_stock.grid(column=4, row=4, rowspan=2, padx=5, sticky='we')
            self.ef_txt_num_fornecedor.focus()
        else:
            self.ef_lf_fornecedor.grid_remove()
            self.ef_lf_cliente.grid()

            self.ef_ltxt_descr_equipamento.scrolledtext.configure(height=4)
            self.ef_ltxt_descr_equipamento.grid_configure(rowspan=5)


            self.ef_lbl_estado_equipamento.grid()
            self.ef_radio_estado_marcas_uso.grid()
            self.ef_radio_estado_bom.grid()
            self.ef_radio_estado_marcas_acidente.grid()
            self.ef_radio_estado_faltam_pecas.grid()
            self.ef_ltxt_obs_estado_equipamento.grid()
            self.ef_lbl_garantia.grid()
            self.ef_radio_garantia_fora_garantia.grid()
            self.ef_radio_garantia_neste.grid()
            self.ef_radio_garantia_noutro.grid()
            self.ef_ltxt_data_compra.grid()
            self.ef_ltxt_num_fatura.grid()

            self.radio_garantia_command()

            self.ef_chkbtn_avaria_reprod_loja.grid()
            self.ef_ltxt_senha.grid()
            self.ef_lbl_find_my.grid()
            self.ef_radio_find_my_sim.grid()
            self.ef_radio_find_my_nao.grid()
            self.ef_radio_find_my_nao_aplic.grid()
            self.ef_lbl_efetuar_copia.grid()
            self.ef_radio_efetuar_copia_nao.grid()
            self.ef_radio_efetuar_copia_sim.grid()
            self.ef_radio_efetuar_copia_n_aplic.grid()

            self.ef_ltxt_nar.grid_remove()
            self.ef_ltxt_num_fatura_fornecedor.grid_remove()
            self.ef_ltxt_data_fatura_fornecedor.grid_remove()
            self.ef_ltxt_num_guia_rececao.grid_remove()
            self.ef_ltxt_data_entrada_stock.grid_remove()
            self.ef_ltxt_num_quebra_stock.grid_remove()
            self.ef_ltxt_num_serie.label.configure(text="\nNº de série")
            self.ef_ltxt_cod_artigo.label.configure(text="\nCódigo de artigo")
            self.ef_ltxt_cod_artigo.grid(column=0, row=5, padx=5, sticky='we')
            self.ef_ltxt_num_serie.grid(column=1, row=5, padx=5, sticky='we')

            self.ef_lf_outros_dados.configure(text="\nOutros dados")
            self.ef_ltxt_notas.label.configure(text="Notas:")
            self.ef_ltxt_acessorios_entregues.grid()
            self.ef_lbl_local_intervencao.grid()
            self.ef_combo_local_intervencao.grid()
            
            self.ef_ltxt_notas.scrolledtext.pack_forget()
            self.ef_ltxt_notas.label.pack(side="top", fill="x", expand=True)
            self.ef_ltxt_notas.scrolledtext.pack(side="top",fill="x", expand=True)
            
            self.ef_ltxt_notas.grid(column=1, row=0, columnspan=1, rowspan=3, padx=5, sticky='wens')
            self.ef_txt_num_cliente.focus()


    def radio_estado_command(self, *event):
        print("RadioButton Estado Changed. New value:", self.ef_var_estado.get()) # obter o valor do campo "estado"


    def radio_garantia_command(self, *event):
        """
        Ajustes que devem ocorrer no formulário quando o utilizador altera o
        estado da elegibilidade para garantia.
        """
        garantia = self.ef_var_garantia.get()
        if garantia == GARANTIA_NOUTRO:
            self.ef_ltxt_local_compra.grid(column=4, row=5, padx=5, sticky='we')
        else:
            self.ef_ltxt_local_compra.grid_remove()


    def radio_copia_command(self, *event):
        print("RadioButton Cópia de Segurança Changed. New value:", self.ef_var_efetuar_copia.get()) # obter o valor do campo "cópia"

    def radio_find_my(self, *event):
        print("RadioButton Find my iPhone Changed. New value:", self.ef_var_find_my.get()) # obter o valor do campo "cópia"


    def gerar_menu(self):
        # Menu da janela principal
        self.menu = tk.Menu(root)
        root.config(menu=self.menu)

        self.MenuFicheiro = tk.Menu(self.menu, postcommand=self.liga_desliga_menu_novo)

        self.menu.add_cascade(label="Ficheiro", menu=self.MenuFicheiro)
        self.MenuFicheiro.add_command(label="Nova reparação", command=self.mostrar_painel_entrada, accelerator="Command+n")
        self.MenuFicheiro.add_command(label="Novo contacto", command=lambda *x: self.create_window_contacts(criar_novo_contacto="Cliente"), accelerator="Command+t")
        self.MenuFicheiro.add_command(label="Nova remessa", command=lambda *x: self.create_window_remessas(criar_nova_remessa=True), accelerator="Command+r")
        self.MenuFicheiro.add_separator()
        self.MenuFicheiro.add_command(label="Pesquisar...", command=None, accelerator="Command+f")
        root.bind_all("<Command-n>", self.mostrar_painel_entrada)
        root.bind_all("<Command-t>", lambda *x: self.create_window_contacts(criar_novo_contacto="Cliente"))
        root.bind_all("<Command-r>", lambda *x: self.create_window_remessas(criar_nova_remessa=True))


        self.menuVis = tk.Menu(self.menu)
        self.menu.add_cascade(label="Visualização", menu=self.menuVis)
        self.menuVis.add_command(label="Mostrar/ocultar mensagens", command=self.abrir_painel_mensagens, accelerator="Command-1")
        self.menuVis.add_command(label="Mostrar/ocultar contactos", command=self.create_window_contacts, accelerator="Command-2")
        self.menuVis.add_command(label="Mostrar/ocultar remessas", command=self.create_window_remessas, accelerator="Command-3")
        self.menuVis.bind_all("<Command-KeyPress-1>", self.abrir_painel_mensagens)
        self.menuVis.bind_all("<Command-KeyPress-2>", self.create_window_contacts)
        self.menuVis.bind_all("<Command-KeyPress-3>", self.create_window_remessas)

        self.windowmenu = tk.Menu(self.menu, name='window')
        self.menu.add_cascade(menu=self.windowmenu, label='Janela')
        self.windowmenu.add_separator()
        #self.windowmenu.add_command(label="Fechar", command=self.fechar_janela_ativa, accelerator="Command-w") ###fechar janela ativa cmd-w


        self.helpmenu = tk.Menu(self.menu)
        self.menu.add_cascade(label="Help", menu=self.helpmenu)
         #       helpmenu.add_command(label="Preferências", command=About)
        self.helpmenu.add_command(label="Acerca de "+__app_name__, command=about_window)
        self.helpmenu.add_command(label="Suporte da aplicação "+__app_name__, command=lambda: webbrowser.open("http://victordomingos.com/contactos/", new=1, autoraise=True))
        self.helpmenu.add_command(label="Agradecimentos", command=thanks_window)
        self.helpmenu.add_separator()
        self.helpmenu.add_command(label="Visitar página do autor", command=lambda: webbrowser.open("http://victordomingos.com", new=1, autoraise=True))
        #root.createcommand('::tk::mac::ShowPreferences', prefs_function)
        #root.bind('<<about-idle>>', about_dialog)
        #root.bind('<<open-config-dialog>>', config_dialog)
        root.createcommand('tkAboutDialog', about_window)

        """
        #----------------Menu contextual tabela principal---------------------
        self.contextMenu = Menu(self.menu)
        self.contextMenu.add_command(label="Informações", command=self.mostrar_detalhe)
        self.contextMenu.add_command(label="Abrir no site da transportadora", command=self.abrir_url_browser)
        self.contextMenu.add_separator()
        self.contextMenu.add_command(label="Copiar número de objeto", command=self.copiar_obj_num)
        self.contextMenu.add_command(label="Copiar mensagem de expedição", command=self.copiar_msg)
        self.contextMenu.add_separator()
        self.contextMenu.add_command(label="Arquivar/restaurar remessa", command=self.del_remessa)
        self.contextMenu.add_separator()
        self.contextMenu.add_command(label="Registar cheque recebido", command=self.pag_recebido)
        self.contextMenu.add_command(label="Registar cheque depositado", command=self.chq_depositado)
        """

    def liga_desliga_menu_novo(self, *event):
        """
        Liga e desliga menus com base na configuração atual da janela. Por exemplo, ao
        abrir o painel de entrada de dados, desativa o menu "nova reparação", para evitar
        que o painel se feche inadvertidamente.
        """
        if self.is_entryform_visible == True:
            self.MenuFicheiro.entryconfigure("Nova reparação", state="disabled")
            # TODO - corrigir bug: o atalho de teclado só fica realmente inativo depois de acedermos ao menu ficheiro. Porquê??
            #root.unbind_all("<Command-n>")
        else:
            self.MenuFicheiro.entryconfigure("Nova reparação", state="active")
            #root.bind_all("<Command-n>")


    def inserir_msg(self, processo, utilizador, data, texto):
        processo = str(processo)
        str_data = f"{data.day}/{data.month}/{data.year} às {data.hour}:{int(data.minute):02}"
        texto = textwrap.fill(texto, width=45)
        texto_final = f"{utilizador}, {str_data}\n﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘\n{texto}"
        #texto_final = f"[{utilizador}, {str_data}]\n﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘\n{texto}"
        ico = "✉️"
        self.msgtree.insert("", "end", values=(ico, processo, texto_final))


    def inserir_dados_de_exemplo(self):
        for i in range(15):
            self.tree.insert("", "end", tag="", text="", values=("12000","José Manuel da Silva Rodrigues", "Artigo Muito Jeitoso (Early 2015)", "Substituição de ecrã", "Em processamento", "120" ))
            self.tree.insert("", "end", text="", values=("12000","Joana Manuela Rodrigues", "Outro Artigo Bem Jeitoso", "Bateria não carrega", "Aguarda envio", "120" ))
            self.tree.insert("", "end", tag="baixa", text="", values=("1004","Maria Apolinário Gomes Fernandes", "Smartphone Daqueles Bons", "Substituição de ecrã", "Enviado", "15" ))
            self.tree.insert("", "end", text="", tag="normal", values=("2001","José Carvalho", "Computador do modelo ABCD", "Formatar disco e reinstalar sistema operativo", "Recebido", "1" ))
            self.tree.insert("", "end", text="", tag="urgente", values=("702","Loja X", "Coisa que não funciona devidamente", "Substituição ao abrigo da garantia", "Aguarda entrega", "12" ))
            self.tree.insert("", "end", text="", tag="baixa", values=("30002","Loja X", "Coisa que devia funcionar melhor", "Substituição ao abrigo da garantia", "Entregue", "12" ))


    def inserir_msgs_de_exemplo(self):
        now = datetime.datetime.now()
        for i in range(3):
            utilizadores = ["Victor Domingos", "DJ Mars", "AC", "NPK"]
            processo0 = 23456
            processo1 = 21345
            processo2 = 99000
            processo3 = 1234

            insert_txt0 = "Convém ligar a este cliente no dia x de dezembro para verificar qual a morada para onde é para enviar"
            insert_txt1 = "Ligar ao cliente a explicar processo para fazer isto ou aquilo"
            insert_txt2 = "Verificar estado com centro de assistência"
            insert_txt3 = "Verificar estado com centro de assistência. O cliente vai enviar fatura para ver se dá para passar em garantia."

            self.inserir_msg(processo0, utilizadores[0], now, insert_txt0)
            self.inserir_msg(processo1, utilizadores[1], now, insert_txt1)
            self.inserir_msg(processo2, utilizadores[2], now, insert_txt2)
            self.inserir_msg(processo3, utilizadores[3], now, insert_txt3)


if __name__ == "__main__":
    root = tk.Tk()
    estado = AppStatus()
    estado.janela_principal = App(root)
    root.configure(background='grey95')
    root.title('RepService')
    root.geometry(WROOT_GEOMETRIA)
    root.bind_all("<Mod2-q>", exit)
    root.mainloop()
