#!/usr/bin/env python3.6
# encoding: utf-8
"""
Aplicação de base de dados para registo de processos de garantia e reparações.
Permite manter um registo dos artigos entregues pelos clientes, do seu
percurso durante a tramitação do processo e da comunicação realizada.

Os processos que requerem atenção, devido a atrasos na entrega ou na receção de
comunicação de cliente são destacados na lista principal, por forma a permitir
uma intervenção em conformidade.

Desenvolvido em Python 3 por Victor Domingos (http://victordomingos.com), com
muitas noites em claro, a partir de uma ideia original de Márcio Araújo.

© 2017 Victor Domingos, Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)
"""
import tkinter as tk
import tkinter.font
from tkinter import ttk, messagebox
from tkinter.scrolledtext import ScrolledText
import datetime
import time
import textwrap
import Pmw
import io
import sys  # For Atom compatibility

import about_window, contactos, remessas, detalhe_reparacao, detalhe_mensagem
import imprimir
from base_app import baseApp, AppStatus
from extra_tk_classes import AutocompleteEntry, AutoScrollbar, LabelEntry
from extra_tk_classes import LabelText, StatusBar
from global_setup import *

if USE_LOCAL_DATABASE:
    import db_local_main as db
else:
    import db_remote as db


__app_name__ = "RepService 2017"
__author__ = "Victor Domingos"
__copyright__ = "Copyright 2017 Victor Domingos"
__license__ = "Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)"
__version__ = "v0.16 development"
__email__ = "web@victordomingos.com"
__status__ = "Development"


class App(baseApp):
    """ base class for application """

    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master = master
        self.master.minsize(MASTER_MIN_WIDTH, MASTER_MIN_HEIGHT)
        self.master.maxsize(MASTER_MAX_WIDTH, MASTER_MAX_HEIGHT)
        self.a_editar_reparacao = False
        self.rep_newDetailsWindow = {}
        self.rep_detail_windows_count = 0
        self.msg_newDetailsWindow = {}
        self.msg_detail_windows_count = 0
        self.nprocessos = 0
        self.nmensagens = 0
        self.reparacao_selecionada = None
        self.mensagem_selecionada = None
        self.ultima_reparacao = None
        self.username = None
        self.password = None
        self.loggedin = False
        self.token = None
        self.failed_login_attempts = 0
        self.start_login_window()

    def start_login_window(self):
        self.root_login = tk.Toplevel()
        self.root_login.minsize(LOGIN_MIN_WIDTH, LOGIN_MIN_HEIGHT)
        self.root_login.maxsize(LOGIN_MAX_WIDTH, LOGIN_MAX_HEIGHT)
        self.root_login.configure(background='grey92')
        self.root_login.title('Login')
        self.root_login.bind_all("<Mod2-q>", self.master.quit)

        self.log_mainframe = ttk.Frame(self.root_login, padding="12 25 12 0")
        self.log_topframe = ttk.Frame(self.log_mainframe, padding="5 8 5 0")
        self.log_centerframe = ttk.Frame(self.log_mainframe)

        self.log_bottomframe = ttk.Frame(self.log_mainframe)
        self.log_btnFont = tkinter.font.Font(family="Lucida Grande", size=10)
        self.log_btnTxtColor = "grey22"
        self.log_btnTxtColor_active = "white"

        w = self.root_login.winfo_screenwidth()
        h = self.root_login.winfo_screenheight()

        size = tuple(int(_)
                     for _ in self.root_login.geometry().split('+')[0].split('x'))
        x = int(w / 2 - LOGIN_MIN_WIDTH / 2)
        y = int(h / 3 - LOGIN_MIN_HEIGHT / 2)
        self.root_login.geometry(
            f"{LOGIN_MIN_WIDTH}x{LOGIN_MIN_HEIGHT}+{x}+{y}")

        self.log_ltxt_username = LabelEntry(self.log_centerframe,
                                            label="Nome de Utilizador",
                                            width=30)

        self.log_ltxt_password = LabelEntry(self.log_centerframe,
                                            label="Palavra-passe",
                                            width=30)
        self.log_ltxt_password.entry.config(show="•")

        self.log_btn_alterar_senha = ttk.Button(self.log_centerframe,
                                                text="Alterar palavra-passe…",
                                                command=self.change_password)

        self.log_btn_cancel = ttk.Button(self.log_centerframe,
                                         text="Cancelar",
                                         command=exit)

        self.log_btn_enter = ttk.Button(self.log_centerframe,
                                        text="Entrar",
                                        default="active",
                                        style="Active.TButton",
                                        command=self.validate_login)

        self.log_ltxt_username.entry.bind("<Return>", 
            lambda x: self.log_ltxt_password.entry.focus_set())
        self.log_ltxt_password.entry.bind("<Return>", self.validate_login)
        self.log_btn_enter.bind("<Return>", self.validate_login)

        self.log_ltxt_username.entry.bind("<Escape>", lambda x: exit())
        self.log_ltxt_password.entry.bind("<Escape>", lambda x: exit())
        self.log_btn_enter.bind("<Escape>", lambda x: exit())
        self.log_btn_cancel.bind("<Escape>", lambda x: exit())
        self.log_btn_alterar_senha.bind("<Escape>", lambda x: exit())

        self.log_ltxt_username.entry.focus_set()
        self.log_ltxt_username.pack(side=tk.TOP, expand=False)
        self.log_ltxt_password.pack(side=tk.TOP, expand=False)
        self.log_btn_enter.pack(side=tk.RIGHT)
        self.log_btn_cancel.pack(side=tk.RIGHT)
        self.log_btn_alterar_senha.pack(side=tk.LEFT)

        self.log_centerframe.pack(side=tk.TOP, expand=True, fill='both')
        self.log_mainframe.pack(side=tk.TOP, expand=True, fill='both')
        root.withdraw()

    def shake_login_window(self):
        """ Shakes login window when user name and password don't match.
        """
        width = LOGIN_MIN_WIDTH
        height = LOGIN_MIN_HEIGHT
        w_x, w_y = self.root_login.winfo_x(), self.root_login.winfo_y()

        for n in range(3):
            for i in range(0, 18 - n * 6, 6):
                self.root_login.geometry(f"{width}x{height}+{w_x+i}+{w_y}")
                self.root_login.update()
            for i in range(18 - n * 6, -18 + n * 6, -6):
                self.root_login.geometry(f"{width}x{height}+{w_x+i}+{w_y}")
                self.root_login.update()
            for i in range(-18 + n * 6, 0, 6):
                self.root_login.geometry(f"{width}x{height}+{w_x+i}+{w_y}")
                self.root_login.update()

        self.root_login.geometry(f"{width}x{height}+{w_x}+{w_y}")

    def validate_login(self, *event):
        username = self.log_ltxt_username.get()
        password = self.log_ltxt_password.get()

        self.loggedin, self.token = db.validate_login(username, password)

        if self.loggedin:
            self.failed_login_attempts = 0
            self.username = username
            self.password = password
            self.start_main_window()
            root.deiconify()
            self.root_login.destroy()
        else:
            self.failed_login_attempts += 1
            self.shake_login_window()
            self.log_ltxt_username.clear()
            self.log_ltxt_password.clear()
            self.log_ltxt_username.entry.focus_set()
            
            if self.failed_login_attempts > 4:
                messagebox.showerror("",
                        "Os dados introduzidos não permitiram a sua "
                        "autenticação. Por favor contacte um administrador.\n"
                        "\nPor motivos de segurança, a aplicação irá agora "
                        "encerrar.")
                exit()          


    def change_password(self):
        self.log_ltxt_username.entry.focus_set()
        self.root_chpwd = tk.Toplevel()
        self.root_chpwd.minsize(CHPWD_MIN_WIDTH, CHPWD_MIN_HEIGHT)
        self.root_chpwd.maxsize(CHPWD_MAX_WIDTH, CHPWD_MAX_HEIGHT)
        self.root_chpwd.configure(background='grey92')
        self.root_chpwd.title('Alterar senha')

        self.chpwd_mainframe = ttk.Frame(self.root_chpwd, padding="12 25 12 0")
        self.chpwd_topframe = ttk.Frame(
            self.chpwd_mainframe, padding="5 8 5 0")
        self.chpwd_centerframe = ttk.Frame(self.chpwd_mainframe)

        self.chpwd_bottomframe = ttk.Frame(self.chpwd_mainframe)
        self.chpwd_btnFont = tkinter.font.Font(family="Lucida Grande", size=10)
        self.chpwd_btnTxtColor = "grey22"
        self.chpwd_btnTxtColor_active = "white"

        w = self.root_chpwd.winfo_screenwidth()
        h = self.root_chpwd.winfo_screenheight()

        size = tuple(int(_) for _ in self.root_chpwd.geometry().split('+')[0].split('x'))
        x = int(w / 2 - LOGIN_MIN_WIDTH / 2)
        y = int(h / 3 - LOGIN_MIN_HEIGHT / 2)

        self.root_chpwd.geometry(
            f"{CHPWD_MIN_WIDTH}x{CHPWD_MIN_HEIGHT}+{x}+{y}")
        self.chpwd_ltxt_username = LabelEntry(
            self.chpwd_centerframe, label="Nome de Utilizador", width=30)
        self.chpwd_ltxt_old_password = LabelEntry(
            self.chpwd_centerframe, label="Palavra-passe antiga", width=30)
        self.chpwd_ltxt_new_password1 = LabelEntry(
            self.chpwd_centerframe, label="Nova palavra-passe", width=30)
        self.chpwd_ltxt_new_password2 = LabelEntry(
            self.chpwd_centerframe,
            label="Confirmar nova palavra-passe",
            width=30)
        self.chpwd_ltxt_old_password.entry.config(show="•")
        self.chpwd_ltxt_new_password1.entry.config(show="•")
        self.chpwd_ltxt_new_password2.entry.config(show="•")

        self.chpwd_btn_cancel = ttk.Button(self.chpwd_centerframe,
                                           text="Cancelar",
                                           command=self.root_chpwd.destroy)
        self.chpwd_btn_alterar = ttk.Button(self.chpwd_centerframe,
                                            text="Alterar palavra-passe",
                                            default="active",
                                            style="Active.TButton",
                                            command=self.validate_change_password)

        self.chpwd_ltxt_username.entry.bind(
            "<Return>", lambda x: self.chpwd_ltxt_old_password.entry.focus_set())
        self.chpwd_ltxt_old_password.entry.bind(
            "<Return>", lambda x: self.chpwd_ltxt_new_password1.entry.focus_set())
        self.chpwd_ltxt_new_password1.entry.bind(
            "<Return>", lambda x: self.chpwd_ltxt_new_password2.entry.focus_set())
        self.chpwd_ltxt_new_password2.entry.bind(
            "<Return>", self.validate_change_password)
        self.chpwd_btn_alterar.bind("<Return>", self.validate_change_password)

        self.chpwd_ltxt_username.entry.bind(
            "<Escape>", lambda x: self.root_chpwd.destroy())
        self.chpwd_ltxt_old_password.entry.bind(
            "<Escape>", lambda x: self.root_chpwd.destroy())
        self.chpwd_ltxt_new_password1.entry.bind(
            "<Escape>", lambda x: self.root_chpwd.destroy())
        self.chpwd_ltxt_new_password2.entry.bind(
            "<Escape>", lambda x: self.root_chpwd.destroy())
        self.chpwd_btn_alterar.bind("<Escape>", lambda x: exit())
        self.chpwd_btn_cancel.bind("<Escape>", lambda x: exit())

        self.chpwd_ltxt_username.entry.focus_set()

        self.chpwd_ltxt_username.pack(side=tk.TOP, expand=False)
        self.chpwd_ltxt_old_password.pack(side=tk.TOP, expand=False)
        self.chpwd_ltxt_new_password1.pack(side=tk.TOP, expand=False)
        self.chpwd_ltxt_new_password2.pack(side=tk.TOP, expand=False)
        self.chpwd_btn_alterar.pack(side=tk.RIGHT)
        self.chpwd_btn_cancel.pack(side=tk.RIGHT)

        self.chpwd_centerframe.pack(side=tk.TOP, expand=True, fill='both')
        self.chpwd_mainframe.pack(side=tk.TOP, expand=True, fill='both')

    def validate_change_password(self, *event):
        username = self.chpwd_ltxt_username.get()
        old_password = self.chpwd_ltxt_old_password.get()
        new_password1 = self.chpwd_ltxt_new_password1.get()
        new_password2 = self.chpwd_ltxt_new_password2.get()

        if new_password1 != new_password2:
            messagebox.showwarning(
                "", "As palavras-passe indicadas são diferentes!")
            self.chpwd_ltxt_new_password1.clear()
            self.chpwd_ltxt_new_password2.clear()
            self.chpwd_ltxt_new_password1.entry.focus_set()
            return
        elif len(new_password1) < 3:
            messagebox.showwarning(
                "", "A palavra-passe que introduziu é demasiado curta!")
            self.chpwd_ltxt_new_password1.clear()
            self.chpwd_ltxt_new_password2.clear()
            self.chpwd_ltxt_new_password1.entry.focus_set()
            return

        loggedin, _ = db.validate_login(username, old_password)
        if loggedin:
            if db.change_password(username, old_password, new_password1):
                self.root_chpwd.destroy()
                self.log_ltxt_username.entry.focus_set()
            else:
                messagebox.showerror("", 
                    "Ocorreu um erro desconhecido ao tentar alterar a senha. "
                    "Tente efetuar login com os seus dados. Se não conseguir, "
                    "por favor contacte um administrador.")
                self.chpwd_ltxt_username.clear()
                self.chpwd_ltxt_old_password.clear()
                self.chpwd_ltxt_new_password1.clear()
                self.chpwd_ltxt_new_password2.clear()
                self.chpwd_ltxt_username.entry.focus_set()
        else:
            messagebox.showwarning("", 
                "O nome de utilizador ou a palavra-passe não estão corretos.")
            self.chpwd_ltxt_username.clear()
            self.chpwd_ltxt_old_password.clear()
            self.chpwd_ltxt_username.entry.focus_set()

    def start_main_window(self):
        self.gerar_painel_mensagens()
        self.gerar_menu()
        self.montar_barra_de_ferramentas()
        self.montar_tabela()
        self.gerar_painel_entrada()

        self.composeFrames()

        self.inserir_dados_de_exemplo()
        self.alternar_cores(self.tree)
        self.inserir_msgs_de_exemplo()
        self.alternar_cores(self.msgtree, inverso=False, fundo1='grey96')
        self.atualizar_soma_processos()

        if self.contar_linhas(self.msgtree) > 0:
            #self.after(1200, self.abrir_painel_mensagens)
            self.abrir_painel_mensagens()

        # self.teste_GUI()

    def teste_GUI(self):
        for i in range(3600):
            print(i)
            self.create_window_contacts()
            self.create_window_remessas()
            self.abrir_painel_mensagens()
            self.mostrar_painel_entrada()

            self.close_window_contactos()
            self.close_window_remessas()
            self.fechar_painel_mensagens()
            self.fechar_painel_entrada()

    def contar_linhas(self, tree):
        """
        Obtém uma contagem do número atual de linhas/itens da tabela (tree)
        passada como argumento.
        """
        linhas = tree.get_children("")
        return len(linhas)

    def atualizar_soma_processos(self):
        """
        Atualiza a barra de estado com o número de reparações visíveis na
        tabela principal.
        """
        self.nprocessos = self.contar_linhas(self.tree)
        self.my_statusbar.set(f"{self.nprocessos} processos")

    def atualizar_soma_msgs(self):
        """
        Atualiza a contagem do número de mensagens.
        """
        self.nmensagens = self.contar_linhas(self.msgtree)

        if self.nmensagens:
            self.lbl_mensagens_titulo.config(
                text=f"Tem {self.nmensagens} mensagens")
        else:
            self.lbl_mensagens_titulo.config(text=f"Não tem mensagens.")

    def bind_tree(self):
        self.tree.bind('<<TreeviewSelect>>', self.selectItem_popup)
        self.tree.bind('<Double-1>', lambda x: self.create_window_detalhe_rep(
            num_reparacao=self.reparacao_selecionada))
        self.tree.bind("<Button-2>", self.popupMenu)
        self.tree.bind("<Button-3>", self.popupMenu)

        self.msgtree.bind('<<TreeviewSelect>>', self.selectItemMsg_popup)
        self.msgtree.bind(
            '<Double-1>', lambda x: self.create_window_detalhe_msg(num_mensagem=self.mensagem_selecionada))
        self.msgtree.bind("<Button-2>", self.popupMenuMsg)
        self.msgtree.bind("<Button-3>", self.popupMenuMsg)

    def unbind_tree(self):
        self.tree.bind('<<TreeviewSelect>>', None)
        self.tree.bind('<Double-1>', None)
        self.tree.bind("<Button-2>", None)
        self.tree.bind("<Button-3>", None)

        self.msgtree.bind('<<TreeviewSelect>>', None)
        self.msgtree.bind('<Double-1>', None)
        self.msgtree.bind("<Button-2>", None)
        self.msgtree.bind("<Button-3>", None)

    def selectItem_popup(self, event):
        """ # Hacking moment: Uma função que junta duas funções, para assegurar a sequência...
        """
        print("selectItem_popup")
        self.selectItem()
        self.popupMenu(event)

    def selectItemMsg_popup(self, event):
        """ # Hacking moment: Uma função que junta duas funções, para assegurar a sequência...
        """
        print("selectItemMsg_popup")
        self.selectItemMsg()
        self.popupMenuMsg(event)

    def selectItemMsg(self, *event):
        """
        Obter mensagem selecionada (após clique de rato na linha correspondente)
        """
        curItem = self.msgtree.focus()
        tree_linha = self.msgtree.item(curItem)

        mensagem = tree_linha["values"][1]
        remetente = tree_linha["values"][2].split(',', 1)[0]
        self.my_statusbar.set(f"{mensagem} • Mensagem enviada por {remetente}")
        self.mensagem_selecionada = mensagem

    def popupMenu(self, event):
        """action in event of button 3 on tree view"""
        # select row under mouse
        self.selectItem()

        iid = self.tree.identify_row(event.y)
        x, y = event.x_root, event.y_root
        if iid:
            if x != 0 and y != 0:
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

    def popupMenuMsg(self, event):
        """action in event of button 3 on tree view"""
        # select row under mouse
        self.selectItemMsg()

        iid = self.msgtree.identify_row(event.y)
        x, y = event.x_root, event.y_root
        if iid:
            if x != 0 and y != 0:
                # mouse pointer over item
                self.msgtree.selection_set(iid)
                self.msgtree.focus(iid)
                self.contextMenuMsg.post(event.x_root, event.y_root)
                print("popupMenuMsg(): x,y = ", event.x_root, event.y_root)
            else:
                print("popupMenuMsg(): wrong values for event - x=0, y=0")
        else:
            print(iid)
            print("popupMenuMsg(): Else - No code here yet! (mouse not over item)")
            # mouse pointer not over item
            # occurs when items do not fill frame
            # no action required
            pass

    def selectItem(self, *event):
        """
        Obter reparação selecionada (após clique de rato na linha correspondente)
        """
        curItem = self.tree.focus()
        tree_linha = self.tree.item(curItem)

        processo = tree_linha["values"][0]
        equipamento = tree_linha["values"][2]
        num_serie = "S/N: CK992737632POT234B"  # TODO: obter num serie
        self.my_statusbar.set(f"{equipamento} • {num_serie}")
        self.reparacao_selecionada = processo

    def montar_tabela(self):
        self.tree['columns'] = (
            'Nº', 'Cliente', 'Equipamento', 'Serviço', 'Estado', 'Dias')
        #self.tree.pack(side='top', expand=True, fill='both')
        self.tree.column('#0', anchor='w', minwidth=0, stretch=0, width=0)
        self.tree.column('Nº', anchor='e', minwidth=46, stretch=0, width=46)
        self.tree.column('Cliente', minwidth=80, stretch=1, width=120)
        self.tree.column('Equipamento', minwidth=80, stretch=1, width=170)
        self.tree.column('Serviço', minwidth=80, stretch=1, width=210)
        self.tree.column('Estado', minwidth=80, stretch=0, width=145)
        self.tree.column('Dias', anchor='e', minwidth=35, stretch=0, width=35)
        self.configurarTree()
        self.leftframe.grid_columnconfigure(0, weight=1)
        self.leftframe.grid_columnconfigure(1, weight=0)
        self.leftframe.grid_rowconfigure(0, weight=1)

        self.bind_tree()

    def montar_barra_de_ferramentas(self):
        self.btn_add = ttk.Button(
            self.topframe, text="➕", width=6, command=self.show_entryform)
        self.btn_add.grid(column=0, row=0)
        self.dicas.bind(self.btn_add, 'Criar novo processo de reparação. (⌘N)')
        self.label_add = ttk.Label(
            self.topframe, font=self.btnFont, foreground=self.btnTxtColor, text="Nova reparação")
        self.label_add.grid(column=0, row=1)

        # ----------- Botão com menu "Mostrar" --------------
        self.label_mbtn_mostrar = ttk.Label(self.topframe, 
            font=self.btnFont,
            foreground=self.btnTxtColor,
            text="Mostrar processos…")
        self.mbtn_mostrar = ttk.Menubutton(
            self.topframe, text="Processos", width=18)
        self.mbtn_mostrar.menu = tk.Menu(self.mbtn_mostrar, tearoff=0)
        self.mbtn_mostrar["menu"] = self.mbtn_mostrar.menu

        self.mbtn_mostrar.menu.add_command(
            label="Processos em curso", command=None)
        self.mbtn_mostrar.menu.add_command(
            label="Processos finalizados", command=None)
        self.mbtn_mostrar.menu.add_command(
            label="Todos os processos", command=None)
        self.mbtn_mostrar.menu.add_separator()
        self.mbtn_mostrar.menu.add_command(
            label=ESTADOS[EM_PROCESSAMENTO], command=None)
        self.mbtn_mostrar.menu.add_command(
            label=ESTADOS[AGUARDA_ENVIO], command=None)
        self.mbtn_mostrar.menu.add_command(
            label=ESTADOS[AGUARDA_RESP_FORNECEDOR], command=None)
        self.mbtn_mostrar.menu.add_command(
            label=ESTADOS[AGUARDA_RESP_CLIENTE], command=None)
        self.mbtn_mostrar.menu.add_command(
            label=ESTADOS[AGUARDA_RECECAO], command=None)
        self.mbtn_mostrar.menu.add_command(
            label=ESTADOS[RECEBIDO], command=None)
        self.mbtn_mostrar.menu.add_command(
            label=ESTADOS[DISPONIVEL_P_LEVANTAMENTO])

        self.mbtn_mostrar.grid(column=1, row=0)
        self.label_mbtn_mostrar.grid(column=1, row=1)
        self.dicas.bind(self.mbtn_mostrar, 
            'Mostrar apenas uma parte dos processos,\n'
            'filtrando-os com base do seu estado atual.')

        # ----------- fim de Botão com menu "Mostrar" -------------

        self.btn_detalhes = ttk.Button(self.topframe, text=" ℹ️️", width=3, command=lambda: self.create_window_detalhe_rep(
            num_reparacao=self.reparacao_selecionada))
        self.btn_detalhes.grid(column=6, row=0)
        ttk.Label(self.topframe, font=self.btnFont,
                  foreground=self.btnTxtColor, text="Detalhes").grid(column=6, row=1)
        self.dicas.bind(
            self.btn_detalhes, 'Apresentar detalhes do processo\nde reparação selecionado. (⌘I)')

        # ----------- Botão com menu "Alterar estado" --------------
        self.label_mbtn_alterar = ttk.Label(
            self.topframe, font=self.btnFont, foreground=self.btnTxtColor, text="Alterar estado")
        self.mbtn_alterar = ttk.Menubutton(self.topframe, text="•••")
        self.mbtn_alterar.menu = tk.Menu(self.mbtn_alterar, tearoff=0)
        self.mbtn_alterar["menu"] = self.mbtn_alterar.menu

        self.mbtn_alterar.menu.add_command(
            label=ESTADOS[EM_PROCESSAMENTO], command=None)
        self.mbtn_alterar.menu.add_command(
            label=ESTADOS[AGUARDA_ENVIO], command=None)
        self.mbtn_alterar.menu.add_command(
            label=ESTADOS[AGUARDA_RESP_FORNECEDOR], command=None)
        self.mbtn_alterar.menu.add_command(
            label=ESTADOS[AGUARDA_RESP_CLIENTE], command=None)
        self.mbtn_alterar.menu.add_command(
            label=ESTADOS[AGUARDA_RECECAO], command=None)
        self.mbtn_alterar.menu.add_command(
            label=ESTADOS[RECEBIDO], command=None)
        self.mbtn_alterar.menu.add_command(
            label=ESTADOS[DISPONIVEL_P_LEVANTAMENTO], command=None)
        self.mbtn_alterar.menu.add_separator()
        self.mbtn_alterar.menu.add_command(
            label=ESTADOS[ENTREGUE], command=None)
        self.mbtn_alterar.menu.add_separator()
        self.mbtn_alterar.menu.add_command(
            label=ESTADOS[ANULADO], command=None)
        self.mbtn_alterar.menu.add_command(
            label=ESTADOS[ABANDONADO], command=None)
        self.mbtn_alterar.menu.add_command(
            label=ESTADOS[SEM_INFORMACAO], command=None)
        self.mbtn_alterar.grid(column=7, row=0)
        self.label_mbtn_alterar.grid(column=7, row=1)
        self.dicas.bind(
            self.mbtn_alterar, 'Alterar o estado do processo\nde reparação selecionado.')
        # ----------- fim de Botão com menu "Alterar estado" -------------

        self.btn_entregar = ttk.Button(
            self.topframe, text=" ✅", width=3, command=None)
        self.btn_entregar.grid(column=8, row=0)
        self.label_entregar = ttk.Label(
            self.topframe, font=self.btnFont, foreground=self.btnTxtColor, text="Entregar")
        self.label_entregar.grid(column=8, row=1)
        self.dicas.bind(
            self.btn_entregar, 'Marcar o processo de reparação\nselecionado como entregue.')

        self.btn_messages = ttk.Button(
            self.topframe, text=" ☝️️", width=3, command=self.abrir_painel_mensagens)
        self.label_messages = ttk.Label(
            self.topframe, font=self.btnFont, foreground=self.btnTxtColor, text="Mensagens")
        self.btn_messages.grid(row=0, column=13)
        self.label_messages.grid(column=13, row=1)
        self.dicas.bind(self.btn_messages,
                        'Mostrar/ocultar o painel de mensagens. (⌘1)')

        self.btn_contacts = ttk.Button(
            self.topframe, text=" ✉️️", width=3, command=self.create_window_contacts)
        self.label_contacts = ttk.Label(
            self.topframe, font=self.btnFont, foreground=self.btnTxtColor, text="Contactos")
        self.btn_contacts.grid(row=0, column=14)
        self.label_contacts.grid(column=14, row=1)
        self.dicas.bind(self.btn_contacts,
                        'Mostrar/ocultar a janela de contactos. (⌘2)')

        self.btn_remessas = ttk.Button(
            self.topframe, text=" ⬆️️", width=3, command=self.create_window_remessas)
        self.label_remessas = ttk.Label(
            self.topframe, font=self.btnFont, foreground=self.btnTxtColor, text="Remessas")
        self.btn_remessas.grid(row=0, column=15)
        self.label_remessas.grid(column=15, row=1)
        self.dicas.bind(self.btn_remessas,
                        'Mostrar/ocultar a janela de remessas. (⌘3)')

        self.text_input_pesquisa = ttk.Entry(self.topframe, width=12)

        self.text_input_pesquisa.grid(column=16, row=0)
        ttk.Label(self.topframe, font=self.btnFont, foreground=self.btnTxtColor,
                  text="Pesquisar").grid(column=16, row=1)
        self.dicas.bind(self.text_input_pesquisa,
                        'Para iniciar a pesquisa, digite\numa palavra ou frase. (⌘F)')

        #letras_etc = ascii_letters + "01234567890-., "
        # for char in letras_etc:
        #    keystr = '<KeyRelease-' + char + '>'
        #    self.text_input_pesquisa.bind(keystr, self.ativar_pesquisa)
        #self.text_input_pesquisa.bind('<Button-1>', self.clique_a_pesquisar)
        #self.text_input_pesquisa.bind('<KeyRelease-Escape>', self.cancelar_pesquisa)
        #self.text_input_pesquisa.bind('<KeyRelease-Mod2-a>', self.text_input_pesquisa.select_range(0, END))

        for col in range(1, 16):
            self.topframe.columnconfigure(col, weight=0)
        #self.topframe.columnconfigure(3, weight=1)
        self.topframe.columnconfigure(5, weight=1)
        self.topframe.columnconfigure(11, weight=1)

    def create_window_remessas(self, *event, criar_nova_remessa=None):
        # TODO: as janelas de contactos e remesas não são destruídas
        # corretamente, ficam sempre na memória e no menu. Como resolver?

        if not estado.janela_remessas_aberta:
            if criar_nova_remessa:
                print("A abrir a janela de remessas, vamos lá criar uma nova remessa!")
                estado.painel_nova_remessa_aberto = True
            #self.newWindow2 = tk.Toplevel(self.master)
            estado.janela_remessas = tk.Toplevel(self.master)
            self.janela_remessas = remessas.RemessasWindow(
                estado.janela_remessas, estado)
            estado.janela_remessas_aberta = True
            estado.janela_remessas.wm_protocol(
                "WM_DELETE_WINDOW", self.close_window_remessas)
        else:
            if not criar_nova_remessa:
                self.close_window_remessas()
            else:
                estado.painel_nova_remessa_aberto = True
                self.janela_remessas.mostrar_painel_entrada()

    def close_window_remessas(self, *event):
        root.update_idletasks()
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
            self.janela_contactos = contactos.ContactsWindow(
                estado.janela_contactos, estado)
            estado.janela_contactos_aberta = True
            estado.janela_contactos.wm_protocol(
                "WM_DELETE_WINDOW", self.close_window_contactos)
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
                self.ef_txt_num_cliente.insert(
                    0, estado.contacto_para_nova_reparacao)
            elif estado.tipo_novo_contacto == "Fornecedor":
                self.ef_txt_num_fornecedor.delete(0, tk.END)
                self.ef_txt_num_fornecedor.insert(
                    0, estado.contacto_para_nova_reparacao)
            else:
                print("Qual é afinal o tipo de contacto a criar???")

        estado.janela_contactos_aberta = False
        estado.painel_novo_contacto_aberto = False
        estado.janela_contactos.destroy()
        self.ef_ltxt_descr_equipamento.scrolledtext.focus()

    def create_window_detalhe_rep(self, *event, num_reparacao=None):
        if num_reparacao is None:
            messagebox.showwarning("", "Nenhuma reparação selecionada.")
            root.focus_force()
            return

        self.rep_detail_windows_count += 1
        self.rep_newDetailsWindow[self.rep_detail_windows_count] = tk.Toplevel(
        )
        self.janela_detalhes_rep = detalhe_reparacao.repairDetailWindow(
            self.rep_newDetailsWindow[self.rep_detail_windows_count], num_reparacao)

    def create_window_detalhe_msg(self, *event, num_mensagem=None):
        if num_mensagem is None:
            messagebox.showwarning("", "Nenhuma mensagem selecionada.")
            root.focus_force()
            return

        self.msg_detail_windows_count += 1
        self.msg_newDetailsWindow[self.msg_detail_windows_count] = tk.Toplevel(
        )
        self.janela_detalhes_msg = detalhe_mensagem.msgDetailWindow(
            self.msg_newDetailsWindow[self.msg_detail_windows_count], num_mensagem)

    def gerar_painel_mensagens(self):
        self.mensagens_frame = ttk.Frame(self.messagepane)
        self.mensagens_frame_top = ttk.Frame(
            self.mensagens_frame, padding="4 10 4 0")

        self.lbl_mensagens_titulo = ttk.Label(
            self.mensagens_frame, text="Tem 0 mensagens", anchor='center', font=("Lucida Grande", 18))
        self.lbl_mensagens_titulo.pack()

        self.mensagens_frame_btn = ttk.Frame(
            self.mensagens_frame, padding="2 4 2 0")
        self.mensagens_frame_tree = ttk.Frame(
            self.mensagens_frame, padding="2 0 2 0")

        self.btn_msg_mostrar = ttk.Button(
            self.mensagens_frame_btn, style="secondary_msg.TButton", text="Mostrar")
        self.btn_msg_mostrar.grid(
            column=0, sticky=tk.W, row=1, in_=self.mensagens_frame_btn)
        self.dicas.bind(self.btn_msg_mostrar,
                        'Mostrar o conteúdo da mensagem\nselecionada.')

        self.btn_msg_apagar_um = ttk.Button(
            self.mensagens_frame_btn, style="secondary_msg.TButton", text="Apagar")
        self.btn_msg_apagar_um.grid(
            column=1, sticky=tk.E, row=1, in_=self.mensagens_frame_btn)
        self.dicas.bind(self.btn_msg_apagar_um,
                        'Eliminar a mensagem selecionada\n(esta ação é irreversível).')

        self.btn_msg_apagar_tudo = ttk.Button(
            self.mensagens_frame_btn, style="secondary_msg.TButton", text="Apagar tudo")
        self.btn_msg_apagar_tudo.grid(
            column=3, sticky=tk.E, row=1, in_=self.mensagens_frame_btn)
        self.dicas.bind(self.btn_msg_apagar_tudo,
                        'Apagar todas as mensagens\n(esta ação é irreversível).')

        self.mensagens_frame_btn.grid_columnconfigure(0, weight=0)
        self.mensagens_frame_btn.grid_columnconfigure(1, weight=0)
        self.mensagens_frame_btn.grid_columnconfigure(2, weight=1)
        self.mensagens_frame_btn.grid_columnconfigure(3, weight=0)

        self.lblFrame_mensagens = ttk.LabelFrame(
            self.mensagens_frame_tree, labelanchor="n", padding="4 4 4 4")

        self.msgtree = ttk.Treeview(
            self.lblFrame_mensagens, height=31, selectmode='browse', show='', style='Msg.Treeview')
        self.msgtree['columns'] = ('ico', 'Processo', 'Mensagem')
        self.msgtree.column('#0', anchor='w', minwidth=0, stretch=0, width=0)
        self.msgtree.column('ico', anchor='ne',
                            minwidth=20, stretch=0, width=20)
        self.msgtree.column('Processo', anchor='ne',
                            minwidth=40, stretch=0, width=40)
        self.msgtree.column('Mensagem', anchor='nw',
                            minwidth=235, stretch=1, width=235)

        self.msgtree.grid(column=0, columnspan=4, row=2, sticky="nsew")
        self.lblFrame_mensagens.grid_columnconfigure(2, weight=1)
        self.lblFrame_mensagens.grid_rowconfigure(2, weight=1)

        # Barra de deslocação para a tabela
        #self.vsb2 = AutoScrollbar(self.tab_mensagens, orient="vertical", command=self.msgtree.yview)
        # self.msgtree.configure(yscrollcommand=self.vsb2.set)
        #self.vsb2.grid(column=1, row=0, sticky=tk.N+tk.S, in_=self.tab_mensagens)

        self.estilo.configure('Msg.Treeview', font=("Lucida Grande", 10), foreground="grey22",
                              fieldbackground="grey89", anchor='n', background='grey91', rowheight=72)
        self.estilo.configure("secondary_msg.TButton",
                              font=("Lucida Grande", 11))
        #estilo.configure('Msg.Treeview.Heading', font=("Lucida Grande", 9), foreground="grey22")
        #estilo.configure( 'Msg.Treeview', relief = 'flat', borderwidth = 0)

        self.mensagens_frame_top.pack(side=tk.TOP)
        self.mensagens_frame_btn.pack(side=tk.TOP)
        self.mensagens_frame_tree.pack(side=tk.TOP, expand=True, fill='both')
        self.lblFrame_mensagens.pack(side=tk.TOP, expand=True, fill='both')

    def abrir_painel_mensagens(self, *event):
        root.update_idletasks()
        if estado.painel_mensagens_aberto == False:
            self.mensagens_frame.pack()
            self.messagepane.pack(side='top', expand=True, fill='both')
            self.rightframe.grid()
            # self.inserir_msgs_de_exemplo()  # TODO atualizar_mensagens()
            self.alternar_cores(self.msgtree, inverso=False, fundo1='grey96')
            self.atualizar_soma_msgs()
            estado.painel_mensagens_aberto = True
        else:
            self.fechar_painel_mensagens()

    def fechar_painel_mensagens(self, *event):
        root.update_idletasks()
        self.messagepane.pack_forget()
        self.mensagens_frame.pack_forget()
        self.rightframe.grid_remove()
        estado.painel_mensagens_aberto = False

    def mostrar_painel_entrada(self, *event):
        self.MenuFicheiro.entryconfig("Nova reparação", state="disabled")
        # root.unbind_all("<Command-n>")
        self.show_entryform()
        estado.painel_nova_reparacao_aberto = self.is_entryform_visible
        self.ef_txt_num_cliente.focus()
        self.entryframe.bind_all(
            "<Command-Escape>", self.fechar_painel_entrada)

    def fechar_painel_entrada(self, *event):
        self.hide_entryform()
        self.clear_text()
        root.focus_force()
        self.tree.focus()
        estado.painel_nova_reparacao_aberto = self.is_entryform_visible
        # root.bind_all("<Command-n>")

    def clear_text(self):
        self.entryframe.focus()
        self.ef_var_tipo.set(0)
        self.ef_var_estado.set(0)
        self.ef_var_garantia.set(0)
        self.ef_var_repr_loja.set(0)
        self.ef_var_efetuar_copia.set(0)
        self.ef_var_find_my.set(0)
        self.ef_var_local_intervencao.set("Loja X")
        self.ef_var_modo_entrega.set("Levantamento nas n/ instalações")
        self.ef_var_portes.set(0)
        self.ef_txt_num_cliente.delete(0, 'end')
        self.ef_txt_nome_cliente.delete(0, 'end')
        self.ef_lbl_telefone_info.configure(text="")
        self.ef_lbl_email_info.configure(text="")
        self.ef_txt_num_fornecedor.delete(0, 'end')
        self.ef_txt_nome_fornecedor.delete(0, 'end')
        self.ef_lbl_telefone_info_fornecedor.configure(text="")
        self.ef_lbl_email_info_fornecedor.configure(text="")
        self.ef_ltxt_descr_equipamento.clear()
        self.ef_ltxt_obs_estado_equipamento.clear()
        self.ef_ltxt_cod_artigo.clear()
        self.ef_ltxt_num_serie.clear()
        self.ef_ltxt_data_compra.clear()
        self.ef_ltxt_num_fatura.clear()
        self.ef_ltxt_local_compra.clear()
        self.ef_ltxt_num_fatura_fornecedor.clear()
        self.ef_ltxt_data_fatura_fornecedor.clear()
        self.ef_ltxt_nar.clear()
        self.ef_ltxt_num_guia_rececao.clear()
        self.ef_ltxt_data_entrada_stock.clear()
        self.ef_ltxt_num_quebra_stock.clear()
        self.ef_text_descr_avaria_servico.delete('1.0', 'end')
        self.ef_ltxt_senha.clear()
        self.ef_ltxt_acessorios_entregues.clear()
        self.ef_ltxt_notas.clear()
        self.ef_ltxt_morada_entrega.clear()
        self.radio_tipo_command()
        self.radio_garantia_command()
        self.adicionar_morada_entrega()

    def gerar_painel_entrada(self):
        self.ef_var_tipo = tk.IntVar()
        self.ef_var_estado = tk.IntVar()
        self.ef_var_garantia = tk.IntVar()
        self.ef_var_repr_loja = tk.IntVar()
        self.ef_var_repr_loja.set(0)
        self.ef_var_efetuar_copia = tk.IntVar()
        self.ef_var_find_my = tk.IntVar()
        self.ef_var_local_intervencao = tk.StringVar()
        self.ef_var_local_intervencao.set("Loja X")
        self.ef_var_modo_entrega = tk.StringVar()
        self.ef_var_modo_entrega.set("Levantamento nas n/ instalações")
        self.ef_var_portes = tk.IntVar()

        # entryfr1-----------------------------
        self.ef_cabecalho = ttk.Frame(self.entryfr1, padding=4)
        self.ef_lbl_titulo = ttk.Label(
            self.ef_cabecalho, style="Panel_Title.TLabel", text="Adicionar Reparação:\n")
        self.ef_lbl_tipo = ttk.Label(
            self.ef_cabecalho, text="Tipo de processo:", style="Panel_Body.TLabel")
        self.ef_radio_tipo_cliente = ttk.Radiobutton(self.ef_cabecalho, text="Cliente", style="Panel_Body.TRadiobutton",
                                                     variable=self.ef_var_tipo, value=TIPO_REP_CLIENTE, command=self.radio_tipo_command)
        self.ef_radio_tipo_stock = ttk.Radiobutton(self.ef_cabecalho, text="Stock", style="Panel_Body.TRadiobutton",
                                                   variable=self.ef_var_tipo, value=TIPO_REP_STOCK, command=self.radio_tipo_command)
        self.btn_adicionar = ttk.Button(self.ef_cabecalho, default="active",
                                        style="Active.TButton", text="Adicionar", command=self.on_save_repair)
        self.btn_cancelar = ttk.Button(
            self.ef_cabecalho, text="Cancelar", command=self.on_repair_cancel)

        self.ef_lbl_titulo.grid(column=0, row=0, columnspan=3, sticky='w')
        self.ef_lbl_tipo.grid(column=0, row=1, sticky='e')
        self.ef_radio_tipo_cliente.grid(column=1, row=1, sticky='w')
        self.ef_radio_tipo_stock.grid(column=2, row=1, sticky='w')
        self.btn_adicionar.grid(column=3, row=1, sticky='we')
        self.btn_cancelar.grid(column=3, row=2, sticky='we')

        self.ef_cabecalho.grid(column=0, row=0, sticky='we')
        self.entryfr1.columnconfigure(0, weight=1)
        #self.ef_cabecalho.columnconfigure(0, weight=0)
        self.ef_cabecalho.columnconfigure(2, weight=1)

        #self.btn_adicionar.bind('<Button-1>', self.add_remessa)

        # entryfr2-----------------------------
        self.ef_lf_cliente = ttk.Labelframe(
            self.entryfr2, padding=4, style="Panel_Section_Title.TLabelframe", text="Dados do cliente")
        self.ef_txt_num_cliente = ttk.Entry(
            self.ef_lf_cliente, font=("Helvetica-Neue", 12), width=5)
        self.dicas.bind(self.ef_txt_num_cliente,
                        'Introduzir o número de cliente. (⌘T)')
        self.ef_btn_buscar_cliente = ttk.Button(
            self.ef_lf_cliente, width=1, text="+", command=lambda *x: self.create_window_contacts(criar_novo_contacto="Cliente"))
        self.dicas.bind(self.ef_btn_buscar_cliente,
                        'Criar novo contacto.\nUtilize esta opção caso o cliente não tenha\nainda ficha criada nesta base de dados. (⌘T)')
        self.ef_txt_nome_cliente = ttk.Entry(
            self.ef_lf_cliente, font=("Helvetica-Neue", 12), width=45)
        self.ef_lbl_telefone_lbl = ttk.Label(
            self.ef_lf_cliente, style="Panel_Body.TLabel", text="Tel.:")
        self.ef_lbl_telefone_info = ttk.Label(
            self.ef_lf_cliente, style="Panel_Body.TLabel", text="00 351 000 000 000")
        self.ef_lbl_email_lbl = ttk.Label(
            self.ef_lf_cliente, style="Panel_Body.TLabel", text="Email:")
        self.ef_lbl_email_info = ttk.Label(
            self.ef_lf_cliente, style="Panel_Body.TLabel", text="email.address@portugalmail.com")

        self.ef_lf_fornecedor = ttk.Labelframe(
            self.entryfr2, padding=4, style="Panel_Section_Title.TLabelframe", text="Dados do fornecedor")
        self.ef_txt_num_fornecedor = ttk.Entry(
            self.ef_lf_fornecedor, font=("Helvetica-Neue", 12), width=5)
        self.dicas.bind(self.ef_txt_num_fornecedor,
                        'Introduzir o número de fornecedor. (⌘T)')
        self.ef_btn_buscar_fornecedor = ttk.Button(
            self.ef_lf_fornecedor, width=1, text="+", command=lambda *x: self.create_window_contacts(criar_novo_contacto="Fornecedor"))
        self.dicas.bind(self.ef_btn_buscar_fornecedor,
                        'Criar novo contacto.\nUtilize esta opção caso o fornecedor ou centro técnico\nnão tenha ainda ficha criada nesta base de dados. (⌘T)')
        self.ef_txt_nome_fornecedor = ttk.Entry(
            self.ef_lf_fornecedor, font=("Helvetica-Neue", 12), width=45)
        self.ef_lbl_telefone_lbl_fornecedor = ttk.Label(
            self.ef_lf_fornecedor, style="Panel_Body.TLabel", text="Tel.:")
        self.ef_lbl_telefone_info_fornecedor = ttk.Label(
            self.ef_lf_fornecedor, style="Panel_Body.TLabel", text="00 351 000 000 000")
        self.ef_lbl_email_lbl_fornecedor = ttk.Label(
            self.ef_lf_fornecedor, style="Panel_Body.TLabel", text="Email:")
        self.ef_lbl_email_info_fornecedor = ttk.Label(
            self.ef_lf_fornecedor, style="Panel_Body.TLabel", text="email.address@portugalmail.com")

        self.ef_txt_num_cliente.grid(column=0, row=0, padx=5, sticky='w')
        self.ef_btn_buscar_cliente.grid(column=2, row=0, sticky='w')
        self.ef_txt_nome_cliente.grid(column=3, row=0, padx=5, sticky='w')
        self.ef_lbl_telefone_lbl.grid(column=5, row=0, padx=5, sticky='e')
        self.ef_lbl_telefone_info.grid(column=6, row=0, padx=5, sticky='w')
        self.ef_lbl_email_lbl.grid(column=7, row=0, padx=5, sticky='e')
        self.ef_lbl_email_info.grid(column=8, row=0, padx=5, sticky='w')

        self.ef_txt_num_fornecedor.grid(column=0, row=0, padx=5, sticky='w')
        self.ef_btn_buscar_fornecedor.grid(column=2, row=0, sticky='w')
        self.ef_txt_nome_fornecedor.grid(column=3, row=0, padx=5, sticky='w')
        self.ef_lbl_telefone_lbl_fornecedor.grid(
            column=5, row=0, padx=5, sticky='e')
        self.ef_lbl_telefone_info_fornecedor.grid(
            column=6, row=0, padx=5, sticky='w')
        self.ef_lbl_email_lbl_fornecedor.grid(
            column=7, row=0, padx=5, sticky='e')
        self.ef_lbl_email_info_fornecedor.grid(
            column=8, row=0, padx=5, sticky='w')

        self.ef_lf_cliente.grid(column=0, row=0, sticky='we')
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

        # entryfr3-----------------------------
        self.ef_lf_equipamento = ttk.Labelframe(
            self.entryfr3, padding=4, style="Panel_Section_Title.TLabelframe", text="\nDados do equipamento")
        self.ef_ltxt_descr_equipamento = LabelText(
            self.ef_lf_equipamento, "Descrição:", style="Panel_Body.TLabel", width=30, height=2)
        self.ef_lbl_estado_equipamento = ttk.Label(
            self.ef_lf_equipamento, style="Panel_Body.TLabel", text="Estado:")
        self.ef_radio_estado_marcas_uso = ttk.Radiobutton(
            self.ef_lf_equipamento, text="Marcas de uso", style="Panel_Body.TRadiobutton", variable=self.ef_var_estado, value=0, command=self.radio_estado_command)
        self.ef_radio_estado_bom = ttk.Radiobutton(self.ef_lf_equipamento, text="Bom estado geral",
                                                   style="Panel_Body.TRadiobutton", variable=self.ef_var_estado, value=1, command=self.radio_estado_command)
        self.ef_radio_estado_marcas_acidente = ttk.Radiobutton(
            self.ef_lf_equipamento, text="Marcas de acidente", style="Panel_Body.TRadiobutton", variable=self.ef_var_estado, value=2, command=self.radio_estado_command)
        self.ef_radio_estado_faltam_pecas = ttk.Radiobutton(
            self.ef_lf_equipamento, text="Faltam peças", style="Panel_Body.TRadiobutton", variable=self.ef_var_estado, value=3, command=self.radio_estado_command)
        self.ef_ltxt_obs_estado_equipamento = LabelText(
            self.ef_lf_equipamento, "Observações acerca do estado:", style="Panel_Body.TLabel", width=27, height=2)

        self.ef_lbl_garantia = ttk.Label(
            self.ef_lf_equipamento, style="Panel_Body.TLabel", text="Garantia:")
        self.ef_radio_garantia_fora_garantia = ttk.Radiobutton(
            self.ef_lf_equipamento, text="Fora de garantia", style="Panel_Body.TRadiobutton", variable=self.ef_var_garantia, value=0, command=self.radio_garantia_command)
        self.ef_radio_garantia_neste = ttk.Radiobutton(self.ef_lf_equipamento, text="Sim, neste estabelecimento",
                                                       style="Panel_Body.TRadiobutton", variable=self.ef_var_garantia, value=1, command=self.radio_garantia_command)
        self.ef_radio_garantia_noutro = ttk.Radiobutton(self.ef_lf_equipamento, text="Sim, noutro estabelecimento",
                                                        style="Panel_Body.TRadiobutton", variable=self.ef_var_garantia, value=2, command=self.radio_garantia_command)

        self.ef_ltxt_cod_artigo = LabelEntry(
            self.ef_lf_equipamento, "\nCódigo de artigo:", style="Panel_Body.TLabel", width=15)
        self.ef_ltxt_num_serie = LabelEntry(
            self.ef_lf_equipamento, "\nNº de série:", style="Panel_Body.TLabel", width=15)

        self.ef_ltxt_data_compra = LabelEntry(
            self.ef_lf_equipamento, "\nData de compra:", style="Panel_Body.TLabel", width=15)

        """now = time.localtime(time.time())
        now_value = f"{now[2]}-{now[1]}-{now[0]}"
        now_validate = f"{now[2]}-{now[1]}-{now[0]}"
        self.ef_ltxt_data_compra = Pmw.EntryField(self.ef_lf_equipamento,
                                                 labelpos = 'ne',
                                                 label_text = '\nData de compra (d-m-aaaa):',
                                                 value = now_value,
                                                 validate = {'validator' : 'date',
                                                             'min' : '1-1-1976',
                                                             'max' : now_validate,
                                                             'minstrict' : 0,
                                                             'maxstrict' : 0,
                                                             'fmt' : 'dmy',
                                                             'separator' : '-'},
                                                 )
        """
        self.ef_ltxt_num_fatura = LabelEntry(
            self.ef_lf_equipamento, "\nNº da fatura:", style="Panel_Body.TLabel", width=15)
        self.ef_ltxt_local_compra = LabelEntry(
            self.ef_lf_equipamento, "\nEstabelecimento:", style="Panel_Body.TLabel", width=15)

        self.ef_ltxt_num_fatura_fornecedor = LabelEntry(
            self.ef_lf_equipamento, "Nº fatura fornecedor:", style="Panel_Body.TLabel", width=15)
        self.ef_ltxt_data_fatura_fornecedor = LabelEntry(
            self.ef_lf_equipamento, "Data fatura fornecedor:", style="Panel_Body.TLabel", width=15)
        self.ef_ltxt_nar = LabelEntry(
            self.ef_lf_equipamento, "NAR:", style="Panel_Body.TLabel", width=15)
        self.ef_ltxt_num_guia_rececao = LabelEntry(
            self.ef_lf_equipamento, "Guia de receção:", style="Panel_Body.TLabel", width=15)
        self.ef_ltxt_data_entrada_stock = LabelEntry(
            self.ef_lf_equipamento, "Data de entrada em stock:", style="Panel_Body.TLabel", width=15)
        self.ef_ltxt_num_quebra_stock = LabelEntry(
            self.ef_lf_equipamento, "Nº de quebra de stock:", style="Panel_Body.TLabel", width=15)

        self.ef_ltxt_descr_equipamento.grid(
            column=0, columnspan=2, rowspan=5, row=0, padx=5, sticky='wen')
        self.ef_lbl_estado_equipamento.grid(
            column=2, row=0, padx=5, sticky='w')
        self.ef_radio_estado_marcas_uso.grid(
            column=2, row=1, padx=5, sticky='w')
        self.ef_radio_estado_bom.grid(column=2, row=2, padx=5, sticky='w')
        self.ef_radio_estado_marcas_acidente.grid(
            column=2, row=3, padx=5, sticky='w')
        self.ef_radio_estado_faltam_pecas.grid(
            column=2, row=4, padx=5, sticky='w')
        self.ef_ltxt_obs_estado_equipamento.grid(
            column=3, row=0, rowspan=5, padx=5, sticky='wen')
        self.ef_lbl_garantia.grid(column=4, row=0, padx=5, sticky='w')
        self.ef_radio_garantia_fora_garantia.grid(
            column=4, row=1, padx=5, sticky='w')
        self.ef_radio_garantia_neste.grid(column=4, row=2, padx=5, sticky='w')
        self.ef_radio_garantia_noutro.grid(column=4, row=3, padx=5, sticky='w')
        self.ef_ltxt_cod_artigo.grid(column=0, row=5, padx=5, sticky='we')
        self.ef_ltxt_num_serie.grid(column=1, row=5, padx=5, sticky='we')
        self.ef_ltxt_data_compra.grid(column=2, row=5, padx=5, sticky='we')
        self.ef_ltxt_num_fatura.grid(column=3, row=5, padx=5, sticky='we')

        self.ef_lf_equipamento.grid(column=0, row=0, sticky='we')
        self.entryfr3.columnconfigure(0, weight=1)

        self.ef_lf_equipamento.columnconfigure(0, weight=1)
        self.ef_lf_equipamento.columnconfigure(1, weight=1)
        self.ef_lf_equipamento.columnconfigure(2, weight=1)
        self.ef_lf_equipamento.columnconfigure(3, weight=1)
        self.ef_lf_equipamento.columnconfigure(4, weight=1)

        # entryfr4-----------------------------
        self.ef_lf_servico = ttk.Labelframe(
            self.entryfr4, padding=4, style="Panel_Section_Title.TLabelframe", text="\nAvaria e/ou serviço a realizar")
        self.ef_text_descr_avaria_servico = ScrolledText(self.ef_lf_servico, highlightcolor="LightSteelBlue2", font=(
            "Helvetica-Neue", 12), wrap='word', width=20, height=4)
        self.ef_chkbtn_avaria_reprod_loja = ttk.Checkbutton(
            self.ef_lf_servico, variable=self.ef_var_repr_loja, style="Panel_Body.Checkbutton", width=27, text="Avaria reproduzida na loja")
        self.ef_ltxt_senha = LabelEntry(
            self.ef_lf_servico, "Senha:", style="Panel_Body.TLabel", width=22)
        self.ef_lbl_find_my = ttk.Label(
            self.ef_lf_servico, style="Panel_Body.TLabel", width=27, text="Find my iPhone ativo?")
        self.ef_radio_find_my_sim = ttk.Radiobutton(
            self.ef_lf_servico, text="Sim", style="Panel_Body.TRadiobutton", variable=self.ef_var_find_my, value=1, command=self.radio_find_my)
        self.ef_radio_find_my_nao = ttk.Radiobutton(
            self.ef_lf_servico, text="Não", style="Panel_Body.TRadiobutton", variable=self.ef_var_find_my, value=0, command=self.radio_find_my)
        self.ef_radio_find_my_nao_aplic = ttk.Radiobutton(
            self.ef_lf_servico, text="Não aplicável", style="Panel_Body.TRadiobutton", variable=self.ef_var_find_my, value=2, command=self.radio_find_my)
        self.ef_lbl_espaco = ttk.Label(
            self.ef_lf_servico, style="Panel_Body.TLabel", text=" ")
        self.ef_lbl_efetuar_copia = ttk.Label(
            self.ef_lf_servico, style="Panel_Body.TLabel", text="Efetuar cópia de segurança?")
        self.ef_radio_efetuar_copia_sim = ttk.Radiobutton(
            self.ef_lf_servico, text="Sim", style="Panel_Body.TRadiobutton", variable=self.ef_var_efetuar_copia, value=1, command=self.radio_copia_command)
        self.ef_radio_efetuar_copia_nao = ttk.Radiobutton(
            self.ef_lf_servico, text="Não", style="Panel_Body.TRadiobutton", variable=self.ef_var_efetuar_copia, value=0, command=self.radio_copia_command)
        self.ef_radio_efetuar_copia_n_aplic = ttk.Radiobutton(
            self.ef_lf_servico, text="Não aplicável", style="Panel_Body.TRadiobutton", variable=self.ef_var_efetuar_copia, value=2, command=self.radio_copia_command)

        self.ef_text_descr_avaria_servico.grid(
            column=0, row=0, columnspan=3, rowspan=5, padx=5, sticky='wens')
        self.ef_chkbtn_avaria_reprod_loja.grid(
            column=3, row=0, columnspan=3, padx=5, sticky='nw')
        self.ef_ltxt_senha.grid(
            column=3, row=3, rowspan=2, columnspan=3, padx=5, sticky='w')
        self.ef_lbl_find_my.grid(
            column=6, row=0, columnspan=3, padx=5, sticky='nw')
        self.ef_radio_find_my_sim.grid(column=6, row=1, padx=5, sticky='nw')
        self.ef_radio_find_my_nao.grid(column=7, row=1, sticky='nw')
        self.ef_radio_find_my_nao_aplic.grid(column=8, row=1, sticky='nw')
        self.ef_lbl_espaco.grid(column=8, row=2, sticky='w')
        self.ef_lbl_efetuar_copia.grid(
            column=6, row=3, columnspan=3, padx=5, sticky='w')
        self.ef_radio_efetuar_copia_sim.grid(
            column=6, row=4, padx=5, sticky='w')
        self.ef_radio_efetuar_copia_nao.grid(column=7, row=4, sticky='w')
        self.ef_radio_efetuar_copia_n_aplic.grid(column=8, row=4, sticky='w')

        self.ef_lf_servico.grid(column=0, row=0, sticky='we')
        self.entryfr4.columnconfigure(0, weight=1)

        self.ef_lf_servico.columnconfigure(0, weight=1)

        # entryfr5-----------------------------
        # Notas: text 3 linhas
        # local intervenção lbl + combobox(contactos>fornecedores)
        self.ef_lf_outros_dados = ttk.Labelframe(
            self.entryfr5, padding=4, style="Panel_Section_Title.TLabelframe", text="\nOutros dados")
        self.ef_ltxt_acessorios_entregues = LabelText(
            self.ef_lf_outros_dados, "Acessórios entregues:", style="Panel_Body.TLabel", width=12, height=4)
        self.ef_ltxt_notas = LabelText(
            self.ef_lf_outros_dados, "Notas:", style="Panel_Body.TLabel", width=25, height=4)

        self.ef_lbl_local_intervencao = ttk.Label(
            self.ef_lf_outros_dados, style="Panel_Body.TLabel", text="Local de intervenção:")
        self.ef_combo_local_intervencao = ttk.Combobox(self.ef_lf_outros_dados,
                                                       textvariable=self.ef_var_local_intervencao,
                                                       postcommand=self.atualizar_combo_local_intervencao,
                                                       state='readonly')  # TODO: Obter estes valores a partir da base de dados, a utilizar também no formulário de Remessas.

        self.ef_lbl_modo_entrega = ttk.Label(
            self.ef_lf_outros_dados, style="Panel_Body.TLabel", text="Morada a utilizar na entrega:")
        self.ef_combo_modo_entrega = ttk.Combobox(self.ef_lf_outros_dados,
                                                  textvariable=self.ef_var_modo_entrega,
                                                  values=("Levantamento nas n/ instalações",
                                                          "Enviar para a morada da ficha de cliente",
                                                          "Enviar para outra morada..."),
                                                  state='readonly')  # TODO: Obter estes valores a partir da base de dados, a utilizar também no formulário de Remessas.

        self.ef_lbl_portes = ttk.Label(
            self.ef_lf_outros_dados, style="Panel_Body.TLabel", text="Cliente pagou portes?")
        self.ef_radio_portes_sim = ttk.Radiobutton(
            self.ef_lf_outros_dados, text="Sim", style="Panel_Body.TRadiobutton", variable=self.ef_var_portes, value=1, command=self.radio_portes_command)
        self.ef_radio_portes_nao = ttk.Radiobutton(
            self.ef_lf_outros_dados, text="Não", style="Panel_Body.TRadiobutton", variable=self.ef_var_portes, value=0, command=self.radio_portes_command)
        self.ef_radio_portes_oferta = ttk.Radiobutton(
            self.ef_lf_outros_dados, text="Oferta", style="Panel_Body.TRadiobutton", variable=self.ef_var_portes, value=2, command=self.radio_portes_command)

        self.ef_ltxt_morada_entrega = LabelText(
            self.ef_lf_outros_dados, "Morada a utilizar na entrega:", style="Panel_Body.TLabel", height=4)

        self.ef_ltxt_acessorios_entregues.grid(
            column=0, row=0, rowspan=5, padx=5, sticky='wens')
        self.ef_ltxt_notas.grid(
            column=1, row=0, rowspan=5, padx=5, sticky='wens')
        self.ef_lbl_local_intervencao.grid(
            column=2, row=0, padx=5, sticky='nw')
        self.ef_combo_local_intervencao.grid(
            column=2, row=1, padx=5, sticky='nwe')
        self.ef_lbl_modo_entrega.grid(
            column=3, row=0, columnspan=3, padx=5, sticky='nw')
        self.ef_combo_modo_entrega.grid(
            column=3, row=1, columnspan=3, padx=5, sticky='nwe')
        self.ef_combo_modo_entrega.bind(
            '<<ComboboxSelected>>', self.adicionar_morada_entrega)
        self.ef_lf_outros_dados.grid(column=0, row=0, sticky='wes')
        self.entryfr5.columnconfigure(0, weight=1)

        self.ef_lf_outros_dados.columnconfigure(0, weight=1)
        self.ef_lf_outros_dados.columnconfigure(1, weight=2)
        self.ef_lf_outros_dados.columnconfigure(2, weight=1)
        self.ef_lf_outros_dados.columnconfigure(3, weight=0)
        self.ef_lf_outros_dados.columnconfigure(4, weight=0)
        self.ef_lf_outros_dados.columnconfigure(5, weight=1)

        #--- acabaram os 'entryfr', apenas código geral para o entryframe a partir daqui ---
        self.entryframe.bind_all(
            "<Command-Escape>", self.fechar_painel_entrada)

    def adicionar_morada_entrega(self, *event):
        if self.ef_combo_modo_entrega.get() == "Enviar para outra morada...":
            self.ef_lbl_portes.grid(
                column=3, row=3, columnspan=3, padx=5, sticky='wens')
            self.ef_radio_portes_sim.grid(column=3, row=4, padx=5, sticky='wn')
            self.ef_radio_portes_nao.grid(column=4, row=4, padx=5, sticky='wn')
            self.ef_radio_portes_oferta.grid(
                column=5, row=4, padx=5, sticky='wn')
            self.ef_ltxt_morada_entrega.grid(
                column=6, row=0, rowspan=5, padx=5, sticky='wens')
            self.ef_lf_outros_dados.columnconfigure(6, weight=2)
            self.ef_ltxt_morada_entrega.scrolledtext.focus()
        elif self.ef_combo_modo_entrega.get() == "Enviar para a morada da ficha de cliente":
            self.ef_lbl_portes.grid(
                column=3, row=3, columnspan=3, padx=5, sticky='wens')
            self.ef_radio_portes_sim.grid(column=3, row=4, padx=5, sticky='wn')
            self.ef_radio_portes_nao.grid(column=4, row=4, padx=5, sticky='wn')
            self.ef_radio_portes_oferta.grid(
                column=5, row=4, padx=5, sticky='wn')
            self.ef_ltxt_morada_entrega.grid_remove()
            self.ef_lf_outros_dados.columnconfigure(6, weight=0)
        else:
            self.ef_lbl_portes.grid_remove()
            self.ef_radio_portes_sim.grid_remove()
            self.ef_radio_portes_nao.grid_remove()
            self.ef_radio_portes_oferta.grid_remove()
            self.ef_ltxt_morada_entrega.grid_remove()
            self.ef_lf_outros_dados.columnconfigure(6, weight=0)

    def atualizar_combo_local_intervencao(self):
        """ Atualizar a lista de locais de intervenção na combobox
            correspondente, obtendo info a partir da base de dados.
        """
        self.ef_combo_local_intervencao['values'] = obter_lista_fornecedores()

    def radio_tipo_command(self, *event):
        """
        Ajustes que devem ocorrer no formulário quando o utilizador altera o tipo de
        reparação (artigo de cliente ou de stock).
        """
        tipo = self.ef_var_tipo.get()
        if tipo == TIPO_REP_STOCK:
            self.ef_lf_fornecedor.grid(column=0, row=0, sticky='we')

            self.ef_ltxt_descr_equipamento.scrolledtext.configure(height=7)
            self.ef_ltxt_descr_equipamento.grid_configure(rowspan=8)

            widgets = (self.ef_lf_cliente,
                       self.ef_lbl_estado_equipamento,
                       self.ef_radio_estado_marcas_uso,
                       self.ef_radio_estado_bom,
                       self.ef_radio_estado_marcas_acidente,
                       self.ef_radio_estado_faltam_pecas,
                       self.ef_ltxt_obs_estado_equipamento,
                       self.ef_lbl_garantia,
                       self.ef_radio_garantia_fora_garantia,
                       self.ef_radio_garantia_neste,
                       self.ef_radio_garantia_noutro,
                       self.ef_ltxt_data_compra,
                       self.ef_ltxt_num_fatura,
                       self.ef_ltxt_local_compra,

                       self.ef_chkbtn_avaria_reprod_loja,
                       self.ef_ltxt_senha,
                       self.ef_lbl_find_my,
                       self.ef_radio_find_my_sim,
                       self.ef_radio_find_my_nao,
                       self.ef_radio_find_my_nao_aplic,
                       self.ef_lbl_efetuar_copia,
                       self.ef_radio_efetuar_copia_nao,
                       self.ef_radio_efetuar_copia_sim,
                       self.ef_radio_efetuar_copia_n_aplic,

                       self.ef_ltxt_acessorios_entregues,
                       self.ef_lbl_modo_entrega,
                       self.ef_combo_modo_entrega,
                       self.ef_lbl_local_intervencao,
                       self.ef_combo_local_intervencao,
                       self.ef_ltxt_morada_entrega,

                       self.ef_lbl_portes,
                       self.ef_radio_portes_sim,
                       self.ef_radio_portes_nao,
                       self.ef_radio_portes_oferta)
            for widget in widgets:
                widget.grid_remove()

            self.ef_ltxt_notas.grid(
                column=0, row=0, columnspan=7, rowspan=5, padx=5, sticky='wens')
            self.ef_ltxt_num_serie.label.configure(text="Nº de série")
            self.ef_ltxt_cod_artigo.label.configure(text="Código de artigo")
            self.ef_ltxt_cod_artigo.grid(
                column=2, row=0, rowspan=2, padx=5, sticky='we')
            self.ef_ltxt_num_serie.grid(
                column=2, row=2, rowspan=2, padx=5, sticky='we')
            self.ef_ltxt_num_fatura_fornecedor.grid(
                column=3, rowspan=2, row=0, padx=5, sticky='we')
            self.ef_ltxt_data_fatura_fornecedor.grid(
                column=3, row=2, rowspan=2, padx=5, sticky='we')
            self.ef_ltxt_nar.grid(
                column=3, row=4, rowspan=2, padx=5, sticky='we')
            self.ef_ltxt_num_guia_rececao.grid(
                column=4, row=0, rowspan=2, padx=5, sticky='we')
            self.ef_ltxt_data_entrada_stock.grid(
                column=4, row=2, rowspan=2, padx=5, sticky='we')
            self.ef_ltxt_num_quebra_stock.grid(
                column=4, row=4, rowspan=2, padx=5, sticky='we')
            self.ef_txt_num_fornecedor.focus()
        else:
            self.ef_ltxt_descr_equipamento.scrolledtext.configure(height=4)
            self.ef_ltxt_descr_equipamento.grid_configure(rowspan=5)

            widgets = (self.ef_lbl_estado_equipamento,
                       self.ef_radio_estado_marcas_uso,
                       self.ef_radio_estado_bom,
                       self.ef_radio_estado_marcas_acidente,
                       self.ef_radio_estado_faltam_pecas,
                       self.ef_ltxt_obs_estado_equipamento,
                       self.ef_lbl_garantia,
                       self.ef_radio_garantia_fora_garantia,
                       self.ef_radio_garantia_neste,
                       self.ef_radio_garantia_noutro,
                       self.ef_ltxt_data_compra,
                       self.ef_ltxt_num_fatura,
                       self.ef_lf_cliente,
                       self.ef_chkbtn_avaria_reprod_loja,
                       self.ef_ltxt_senha,
                       self.ef_lbl_find_my,
                       self.ef_radio_find_my_sim,
                       self.ef_radio_find_my_nao,
                       self.ef_radio_find_my_nao_aplic,
                       self.ef_lbl_efetuar_copia,
                       self.ef_radio_efetuar_copia_nao,
                       self.ef_radio_efetuar_copia_sim,
                       self.ef_radio_efetuar_copia_n_aplic,
                       self.ef_ltxt_acessorios_entregues,
                       self.ef_lbl_modo_entrega,
                       self.ef_combo_modo_entrega,
                       self.ef_lbl_local_intervencao,
                       self.ef_combo_local_intervencao)
            for widget in widgets:
                widget.grid()

            self.radio_garantia_command()

            widgets = (self.ef_lf_fornecedor,
                       self.ef_ltxt_nar,
                       self.ef_ltxt_num_fatura_fornecedor,
                       self.ef_ltxt_data_fatura_fornecedor,
                       self.ef_ltxt_num_guia_rececao,
                       self.ef_ltxt_data_entrada_stock,
                       self.ef_ltxt_num_quebra_stock)
            for widget in widgets:
                widget.grid_remove()

            self.ef_ltxt_num_serie.label.configure(text="\nNº de série")
            self.ef_ltxt_cod_artigo.label.configure(text="\nCódigo de artigo")
            self.ef_ltxt_cod_artigo.grid(column=0, row=5, padx=5, sticky='we')
            self.ef_ltxt_num_serie.grid(column=1, row=5, padx=5, sticky='we')

            self.ef_lf_outros_dados.configure(text="\nOutros dados")
            self.ef_ltxt_notas.grid(
                column=1, row=0, columnspan=1, rowspan=5, padx=5, sticky='wens')

            self.adicionar_morada_entrega()
            self.ef_txt_num_cliente.focus()

    def radio_estado_command(self, *event):
        print("RadioButton Estado Changed. New value:",
              self.ef_var_estado.get())  # obter o valor do campo "estado"

    def radio_garantia_command(self, *event):
        """
        Ajustes que devem ocorrer no formulário quando o utilizador altera o
        estado da elegibilidade para garantia.
        """
        garantia = self.ef_var_garantia.get()
        if garantia == GARANTIA_NOUTRO:
            self.ef_ltxt_local_compra.grid(
                column=4, row=5, padx=5, sticky='we')
            self.ef_ltxt_local_compra.entry.focus()
        else:
            self.ef_ltxt_local_compra.grid_remove()

    def radio_copia_command(self, *event):
        print("RadioButton Cópia de Segurança Changed. New value:",
              self.ef_var_efetuar_copia.get())  # obter o valor do campo "cópia"

    def radio_find_my(self, *event):
        print("RadioButton Find my iPhone Changed. New value:",
              self.ef_var_find_my.get())  # obter o valor do campo "Find my"

    def radio_portes_command(self, *event):
        print("RadioButton Portes Changed. New value:",
              self.ef_var_estado.get())  # obter o valor do campo "portes"

    def gerar_menu(self):
        # Menu da janela principal
        self.menu = tk.Menu(root)
        root.config(menu=self.menu)

        self.MenuFicheiro = tk.Menu(
            self.menu, postcommand=self.liga_desliga_menu_novo)

        self.menu.add_cascade(label="Ficheiro", menu=self.MenuFicheiro)
        self.MenuFicheiro.add_command(
            label="Nova reparação", command=self.mostrar_painel_entrada, accelerator="Command+n")

        self.MenuFicheiro.add_command(label="Novo contacto", command=lambda *x: self.create_window_contacts(
            criar_novo_contacto="Cliente"), accelerator="Command+t")
        self.MenuFicheiro.add_command(label="Nova remessa", command=lambda *x: self.create_window_remessas(
            criar_nova_remessa=True), accelerator="Command+r")
        self.MenuFicheiro.add_separator()
        self.MenuFicheiro.add_command(
            label="Pesquisar...", command=None, accelerator="Command+f")
        root.bind_all("<Command-n>", self.mostrar_painel_entrada)
        root.bind_all(
            "<Command-t>", lambda *x: self.create_window_contacts(criar_novo_contacto="Cliente"))
        root.bind_all(
            "<Command-r>", lambda *x: self.create_window_remessas(criar_nova_remessa=True))

        self.menuVis = tk.Menu(self.menu)
        self.menu.add_cascade(label="Visualização", menu=self.menuVis)
        self.menuVis.add_command(label="Mostrar/ocultar mensagens",
                                 command=self.abrir_painel_mensagens, accelerator="Command-1")
        self.menuVis.add_command(label="Mostrar/ocultar contactos",
                                 command=self.create_window_contacts, accelerator="Command-2")
        self.menuVis.add_command(label="Mostrar/ocultar remessas",
                                 command=self.create_window_remessas, accelerator="Command-3")
        self.menuVis.bind_all("<Command-KeyPress-1>",
                              self.abrir_painel_mensagens)
        self.menuVis.bind_all("<Command-KeyPress-2>",
                              self.create_window_contacts)
        self.menuVis.bind_all("<Command-KeyPress-3>",
                              self.create_window_remessas)

        self.windowmenu = tk.Menu(self.menu, name='window')
        self.menu.add_cascade(menu=self.windowmenu, label='Janela')
        self.windowmenu.add_separator()

        self.helpmenu = tk.Menu(self.menu)
        self.menu.add_cascade(label="Help", menu=self.helpmenu)
        #       helpmenu.add_command(label="Preferências", command=About)
        self.helpmenu.add_command(
            label="Acerca de " + __app_name__, command=about_window.about_window)
        self.helpmenu.add_command(label="Suporte da aplicação " + __app_name__, command=lambda: webbrowser.open(
            "http://victordomingos.com/contactos/", new=1, autoraise=True))
        self.helpmenu.add_command(
            label="Agradecimentos", command=about_window.thanks_window)
        self.helpmenu.add_separator()
        self.helpmenu.add_command(label="Visitar página do autor", command=lambda: webbrowser.open(
            "http://victordomingos.com", new=1, autoraise=True))
        #root.createcommand('::tk::mac::ShowPreferences', prefs_function)
        #root.bind('<<about-idle>>', about_dialog)
        #root.bind('<<open-config-dialog>>', config_dialog)
        root.createcommand('tkAboutDialog', about_window.about_window)

        #----------------Menu contextual tabela principal---------------------
        self.contextMenu = tk.Menu(self.menu)
        self.contextMenu.add_command(label="Informações", command=lambda: self.create_window_detalhe_rep(
            num_reparacao=self.reparacao_selecionada))
        #self.contextMenu.add_command(label="Abrir no site da transportadora", command=self.abrir_url_browser)
        self.contextMenu.add_separator()
        #self.contextMenu.add_command(label="Copiar número de objeto", command=self.copiar_obj_num)
        #self.contextMenu.add_command(label="Copiar mensagem de expedição", command=self.copiar_msg)
        # self.contextMenu.add_separator()
        #self.contextMenu.add_command(label="Arquivar/restaurar remessa", command=self.del_remessa)
        # self.contextMenu.add_separator()
        #self.contextMenu.add_command(label="Registar cheque recebido", command=self.pag_recebido)
        #self.contextMenu.add_command(label="Registar cheque depositado", command=self.chq_depositado)

        #----------------Menu contextual tabela de mensagens-------------------
        self.contextMenuMsg = tk.Menu(self.menu)
        self.contextMenuMsg.add_command(label="Visualizar Mensagem", command=lambda: self.create_window_detalhe_msg(
            num_mensagem=self.mensagem_selecionada))

    def liga_desliga_menu_novo(self, *event):
        """
        Liga e desliga menus com base na configuração atual da janela. Por exemplo, ao
        abrir o painel de entrada de dados, desativa o menu "nova reparação", para evitar
        que o painel se feche inadvertidamente.
        """
        if self.is_entryform_visible == True:
            self.MenuFicheiro.entryconfigure(
                "Nova reparação", state="disabled")
            # TODO - corrigir bug: o atalho de teclado só fica realmente inativo depois de acedermos ao menu ficheiro. Porquê??
            # root.unbind_all("<Command-n>")
        else:
            self.MenuFicheiro.entryconfigure("Nova reparação", state="active")
            # root.bind_all("<Command-n>")

    def on_save_repair(self, event=None):
        # reparacao = recolher todos os dados do formulário  #TODO
        reparacao = "teste"
        self.ultima_reparacao = db.save_repair(
            reparacao)  # TODO - None se falhar
        if self.ultima_reparacao:
            self.on_repair_save_success()
        else:
            wants_to_try_again_save = messagebox.askquestion(message='Não foi possível guardar o processo de reparação. Deseja tentar novamente?',
                                                             default='yes',
                                                             parent=self)
            if wants_to_try_again_save == 'yes':
                self.on_save_repair()
            else:
                self.on_repair_cancel()

    def on_repair_save_success(self):
        # TODO - criar um mecanismo para obter o número da reparação acabada de
        # introduzir na base de dados
        self.ultima_reparacao = "1234"
        wants_to_print = messagebox.askquestion(message='O processo de reparação foi guardado com sucesso. Deseja imprimir?',
                                                default='yes',
                                                parent=self)
        if wants_to_print == 'yes':
            imprimir.imprimir_folhas_de_reparacao(self.ultima_reparacao)
            self.fechar_painel_entrada()
        else:
            self.entryframe.focus()

    # TODO
    def on_repair_cancel(self, event=None):
        # caso haja informação introduzida no formulário TODO: verificar
        # primeiro
        wants_to_cancel = messagebox.askyesno(message='Tem a certeza que deseja cancelar a introdução de dados? Toda a informação não guardada será eliminada de forma irreversível.',
                                              default='no',
                                              parent=self)
        if wants_to_cancel:
            self.fechar_painel_entrada()
        else:
            self.entryframe.focus()

    def inserir_msg(self, processo, utilizador, data, texto):
        processo = str(processo)
        str_data = f"{data.day}/{data.month}/{data.year} às {data.hour}:{int(data.minute):02}"
        texto = textwrap.fill(texto, width=45)
        texto_final = f"{utilizador}, {str_data}\n﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘\n{texto}"
        #texto_final = f"[{utilizador}, {str_data}]\n﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘\n{texto}"
        ico = "✉️"
        self.msgtree.insert("", "end", values=(ico, processo, texto_final))

    def inserir_dados_de_exemplo(self):
        for i in range(1, 5):
            self.tree.insert("", "end", tag="", text="", values=(str(i), "José Manuel da Silva Rodrigues",
                                                                 "Artigo Muito Jeitoso (Early 2015)", "Substituição de ecrã", "Em processamento", "120"))
            self.tree.insert("", "end", text="", values=(str(i + 1), "Joana Manuela Rodrigues",
                                                         "Outro Artigo Bem Jeitoso", "Bateria não carrega", "Aguarda envio", "120"))
            self.tree.insert("", "end", tag="baixa", text="", values=(str(
                i + 2), "Maria Apolinário Gomes Fernandes", "Smartphone Daqueles Bons", "Substituição de ecrã", "Enviado", "15"))
            self.tree.insert("", "end", text="", tag="normal", values=(str(i + 3), "José Carvalho",
                                                                       "Computador do modelo ABCD", "Formatar disco e reinstalar sistema operativo", "Recebido", "1"))
            self.tree.insert("", "end", text="", tag="urgente", values=(str(
                i + 4), "Loja X", "Coisa que não funciona devidamente", "Substituição ao abrigo da garantia", "Aguarda entrega", "12"))
            self.tree.insert("", "end", text="", tag="baixa", values=(str(
                i + 5), "Loja X", "Coisa que devia funcionar melhor", "Substituição ao abrigo da garantia", "Entregue", "12"))

    def inserir_msgs_de_exemplo(self):
        now = datetime.datetime.now()
        for i in range(7):
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
    # sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding = 'utf-8')  # For Atom compatibility
    # sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding = 'utf-8')
    # # For Atom compatibility
    estado = AppStatus()
    root = tk.Tk()
    estado.janela_principal = App(root)
    root.configure(background='grey95')
    root.title('RepService')
    root.geometry(ROOT_GEOMETRIA)
    root.bind_all("<Mod2-q>", root.quit)

    # Remove bad AquaTk Button-2 (right) and Paste bindings.
    root.unbind_class('Text', '<B2>')
    root.unbind_class('Text', '<B2-Motion>')
    root.unbind_class('Text', '<<PasteSelection>>')

    root.unbind_class('TEntry', '<B2>')
    root.bind_class('Tentry', '<Button-2>', lambda: print("bla"))
    root.unbind_class('TEntry', '<B2-Motion>')
    root.unbind_class('TEntry', '<<PasteSelection>>')

    root.mainloop()
