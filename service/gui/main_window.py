#!/usr/bin/env python3
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

© 2018 Victor Domingos, Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)
"""

import textwrap
import webbrowser
import tkinter as tk
import tkinter.font
from tkinter import ttk, messagebox
from tkinter.scrolledtext import ScrolledText
from string import ascii_letters

from gui import detalhe_reparacao, about_window, contactos, detalhe_mensagem, remessas
from printing import imprimir
from gui.base_app import baseApp
from gui.extra_tk_classes import LabelEntry, LabelText, DatePicker
from misc.misc_funcs import txt_para_data, restart_program
from global_setup import *
from misc.constants import *


if USE_LOCAL_DATABASE:
    from local_db import db_main as db
else:
    from remote_db import db_main as db


class App(baseApp):
    """ Base class for the application. It starts by showing the login dialog
        and, after a successfull login, presents the application's main window
        (repair list).
    """
    def __init__(self, master, estado_app, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master = master
        self.estado_app = estado_app
        self.master.minsize(MASTER_MIN_WIDTH, MASTER_MIN_HEIGHT)
        self.master.maxsize(MASTER_MAX_WIDTH, MASTER_MAX_HEIGHT)
        self.a_editar_reparacao = False
        self.rep_newDetailsWindow = {}
        self.rep_detail_windows_count = 0
        self.msg_newDetailsWindow = {}
        self.msg_detail_windows_count = 0
        self.last_selected_view_repair_list = PROCESSOS_EM_CURSO
        self.nprocessos = 0
        self.nmensagens = 0
        self.reparacao_selecionada = None
        self.mensagem_selecionada = None
        self.ultima_reparacao = None
        self.username = None
        self.user_id = None
        self.password = None
        self.loggedin = False
        self.token = None
        self.failed_login_attempts = 0
        self.start_login_window()

    def start_login_window(self):
        """ Displays the login dialog.
        """
        self.root_login = tk.Toplevel()
        self.root_login.minsize(LOGIN_MIN_WIDTH, LOGIN_MIN_HEIGHT)
        #self.root_login.maxsize(LOGIN_MAX_WIDTH, LOGIN_MAX_HEIGHT)
        self.root_login.configure(background='grey92')
        self.root_login.resizable(width=False, height=False)
        self.root_login.title('Login')
        self.root_login.bind_all("<Mod2-q>", self.master.quit)

        self.log_mainframe = ttk.Frame(self.root_login, padding="13 15 13 10")
        self.log_logoframe = ttk.Frame(self.log_mainframe, padding="0 0 0 0")
        self.log_formframe = ttk.Frame(self.log_mainframe, padding="0 15 15 20")
        self.log_bottomframe = ttk.Frame(self.log_mainframe, padding="0 0 0 8")

        self.log_btnFont = tkinter.font.Font(family="Lucida Grande", size=10)
        self.log_btnTxtColor = "grey22"
        self.log_btnTxtColor_active = "white"

        w = self.root_login.winfo_screenwidth()
        h = self.root_login.winfo_screenheight()

        size = tuple(int(_) for _ in self.root_login.geometry().split('+')[0].split('x'))
        x = int(w / 2 - LOGIN_MIN_WIDTH / 2)
        y = int(h / 3 - LOGIN_MIN_HEIGHT / 2)
        self.root_login.geometry(f"{LOGIN_MIN_WIDTH}x{LOGIN_MIN_HEIGHT}+{x}+{y}")

        icon_path = APP_PATH + "/images/icon.gif"
        self.icon = tk.PhotoImage(file=icon_path)
        self.label_icon = ttk.Label(self.log_logoframe, image=self.icon)

        self.log_ltxt_username = LabelEntry(self.log_formframe,
                                            label="Nome de Utilizador",
                                            width=30)

        self.log_ltxt_password = LabelEntry(self.log_formframe,
                                            label="Palavra-passe",
                                            width=30)
        self.log_ltxt_password.entry.config(show="•")

        self.log_btn_alterar_senha = ttk.Button(self.log_bottomframe,
                                                text="Alterar palavra-passe…",
                                                command=self.change_password)

        self.log_btn_cancel = ttk.Button(self.log_bottomframe,
                                         text="Cancelar",
                                         command=exit)

        self.log_btn_enter = ttk.Button(self.log_bottomframe,
                                        text="Entrar",
                                        default="active",
                                        style="Active.TButton",
                                        command=self.validate_login)

        self.label_icon.bind('<Button-1>', about_window.AboutWindow)

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

        self.label_icon.pack(side=tk.TOP, pady=15, padx=30)
        self.log_ltxt_username.pack(side=tk.TOP, expand=False)
        self.log_ltxt_password.pack(side=tk.TOP, expand=False)
        self.log_btn_enter.pack(side=tk.RIGHT, padx=4)
        self.log_btn_cancel.pack(side=tk.RIGHT, padx=4)
        self.log_btn_alterar_senha.pack(side=tk.LEFT, padx=4)

        self.log_bottomframe.pack(side=tk.BOTTOM, expand=False, fill='x')
        self.log_logoframe.pack(side=tk.LEFT, expand=True, fill='both')
        self.log_formframe.pack(side=tk.RIGHT, expand=True, fill='both')
        self.log_mainframe.pack(side=tk.TOP, expand=True, fill='both')
        self.master.withdraw()


    def validate_login(self, *event):
        """ Checks if username and password entered are correct and, if so, it
            opens the aplication's main window. After 5 failed login attempts,
            the application closes immediately. The failed login attempts
            count is stored in a class property so that it is shared with the
            password change dialog.
        """
        username = self.log_ltxt_username.get()
        password = self.log_ltxt_password.get()

        self.loggedin, self.token = db.validate_login(username, password)

        if self.loggedin:
            self.failed_login_attempts = 0
            self.username = username
            self.password = password
            self.user_id = db.get_user_id(self.username)
            self.start_main_window()
            self.master.deiconify()
            self.root_login.destroy()
        else:
            self.failed_login_attempts += 1
            self.shake_window(self.root_login)
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
        """ Displays the password change dialog.
        """

        self.log_ltxt_username.entry.focus_set()
        self.root_chpwd = tk.Toplevel()
        self.root_chpwd.minsize(CHPWD_MIN_WIDTH, CHPWD_MIN_HEIGHT)
        #self.root_chpwd.maxsize(CHPWD_MAX_WIDTH, CHPWD_MAX_HEIGHT)
        self.root_chpwd.resizable(width=False, height=False)
        self.root_chpwd.configure(background='grey92')
        self.root_chpwd.title('Alterar Palavra-passe')

        self.chpwd_mainframe = ttk.Frame(self.root_chpwd, padding="13 25 13 10")
        #self.chpwd_topframe = ttk.Frame(self.chpwd_mainframe, padding="5 8 5 0")
        self.chpwd_centerframe = ttk.Frame(self.chpwd_mainframe, padding="0 5 0 5")
        self.chpwd_bottomframe = ttk.Frame(self.chpwd_mainframe, padding="0 20 0 8")

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

        self.chpwd_btn_cancel = ttk.Button(self.chpwd_bottomframe,
                                           text="Cancelar",
                                           command=self.root_chpwd.destroy)
        self.chpwd_btn_alterar = ttk.Button(self.chpwd_bottomframe,
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
        self.chpwd_btn_alterar.pack(side=tk.RIGHT, padx=4)
        self.chpwd_btn_cancel.pack(side=tk.RIGHT, padx=4)

        self.chpwd_bottomframe.pack(side=tk.BOTTOM, expand=False, fill='x')
        self.chpwd_centerframe.pack(side=tk.TOP, expand=True, fill='both')
        self.chpwd_mainframe.pack(side=tk.TOP, expand=True, fill='both')


    def validate_change_password(self, *event):
        """ Checks all the fields were filled correctly. After 5 failed login
            attempts, the application closes immediately. The failed login
            attempts count is stored in a class property so that it is shared
            with the login dialog.
        """
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
            self.failed_login_attempts = 0
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
            self.failed_login_attempts += 1
            if self.failed_login_attempts > 4:
                messagebox.showerror("",
                        "Os dados introduzidos não permitiram a sua "
                        "autenticação. Por favor contacte um administrador.\n"
                        "\nPor motivos de segurança, a aplicação irá agora "
                        "encerrar.")
                exit()
            else:
                self.chpwd_ltxt_username.clear()
                self.chpwd_ltxt_old_password.clear()
                self.chpwd_ltxt_username.entry.focus_set()


    def start_main_window(self):
        """ From here we start building the main window (repair list)
        """
        self.gerar_painel_mensagens()
        self.gerar_menu()
        self.montar_barra_de_ferramentas()
        self.montar_tabela()
        self.gerar_painel_entrada()

        self.composeFrames()

        self.my_statusbar.show_progress(value=30, mode="determinate")
        reps = db.obter_reparacoes_por_estados(PROCESSOS_EM_CURSO)
        self.my_statusbar.progress_update(60)
        self.atualizar_lista(reps)
        self.my_statusbar.progress_update(80)
        self.atualizar_lista_msgs()
        self.my_statusbar.progress_update(90)
        if self.contar_linhas(self.msgtree) > 0:
            #self.after(1200, self.abrir_painel_mensagens)
            self.abrir_painel_mensagens()

        self.my_statusbar.hide_progress(last_update=100)


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
        self.tree.bind('<<TreeviewSelect>>', self.selectItem)
        self.tree.bind('<Double-1>', lambda x: self.create_window_detalhe_rep(
            num_reparacao=self.reparacao_selecionada))
        self.tree.bind("<Button-2>", self.popupMenu)
        self.tree.bind("<Button-3>", self.popupMenu)

        self.msgtree.bind('<<TreeviewSelect>>', self.selectItemMsg)
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


    def selectItemMsg(self, *event):
        """
        Obter mensagem selecionada (após clique de rato na linha correspondente)
        """
        curItem = self.msgtree.focus()
        tree_linha = self.msgtree.item(curItem)

        mensagem = tree_linha["values"][1]
        remetente = tree_linha["values"][3].split(',', 1)[0]
        self.my_statusbar.set(f"{mensagem} • Mensagem enviada por {remetente}")
        self.mensagem_selecionada = mensagem

    def popupMenu(self, event):
        """action in event of button 3 on tree view"""
        # select row under mouse
        self.selectItem()
        self.update_idletasks()

        iid = self.tree.identify_row(event.y)
        x, y = event.x_root, event.y_root
        if iid:
            if x != 0 and y != 0:
                # mouse pointer over item
                self.tree.selection_set(iid)
                self.tree.focus(iid)
                self.contextMenu.post(event.x_root, event.y_root)
                #print("popupMenu(): x,y = ", event.x_root, event.y_root)
            else:
                #print("popupMenu(): wrong values for event - x=0, y=0")
                pass
        else:
            #print(iid)
            #print("popupMenu(): Else - No code here yet! (mouse not over item)")
            # mouse pointer not over item
            # occurs when items do not fill frame
            # no action required
            pass

    def popupMenuMsg(self, event):
        """action in event of button 3 on tree view"""
        # select row under mouse
        self.selectItemMsg()
        self.update_idletasks()

        iid = self.msgtree.identify_row(event.y)
        x, y = event.x_root, event.y_root
        if iid:
            if x != 0 and y != 0:
                # mouse pointer over item
                self.msgtree.selection_set(iid)
                self.msgtree.focus(iid)
                self.contextMenuMsg.post(event.x_root, event.y_root)
                #print("popupMenuMsg(): x,y = ", event.x_root, event.y_root)
            else:
                #print("popupMenuMsg(): wrong values for event - x=0, y=0")
                pass
        else:
            #print(iid)
            #print("popupMenuMsg(): Else - No code here yet! (mouse not over item)")
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

        num_rep = tree_linha["values"][0]
        equipamento = tree_linha["values"][2]
        num_serie = db.obter_num_serie(num_rep)
        self.my_statusbar.set(f"{equipamento} • {num_serie}")
        self.reparacao_selecionada = num_rep

    def montar_tabela(self):
        self.tree['columns'] = (
            'Nº', 'Cliente', 'Equipamento', 'Serviço', 'Estado', 'Dias')
        #self.tree.pack(side='top', expand=True, fill='both')
        self.tree.column('#0', anchor='w', minwidth=0, stretch=0, width=0)
        self.tree.column('Nº', anchor='e', minwidth=46, stretch=0, width=46)
        self.tree.column('Cliente', minwidth=40, stretch=1, width=120)
        self.tree.column('Equipamento', minwidth=40, stretch=1, width=160)
        self.tree.column('Serviço', minwidth=40, stretch=1, width=195)
        self.tree.column('Estado', minwidth=40, stretch=1, width=150)
        self.tree.column('Dias', anchor='e', minwidth=35, stretch=0, width=35)
        self.configurarTree()
        self.leftframe.grid_columnconfigure(0, weight=1)
        self.leftframe.grid_columnconfigure(1, weight=0)
        self.leftframe.grid_rowconfigure(0, weight=1)

        self.bind_tree()

    def montar_barra_de_ferramentas(self):
        self.btn_add = ttk.Button(self.topframe, text="➕", width=6, command=self.show_entryform)
        self.btn_add.grid(column=0, row=0)
        self.dicas.bind(self.btn_add, 'Criar novo processo de reparação. (⌘N)')
        self.label_add = ttk.Label(
            self.topframe, font=self.btnFont, foreground=self.btnTxtColor, text="Nova reparação")
        self.label_add.grid(column=0, row=1)

        # ----------- Botão com menu "Mostrar" --------------
        self.label_mbtn_mostrar = ttk.Label(self.topframe, font=self.btnFont,
            foreground=self.btnTxtColor, text="Mostrar processos…")
        self.mbtn_mostrar = ttk.Menubutton(self.topframe,
            text="Processos em curso", width=18)
        self.mbtn_mostrar.menu = tk.Menu(self.mbtn_mostrar, tearoff=0)
        self.mbtn_mostrar["menu"] = self.mbtn_mostrar.menu

        self.mbtn_mostrar.menu.add_command(label="Processos em curso",
            command=lambda status_list=PROCESSOS_EM_CURSO: self._on_repair_view_select(None, status_list=PROCESSOS_EM_CURSO),
            accelerator="Command-4")

        self.mbtn_mostrar.menu.add_command(label="Processos finalizados",
            command=lambda estados=PROCESSOS_FINALIZADOS: self._on_repair_view_select(None, status_list=PROCESSOS_FINALIZADOS),
            accelerator="Command-5")

        self.mbtn_mostrar.menu.add_command(label="Todos os processos",
            command=lambda estados=[]:self._on_repair_view_select(None, status_list=[]),
            accelerator="Command-6")
        self.mbtn_mostrar.menu.add_separator()


        for estado in ESTADOS:
            self.mbtn_mostrar.menu.add_command(label=ESTADOS[estado],
                command=lambda estado=estado: self._on_repair_view_select(None, status_list=[estado]))

        self.mbtn_mostrar.grid(column=1, row=0)
        self.label_mbtn_mostrar.grid(column=1, row=1)
        self.dicas.bind(self.mbtn_mostrar,
            'Mostrar apenas uma parte dos processos,\n'
            'filtrando-os com base do seu estado atual.')
        # ----------- fim de Botão com menu "Mostrar" -------------

        """
        self.btn_sair = ttk.Button(self.topframe, text="x", width=3,
            command=restart_program)
        self.btn_sair.grid(column=2, row=0)
        ttk.Label(self.topframe, font=self.btnFont, foreground=self.btnTxtColor, text="Terminar sessão").grid(column=2, row=1)
        self.dicas.bind(self.btn_sair, "Terminar sessão.")
        """

        self.btn_detalhes = ttk.Button(self.topframe, text=" ℹ️️", width=3,
            command=lambda: self.create_window_detalhe_rep(num_reparacao=self.reparacao_selecionada))
        self.btn_detalhes.grid(column=6, row=0)
        ttk.Label(self.topframe, font=self.btnFont,
                  foreground=self.btnTxtColor, text="Detalhes").grid(column=6, row=1)
        self.dicas.bind(
            self.btn_detalhes, 'Apresentar detalhes do processo\nde reparação selecionado. (⌘I)')

        # ----------- Botão com menu "Alterar estado" --------------
        self.label_mbtn_alterar = ttk.Label(self.topframe, font=self.btnFont,
            foreground=self.btnTxtColor,text="Alterar estado")
        self.mbtn_alterar = ttk.Menubutton(self.topframe, text="•••", style="TMenubutton")
        self.mbtn_alterar.menu = tk.Menu(self.mbtn_alterar, tearoff=0)
        self.mbtn_alterar["menu"] = self.mbtn_alterar.menu

        for estado in ESTADOS:
            if estado in (ENTREGUE, ABANDONADO):
                self.mbtn_alterar.menu.add_separator()
            self.mbtn_alterar.menu.add_command(label=ESTADOS[estado],
                command=lambda estado=estado:self._on_repair_state_change(estado))

        self.mbtn_alterar.grid(column=7, row=0)
        self.label_mbtn_alterar.grid(column=7, row=1)
        self.dicas.bind(self.mbtn_alterar, 'Alterar o estado do processo\nde reparação selecionado.')
        # ----------- fim de Botão com menu "Alterar estado" -------------


        self.btn_entregar = ttk.Button(self.topframe, text=" ✅", width=3,
            command=lambda:self._on_repair_state_change(ENTREGUE))
        self.btn_entregar.grid(column=8, row=0)
        self.label_entregar = ttk.Label(self.topframe, font=self.btnFont,
            foreground=self.btnTxtColor, text="Entregar")
        self.label_entregar.grid(column=8, row=1)
        self.dicas.bind(self.btn_entregar, 'Marcar o processo de reparação\nselecionado como entregue.')

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

        letras_etc = ascii_letters + "01234567890-., "
        for char in letras_etc:
            keystr = '<KeyRelease-' + char + '>'
            self.text_input_pesquisa.bind(keystr, self.mostrar_pesquisa)
        self.text_input_pesquisa.bind('<Button-1>', self.clique_a_pesquisar_reps)
        self.text_input_pesquisa.bind('<KeyRelease-Escape>', self._on_sair_da_pesquisa)
        self.text_input_pesquisa.bind('<Command-a>', lambda x: self.text_input_pesquisa.select_range(0, tk.END))


        for col in range(1, 16):
            self.topframe.columnconfigure(col, weight=0)
        #self.topframe.columnconfigure(3, weight=1)
        self.topframe.columnconfigure(5, weight=1)
        self.topframe.columnconfigure(11, weight=1)

    def create_window_remessas(self, *event, criar_nova_remessa=None):
        # TODO: as janelas de contactos e remesas não são destruídas
        # corretamente, ficam sempre na memória e no menu. Como resolver?

        if not self.estado_app.janela_remessas_aberta:
            if criar_nova_remessa:
                #print("A abrir a janela de remessas, vamos lá criar uma nova remessa!")
                self.estado_app.painel_nova_remessa_aberto = True
            #self.newWindow2 = tk.Toplevel(self.master)
            self.estado_app.janela_remessas = tk.Toplevel(self.master)
            self.janela_remessas = remessas.RemessasWindow(
                self.estado_app.janela_remessas, self.estado_app)
            self.estado_app.janela_remessas_aberta = True
            self.estado_app.janela_remessas.wm_protocol(
                "WM_DELETE_WINDOW", self.close_window_remessas)
        else:
            if not criar_nova_remessa:
                self.close_window_remessas()
            else:
                self.estado_app.painel_nova_remessa_aberto = True
                self.janela_remessas.mostrar_painel_entrada()

    def close_window_remessas(self, *event):
        self.master.update_idletasks()

        if self.janela_remessas.is_entryform_visible:
            self.janela_remessas.on_remessa_cancel()
            if not self.estado_app.painel_nova_remessa_aberto:
                self.janela_remessas.is_entryform_visible = False
                self.janela_remessas.liga_desliga_menu_novo()
            self.bind_all("<Command-r>", lambda
                *x: self.create_window_remessas(criar_nova_remessa=True))

        self.estado_app.janela_remessas_aberta = False
        self.estado_app.painel_nova_remessa_aberto = False
        self.estado_app.janela_remessas.destroy()

    def create_window_contacts(self, *event, criar_novo_contacto=None, pesquisar=None):
        #self.estado_app.contacto_para_nova_reparacao = nova_reparacao
        self.estado_app.tipo_novo_contacto = criar_novo_contacto

        if self.estado_app.janela_contactos_aberta:
            if criar_novo_contacto:
                self.estado_app.painel_novo_contacto_aberto = True
                self.janela_contactos.mostrar_painel_entrada()
            elif pesquisar:
                self.janela_contactos.clique_a_pesquisar()
            else:
                self.close_window_contactos()
        else:
            if criar_novo_contacto in ["Cliente", "Fornecedor"]:
                print("Sim:", criar_novo_contacto)
                self.estado_app.painel_novo_contacto_aberto = True
            self.estado_app.janela_contactos = tk.Toplevel(self.master)
            self.janela_contactos = contactos.ContactsWindow(
                self.estado_app.janela_contactos, self.estado_app, pesquisar)
            self.estado_app.janela_contactos_aberta = True
            self.estado_app.janela_contactos.wm_protocol(
                "WM_DELETE_WINDOW", self.close_window_contactos)

    def close_window_contactos(self, *event):
        self.master.update_idletasks()

        if self.janela_contactos.is_entryform_visible:
            self.janela_contactos.on_contact_cancel()
            if not self.estado_app.painel_novo_contacto_aberto:
                self.janela_contactos.is_entryform_visible = False
                self.janela_contactos.liga_desliga_menu_novo()
            self.bind_all("<Command-t>", lambda
                *x: self.create_window_contacts(criar_novo_contacto="Cliente"))

        if self.estado_app.contacto_para_nova_reparacao:
            if self.estado_app.tipo_novo_contacto == "Cliente":
                self.ef_txt_num_cliente.focus()
                self.ef_txt_num_cliente.delete(0, tk.END)
                self.ef_txt_num_cliente.insert(0, self.estado_app.contacto_para_nova_reparacao)
            elif self.estado_app.tipo_novo_contacto == "Fornecedor":
                self.ef_txt_num_fornecedor.focus()
                self.ef_txt_num_fornecedor.delete(0, tk.END)
                self.ef_txt_num_fornecedor.insert(0, self.estado_app.contacto_para_nova_reparacao)
            else:
                print("Qual é afinal o tipo de contacto a criar???")
                pass

        self.estado_app.janela_contactos_aberta = False
        self.estado_app.painel_novo_contacto_aberto = False
        self.estado_app.janela_contactos.destroy()
        self.ef_ltxt_descr_equipamento.scrolledtext.focus()

    def create_window_detalhe_rep(self, *event, num_reparacao=None):
        if num_reparacao is None:
            messagebox.showwarning("", "Nenhuma reparação selecionada. Por favor selecione primeiro uma reparação.")
            self.master.focus_force()
            return

        self.rep_detail_windows_count += 1
        self.rep_newDetailsWindow[self.rep_detail_windows_count] = tk.Toplevel(
        )
        self.janela_detalhes_rep = detalhe_reparacao.repairDetailWindow(
            self.rep_newDetailsWindow[self.rep_detail_windows_count], num_reparacao, self.estado_app)

    def create_window_detalhe_msg(self, *event, num_mensagem=None):
        self.selectItemMsg()
        self.master.update_idletasks()

        if num_mensagem is None:
            messagebox.showwarning("", "Nenhuma mensagem selecionada. Por favor selecione primeiro uma mensagem.")
            self.master.focus_force()
            return

        self.msg_detail_windows_count += 1
        self.msg_newDetailsWindow[self.msg_detail_windows_count] = tk.Toplevel(
        )
        self.janela_detalhes_msg = detalhe_mensagem.msgDetailWindow(
            self.msg_newDetailsWindow[self.msg_detail_windows_count], num_mensagem, self.estado_app)

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
        self.msgtree['columns'] = ('ico', "msg_id", 'Processo', 'Mensagem')
        self.msgtree.column('#0', anchor='w', minwidth=0, stretch=0, width=0)
        self.msgtree.column('ico', anchor='nw',
                            minwidth=35, stretch=0, width=35)
        self.msgtree.column('msg_id', anchor='w', minwidth=0, stretch=0, width=0)
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
        self.master.update_idletasks()
        if self.estado_app.painel_mensagens_aberto == False:
            self.atualizar_lista_msgs()
            self.estado_app.painel_mensagens_aberto = True
            self.mensagens_frame.pack()
            self.messagepane.pack(side='top', expand=True, fill='both')
            self.rightframe.grid()
            self.alternar_cores(self.msgtree, inverso=False, fundo1='grey96')
            self.atualizar_soma_msgs()
        else:
            self.fechar_painel_mensagens()

    def fechar_painel_mensagens(self, *event):
        self.master.update_idletasks()
        self.estado_app.painel_mensagens_aberto = False
        self.messagepane.pack_forget()
        self.mensagens_frame.pack_forget()
        self.rightframe.grid_remove()

    def mostrar_painel_entrada(self, *event):
        self.MenuFicheiro.entryconfig("Nova reparação", state="disabled")
        # self.master.unbind_all("<Command-n>")
        if self.estado_app.painel_mensagens_aberto:
            self.estado_app.painel_mensagens_estava_aberto = True
            self.fechar_painel_mensagens()
        self.show_entryform()

        self.estado_app.painel_nova_reparacao_aberto = self.is_entryform_visible

        print(self.estado_app.contacto_para_nova_reparacao, self.estado_app.tipo_novo_contacto)
        if self.estado_app.contacto_para_nova_reparacao:
            if self.estado_app.tipo_novo_contacto == "Cliente":
                self.ef_txt_num_cliente.delete(0, tk.END)
                self.ef_txt_num_cliente.insert(0, str(self.estado_app.contacto_para_nova_reparacao))
                self.ef_ltxt_descr_equipamento.focus()
                self.ef_txt_num_cliente.bind("<FocusOut>", self._on_num_contact_exit)
            else:
                self.ef_txt_num_fornecedor.delete(0, tk.END)
                self.ef_txt_num_fornecedor.insert(0, str(self.estado_app.contacto_para_nova_reparacao))
                self.ef_ltxt_descr_equipamento.focus()
                self.ef_txt_num_fornecedor.bind("<FocusOut>", self._on_num_contact_exit)
        else:
            self.ef_txt_num_cliente.bind("<FocusOut>", self._on_num_contact_exit)
            self.ef_txt_num_fornecedor.bind("<FocusOut>", self._on_num_contact_exit)


        self.entryframe.bind_all("<Command-Escape>", self.fechar_painel_entrada)

    def fechar_painel_entrada(self, *event):
        self.ef_txt_num_cliente.unbind_all("<FocusOut>")
        self.ef_txt_num_fornecedor.unbind_all("<FocusOut>")
        self.hide_entryform()
        self.clear_text()
        self.master.focus_force()
        self.tree.focus()
        self.estado_app.painel_nova_reparacao_aberto = self.is_entryform_visible
        self.estado_app.tipo_novo_contacto = "Cliente"
        self.estado_app.contacto_para_nova_reparacao = None
        if self.estado_app.painel_mensagens_estava_aberto:
            self.abrir_painel_mensagens()
        # self.master.bind_all("<Command-n>")

    def clear_text(self):
        self.entryframe.focus()
        self.ef_radio_tipo_cliente.focus_set()
        self.ef_var_tipo.set(0)
        self.ef_var_estado.set(0)
        self.ef_var_garantia.set(0)
        self.ef_var_reprod_loja.set(0)
        self.ef_var_efetuar_copia.set(0)
        self.ef_var_find_my.set(0)
        self.ef_var_local_intervencao.set("Loja X")
        self.ef_var_modo_entrega.set(MODOS_ENTREGA[LEVANTAMENTO])
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
        self.ef_var_reprod_loja = tk.IntVar()
        self.ef_var_reprod_loja.set(0)
        self.ef_var_efetuar_copia = tk.IntVar()
        self.ef_var_find_my = tk.IntVar()
        self.ef_var_local_intervencao = tk.StringVar()
        self.ef_var_local_intervencao.set("Loja X") #TODO: obter a loja a que pertence o utilizador atual
        self.ef_var_modo_entrega = tk.StringVar()
        self.ef_var_modo_entrega.set(MODOS_ENTREGA[LEVANTAMENTO])
        self.ef_var_portes = tk.IntVar()

        # entryfr1-----------------------------
        self.ef_cabecalho = ttk.Frame(self.entryfr1, padding=4)
        self.ef_lbl_titulo = ttk.Label(
            self.ef_cabecalho, style="Panel_Title.TLabel", text="Adicionar Reparação:")
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

        self.ef_lbl_titulo.grid(column=0, row=0, columnspan=3, sticky='w', pady="0 10")
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
        self.dicas.bind(self.ef_txt_num_cliente, 'Introduzir o número de cliente.')
        self.ef_btn_buscar_cliente = ttk.Button(
            self.ef_lf_cliente, width=1, text="+", command=lambda *x: self.create_window_contacts(criar_novo_contacto="Cliente"))
        self.dicas.bind(self.ef_btn_buscar_cliente,
                        'Criar novo contacto.\nUtilize esta opção caso o cliente não tenha\nainda ficha criada nesta base de dados. (⌘T)')
        self.ef_txt_nome_cliente = ttk.Entry(
            self.ef_lf_cliente, font=("Helvetica-Neue", 12), width=45)
        self.ef_lbl_telefone_lbl = ttk.Label(
            self.ef_lf_cliente, style="Panel_Body.TLabel", text="Tel.:")
        self.ef_lbl_telefone_info = ttk.Label(
            self.ef_lf_cliente, style="Panel_Body.TLabel", text="")
        self.ef_lbl_email_lbl = ttk.Label(
            self.ef_lf_cliente, style="Panel_Body.TLabel", text="Email:")
        self.ef_lbl_email_info = ttk.Label(
            self.ef_lf_cliente, style="Panel_Body.TLabel", text="")

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
            self.ef_lf_fornecedor, style="Panel_Body.TLabel", text="")
        self.ef_lbl_email_lbl_fornecedor = ttk.Label(
            self.ef_lf_fornecedor, style="Panel_Body.TLabel", text="Email:")
        self.ef_lbl_email_info_fornecedor = ttk.Label(
            self.ef_lf_fornecedor, style="Panel_Body.TLabel", text="")

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
            self.entryfr3, padding=4, style="Panel_Section_Title.TLabelframe", text="Dados do equipamento")
        self.ef_ltxt_descr_equipamento = LabelText(
            self.ef_lf_equipamento, "Descrição:", style="Panel_Body.TLabel", width=30, height=5)
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
            self.ef_lf_equipamento, "Observações acerca do estado:", style="Panel_Body.TLabel", width=27, height=5)

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
        self.cal_data_compra = DatePicker(self.entryframe, self.ef_ltxt_data_compra)
        self.ef_ltxt_data_compra.bind('<FocusIn>', self._on_data_compra_enter)
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
        self.cal_fat_fornecedor = DatePicker(self.entryframe, self.ef_ltxt_data_fatura_fornecedor)
        self.ef_ltxt_data_fatura_fornecedor.bind('<FocusIn>', self._on_data_fatura_forn_enter)

        self.ef_ltxt_nar = LabelEntry(
            self.ef_lf_equipamento, "NAR:", style="Panel_Body.TLabel", width=15)
        self.ef_ltxt_num_guia_rececao = LabelEntry(
            self.ef_lf_equipamento, "Guia de receção:", style="Panel_Body.TLabel", width=15)

        self.ef_ltxt_data_entrada_stock = LabelEntry(
            self.ef_lf_equipamento, "Data de entrada em stock:", style="Panel_Body.TLabel", width=15)
        self.cal_entr_stk = DatePicker(self.entryframe, self.ef_ltxt_data_entrada_stock)
        self.ef_ltxt_data_entrada_stock.bind('<FocusIn>', self._on_data_entrada_stock)
        self.ef_ltxt_data_entrada_stock.bind('<FocusOut>', self.close_calendars)

        self.ef_ltxt_num_quebra_stock = LabelEntry(
            self.ef_lf_equipamento, "Nº de quebra de stock:", style="Panel_Body.TLabel", width=15)

        self.ef_ltxt_descr_equipamento.grid(
            column=0, columnspan=2, rowspan=5, row=0, padx=5, sticky='wens')
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
            self.entryfr4, padding=4, style="Panel_Section_Title.TLabelframe", text="Avaria e/ou serviço a realizar")
        self.ef_text_descr_avaria_servico = tk.Text(self.ef_lf_servico, highlightcolor="LightSteelBlue2", font=(
            "Helvetica-Neue", 12), wrap='word', width=20, height=4)
        self.ef_chkbtn_avaria_reprod_loja = ttk.Checkbutton(
            self.ef_lf_servico, variable=self.ef_var_reprod_loja, style="Panel_Body.Checkbutton", width=27, text="Avaria reproduzida na loja")
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
        #self.ef_lbl_espaco.grid(column=8, row=2, sticky='w')
        self.ef_lbl_efetuar_copia.grid(
            column=6, row=3, columnspan=3, padx=5, pady="6 0", sticky='w')
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
            self.entryfr5, padding=4, style="Panel_Section_Title.TLabelframe", text="Outros dados")
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
                                                  values=(list(MODOS_ENTREGA.values())),
                                                  state='readonly')

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
        self.entryframe.bind_all(
            "<Escape>", self.close_calendars)

    def close_calendars(self, *event):
        self.cal_data_compra.close_calendar()
        self.cal_fat_fornecedor.close_calendar()
        self.cal_entr_stk.close_calendar()

    def _on_data_compra_enter(self, *event):
        self.cal_data_compra.show()
        self.cal_fat_fornecedor.close_calendar()
        self.cal_entr_stk.close_calendar()

    def _on_data_fatura_forn_enter(self, *event):
        self.cal_fat_fornecedor.show()
        self.cal_data_compra.close_calendar()
        self.cal_entr_stk.close_calendar()

    def _on_data_entrada_stock(self, *event):
        self.cal_entr_stk.show()
        self.cal_data_compra.close_calendar()
        self.cal_fat_fornecedor.close_calendar()

    def _on_num_contact_exit(self, event):
        """ Preencher nome do cliente/fornecedor ao sair do campo do numero de contacto
        """
        def limpar_dados_fornecedor():
            self.ef_txt_num_fornecedor.delete(0, tk.END)
            self.ef_txt_nome_fornecedor.delete(0, tk.END)
            self.ef_lbl_telefone_info_fornecedor.config(text='')
            self.ef_lbl_email_info_fornecedor.config(text='')

        def limpar_dados_cliente():
            self.ef_txt_num_cliente.delete(0, tk.END)
            self.ef_txt_nome_cliente.delete(0, tk.END)
            self.ef_lbl_telefone_info.config(text='')
            self.ef_lbl_email_info.config(text='')

        tipo = self.ef_var_tipo.get()
        if tipo == TIPO_REP_STOCK:
            num_contacto = self.ef_txt_num_fornecedor.get().strip()
            print("DEBUG: suposto fornecedor:", num_contacto)
            if len(num_contacto)<1:
                limpar_dados_fornecedor()
                return

            contacto = db.obter_info_contacto(num_contacto, "Fornecedor")
            if contacto:
                self.ef_txt_nome_fornecedor.delete(0, tk.END)
                self.ef_txt_nome_fornecedor.insert(0,contacto['nome'])
                self.ef_lbl_telefone_info_fornecedor.config(text=contacto['telefone'])
                self.ef_lbl_email_info_fornecedor.config(text=contacto['email'])
            else:
                criar_contacto_forn = messagebox.askyesno("", "Não existe um fornecedor com o número indicado. Pretende criar um novo contacto?")
                limpar_dados_fornecedor()
                if criar_contacto_forn:
                    self.create_window_contacts(criar_novo_contacto="Fornecedor")
        else:
            num_contacto = self.ef_txt_num_cliente.get()
            if len(num_contacto)<1:
                return
            contacto = db.obter_info_contacto(num_contacto, "Cliente")
            if contacto:
                self.ef_txt_nome_cliente.delete(0, tk.END)
                self.ef_txt_nome_cliente.insert(0, contacto['nome'])
                self.ef_lbl_telefone_info.config(text=contacto['telefone'])
                self.ef_lbl_email_info.config(text=contacto['email'])
            else:
                criar_contacto_cliente = messagebox.askyesno("", "Não existe um cliente com o número indicado. Pretende criar um novo contacto?")
                limpar_dados_cliente()
                if criar_contacto_cliente:
                    self.create_window_contacts(criar_novo_contacto="Cliente")

    def adicionar_morada_entrega(self, *event):
        if self.ef_combo_modo_entrega.get() == MODOS_ENTREGA[ENVIAR_NOVA_MORADA]:
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
        elif self.ef_combo_modo_entrega.get() == MODOS_ENTREGA[ENVIAR_MORADA_FICHA]:
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
        fornecedores = db.obter_lista_fornecedores()
        lista_forn = [f"{forn['id']} - {forn['nome']}" for forn in fornecedores]
        self.ef_combo_local_intervencao['values'] = lista_forn


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

            self.ef_lf_outros_dados.configure(text="Outros dados")
            self.ef_ltxt_notas.grid(
                column=1, row=0, columnspan=1, rowspan=5, padx=5, sticky='wens')

            self.adicionar_morada_entrega()
            self.ef_txt_num_cliente.focus()


    def _on_repair_state_change(self, new_status):
        if not self.reparacao_selecionada:
            messagebox.showwarning("", "Nenhuma reparação selecionada. Por favor selecione primeiro uma reparação.")
            return
        reparacao = db.obter_reparacao(self.reparacao_selecionada)
        if reparacao['estado_reparacao'] == new_status:
            self.popupMsg(f"A reparação nº {self.reparacao_selecionada} já tinha o estado selecionado.\nNenhuma alteração efetuada.")
            return
        db.update_repair_status(self.reparacao_selecionada, new_status)
        self.popupMsg(f"A atualizar o estado da reparação nº {self.reparacao_selecionada} para: {ESTADOS[new_status]}")
        if new_status == ENTREGUE:
            pass # TODO: procedimentos de entrega (registo do serviço realizado, verificar se há equipamentos emprestados, gerar documentos para impressão...)


    def _on_repair_view_select(self, *event, status_list=None):
        self.cancelar_pesquisa()
        self.reparacao_selecionada = None
        if not status_list:
            status_list = []

        self.my_statusbar.show_progress(mode='determinate', value=25)

        if not status_list:
            self.mbtn_mostrar.configure(text="Todos os processos")
            self.my_statusbar.set("A consultar a base de dados. Esta operação poderá demorar. Por favor, aguarde.")
            reparacoes = db.obter_todas_reparacoes()
        else:
            if len(status_list) == 1:
                txt = f"{ESTADOS[status_list[0]]}"
                self.mbtn_mostrar.configure(text=txt)
                self.my_statusbar.set(f"A consultar a lista de processos ({txt.lower()}) na base de dados.")
            elif status_list == PROCESSOS_FINALIZADOS:
                txt = "Processos finalizados"
                self.mbtn_mostrar.configure(text=txt)
                self.my_statusbar.set(f"A consultar a lista de {txt.lower()} na base de dados. Esta operação poderá demorar. Por favor, aguarde.")
            elif status_list == PROCESSOS_EM_CURSO:
                txt = "Processos em curso"
                self.mbtn_mostrar.configure(text=txt)
                self.my_statusbar.set(f"A consultar a lista de {txt.lower()} na base de dados.")
            reparacoes = db.obter_reparacoes_por_estados(status_list)

        self.my_statusbar.progress_update(75)
        self.last_selected_view_repair_list = status_list
        self.atualizar_lista(reparacoes)
        self.my_statusbar.hide_progress(last_update=100)


    def clique_a_pesquisar_contactos(self, *event):
        self.create_window_contacts(criar_novo_contacto=None, pesquisar=True)


    def clique_a_pesquisar_reps(self, *event):
        self.text_input_pesquisa.focus_set()
        self.my_statusbar.set("Por favor, introduza o texto a pesquisar na base de dados.")


    def _on_sair_da_pesquisa(self, event):
        self.cancelar_pesquisa()
        self._on_repair_view_select(None, status_list=self.last_selected_view_repair_list)


    def cancelar_pesquisa(self):
        self.text_input_pesquisa.delete(0, tk.END)
        self.tree.focus_set()


    def mostrar_pesquisa(self, *event):
        termo_pesquisa = self.text_input_pesquisa.get()
        termo_pesquisa = termo_pesquisa.strip()

        # regressar ao campo de pesquisa caso não haja texto a pesquisar (resolve questão do atalho de teclado)

        if len(termo_pesquisa) < 1:
        #    reparacoes = local_db.obter_reparacoes_por_estados(self.last_selected_view_repair_list)
        #    self.atualizar_lista(reparacoes)
            return
        elif (len(termo_pesquisa) < 4) and not self.isNumeric(termo_pesquisa):
            return
        else:
            print("Else:", termo_pesquisa, self.isNumeric(termo_pesquisa))
        print(termo_pesquisa, len(termo_pesquisa))
        self.my_statusbar.clear()
        self.my_statusbar.set(f"A pesquisar: {termo_pesquisa}")

        estados = []
        if self.last_selected_view_repair_list == estados:
            estados = list(ESTADOS.keys())
        else:
            estados = self.last_selected_view_repair_list

        self.my_statusbar.show_progress(mode='determinate', value=30)
        reparacoes = db.pesquisar_reparacoes(termo_pesquisa, estados=estados)
        self.my_statusbar.progress_update(90)
        self.atualizar_lista(reparacoes)

        self.nprocessos = len(reparacoes)
        em_curso = 0
        for rep in reparacoes:
            if rep['estado'] in PROCESSOS_EM_CURSO:
                em_curso += 1

        if self.nprocessos == 0:
            s_status = f"""Pesquisa: {'"'+termo_pesquisa.upper()+'"'}. Não foi encontrado nenhum processo com o termo de pesquisa introduzido."""
        else:
            s_status = f"""Pesquisa: {'"'+termo_pesquisa.upper()+'"'}. Encontrados {self.nprocessos} processos ({em_curso} em curso)."""
        self.my_statusbar.set(s_status)
        self.my_statusbar.hide_progress(last_update=100)


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
        self.menu = tk.Menu(self.master)
        self.master.config(menu=self.menu)

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
            label="Pesquisar reparações...", command=self.clique_a_pesquisar_reps, accelerator="Command+f")
        self.MenuFicheiro.bind_all("<Command-f>", self.clique_a_pesquisar_reps)
        self.MenuFicheiro.add_command(
            label="Pesquisar contactos...", command=self.clique_a_pesquisar_contactos, accelerator="Shift+Command+f")
        self.MenuFicheiro.bind_all("<Shift-Command-f>", self.clique_a_pesquisar_contactos)
        self.MenuFicheiro.add_separator()
        self.MenuFicheiro.add_command(
            label=f"Terminar sessão de {self.username}…", command=self.logout_user, accelerator="Shift+Command+l")
        self.MenuFicheiro.bind_all("<Shift-Command-l>", self.logout_user)

        self.master.bind_all("<Command-n>", self.mostrar_painel_entrada)
        self.master.bind_all(
            "<Command-t>", lambda *x: self.create_window_contacts(criar_novo_contacto="Cliente"))
        self.master.bind_all(
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
        self.menuVis.add_separator()
        self.menuMostraProcessos = tk.Menu(self.menuVis)
        self.menuVis.add_cascade(label="Mostrar processos...", menu=self.menuMostraProcessos)

        self.menuMostraProcessos.add_command(label="Processos em curso",
            command=lambda status_list=PROCESSOS_EM_CURSO:
                self._on_repair_view_select(status_list=PROCESSOS_EM_CURSO),
            accelerator="Command-4")
        self.menuVis.bind_all("<Command-KeyPress-4>",
            lambda status_list=PROCESSOS_EM_CURSO:
                self._on_repair_view_select(None, status_list=PROCESSOS_EM_CURSO))


        self.menuMostraProcessos.add_command(label="Processos finalizados",
            command=lambda estados=PROCESSOS_FINALIZADOS:
                self._on_repair_view_select(None, status_list=PROCESSOS_FINALIZADOS),
            accelerator="Command-5")
        self.menuVis.bind_all("<Command-KeyPress-5>",
            lambda estados=PROCESSOS_FINALIZADOS:
                self._on_repair_view_select(None, status_list=PROCESSOS_FINALIZADOS))
        self.menuMostraProcessos.add_command(label="Todos os processos",
            command=lambda estados=[]:self._on_repair_view_select(None, status_list=None),
            accelerator="Command-6")
        self.menuVis.bind_all("<Command-KeyPress-6>",
            lambda estados=[]:self._on_repair_view_select(None, status_list=None))
        self.menuMostraProcessos.add_separator()

        for estado in ESTADOS:
            self.menuMostraProcessos.add_command(label=ESTADOS[estado],
                command=lambda estado=estado:self._on_repair_view_select(None, status_list=[estado]))

        self.windowmenu = tk.Menu(self.menu, name='window')
        self.menu.add_cascade(menu=self.windowmenu, label='Janela')
        self.windowmenu.add_separator()

        self.helpmenu = tk.Menu(self.menu)
        self.menu.add_cascade(label="Help", menu=self.helpmenu)
        #       helpmenu.add_command(label="Preferências", command=About)
        self.helpmenu.add_command(
            label="Acerca de " + APP_NAME, command=about_window.AboutWindow)
        self.helpmenu.add_command(label="Suporte da aplicação " + APP_NAME, command=lambda: webbrowser.open(
            "http://victordomingos.com/contactos/", new=1, autoraise=True))
        self.helpmenu.add_command(
            label="Agradecimentos", command=about_window.ThanksWindow)
        self.helpmenu.add_separator()
        self.helpmenu.add_command(label="Visitar página do autor", command=lambda: webbrowser.open(
            "http://victordomingos.com", new=1, autoraise=True))
        #self.master.createcommand('::tk::mac::ShowPreferences', prefs_function)
        #self.master.bind('<<about-idle>>', about_dialog)
        #self.master.bind('<<open-config-dialog>>', config_dialog)
        self.master.createcommand('tkAboutDialog', about_window.AboutWindow)

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


    def logout_user(self, *event):
        restart_program()


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
            # self.master.unbind_all("<Command-n>")
        else:
            self.MenuFicheiro.entryconfigure("Nova reparação", state="active")
            # self.master.bind_all("<Command-n>")


    def _is_form_data_valid(self) -> bool:
        """ Verifica se todos os campos obrigatórios foram preenchidos e se os
            dados introduzidos estão corretos.
        """
        # validar aqui se dados estão corretos # TODO
        return True

        """
        if not self.ef_ltxt_nome.get().strip():
            msg = 'O campo "Nome" é de preenchimento obrigatório.'
            messagebox.showwarning(message=msg, parent=self)
            self.ef_ltxt_nome.entry.focus()
            return False
        
        elif not (self.ef_var_tipo_is_cliente.get()
                  or self.ef_var_tipo_is_fornecedor.get()):
            msg = 'Por favor, especifique qual a categoria (cliente/fornecedor) a atribuir a este contacto.'
            messagebox.showwarning(message=msg, parent=self)
            self.ef_chkbtn_tipo_cliente.entry.focus()
            return False
        else:
            return True
        """

    def on_save_repair(self, event=None):
        """ Recolhe todos os dados do formulário e guarda uma nova reparação """

        if not self._is_form_data_valid():
            return

        # Adaptar para o caso de ser uma reparação de stock #TODO
        # pesquisar se existe artigo criado; se não existir, criar

        if self.ef_ltxt_cod_artigo.get().strip:
            artigo = db.obter_artigo(self.ef_ltxt_cod_artigo.get())
        tipo = self.ef_var_tipo.get()
        if tipo == TIPO_REP_STOCK:
            dados_rep = {#'cliente_id',
                         'product_id': artigo['id'],
                         'sn': self.ef_ltxt_num_serie.get(),
                         'fornecedor_id': self.ef_txt_num_fornecedor,
                         'estado_artigo': self.ef_var_estado.get(),
                         'obs_estado': self.ef_ltxt_obs_estado_equipamento.get(),
                         'is_garantia': self.ef_var_garantia.get(),
                         #'data_compra': txt_para_data(self.ef_ltxt_data_compra.get()),
                         #'num_fatura': self.ef_ltxt_num_fatura.get(),
                         #'loja_compra': self.ef_ltxt_local_compra.get(),
                         'desc_servico': self.ef_text_descr_avaria_servico.get(1.0, tk.END),
                         'avaria_reprod_loja': self.ef_var_reprod_loja.get(),
                         'requer_copia_seg': self.ef_var_efetuar_copia.get(),
                         'is_find_my_ativo': self.ef_var_find_my.get(),
                         'senha': self.ef_ltxt_senha.get(),  # todo: scramble text
                         'acessorios_entregues': self.ef_ltxt_acessorios_entregues.get(),
                         'notas': self.ef_ltxt_notas.get(),
                         'local_reparacao_id': self.ef_var_local_intervencao.get(),
                         'estado_reparacao': EM_PROCESSAMENTO,
                         'fatura_fornecedor': self.ef_ltxt_num_fatura_fornecedor.get(),
                         'nar_autorizacao_rep': self.ef_ltxt_nar.get(),
                         'data_fatura_fornecedor': txt_para_data(self.ef_ltxt_data_fatura_fornecedor.get()),
                         'num_guia_rececao': self.ef_ltxt_num_guia_rececao.get(),
                         'data_guia_rececao': txt_para_data(self.ef_ltxt_data_entrada_stock.get()),
                         # 'cod_resultado_reparacao': SEM_INFORMACAO,
                         # 'descr_detalhe_reparacao': "",
                         # 'novo_sn_artigo': ,
                         # 'notas_entrega': ,
                         # 'utilizador_entrega_id': ,
                         # 'data_entrega': ,
                         # 'num_quebra_stock': ,
                         'is_stock': True,
                         #'modo_entrega': self.ef_var_modo_entrega.get(),  # TODO_converter para int?
                         #'reincidencia_processo_id': None,  # TODO
                         #'morada_entrega': self.ef_ltxt_morada_entrega.get(),
                         #'cliente_pagou_portes': self.ef_var_portes.get(),
                         'criado_por_utilizador_id': self.user_id,
                         }
        else:
            dados_rep = {'cliente_id': self.ef_txt_num_cliente.get(),
                         'product_id': artigo['id'],
                         'sn': self.ef_ltxt_num_serie.get(),
                         #'fornecedor_id': "",
                         'estado_artigo': self.ef_var_estado.get(),
                         'obs_estado': self.ef_ltxt_obs_estado_equipamento.get(),
                         'is_garantia': self.ef_var_garantia.get(),
                         'data_compra': txt_para_data(self.ef_ltxt_data_compra.get()),
                         'num_fatura': self.ef_ltxt_num_fatura.get(),
                         'loja_compra': self.ef_ltxt_local_compra.get(),
                         'descr_servico': self.ef_text_descr_avaria_servico.get(1.0, tk.END),
                         'avaria_reprod_loja': self.ef_var_reprod_loja.get(),
                         'requer_copia_seg': self.ef_var_efetuar_copia.get(),
                         'is_find_my_ativo': self.ef_var_find_my.get(),
                         'senha': self.ef_ltxt_senha.get(),  # todo: scramble text
                         'acessorios_entregues': self.ef_ltxt_acessorios_entregues.get(),
                         'notas': self.ef_ltxt_notas.get(),
                         'local_reparacao_id': self.ef_var_local_intervencao.get(),
                         'estado_reparacao': EM_PROCESSAMENTO,
                         #'fatura_fornecedor': self.ef_ltxt_num_fatura_fornecedor.get(),
                         'nar_autorizacao_rep': self.ef_ltxt_nar.get(),
                         #'data_fatura_fornecedor': txt_para_data(self.ef_ltxt_data_fatura_fornecedor.get()),
                         #'num_guia_rececao': self.ef_ltxt_num_guia_rececao.get(),
                         #'data_guia_rececao': txt_para_data(self.ef_ltxt_data_entrada_stock.get()),
                         # 'cod_resultado_reparacao': SEM_INFORMACAO,
                         # 'descr_detalhe_reparacao': "",
                         # 'novo_sn_artigo': ,
                         # 'notas_entrega': ,
                         # 'utilizador_entrega_id': ,
                         # 'data_entrega': ,
                         # 'num_quebra_stock': ,
                         'is_stock': False,
                         'modo_entrega': list(MODOS_ENTREGA.keys())[list(MODOS_ENTREGA.values()).index(self.ef_var_modo_entrega.get())],
                         'reincidencia_processo_id': None,  # TODO
                         'morada_entrega': self.ef_ltxt_morada_entrega.get(),
                         'cliente_pagou_portes': self.ef_var_portes.get(),
                         'criado_por_utilizador_id': db.get_user_id(self.username)
                         }

        self.ultima_reparacao = db.save_repair(dados_rep)

        # TODO - None se falhar
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
        wants_to_print = messagebox.askquestion(message='O processo de reparação foi guardado com sucesso. Deseja imprimir?',
                                                default='yes',
                                                parent=self)
        if wants_to_print == 'yes':
            imprimir.imprimir_folhas_de_reparacao(self.ultima_reparacao)

        self.master.focus()
        self.fechar_painel_entrada()
        self.reparacao_selecionada = self.ultima_reparacao
        self.create_window_detalhe_rep(num_reparacao=self.ultima_reparacao)


    # TODO
    def on_repair_cancel(self, event=None):
        # caso haja informação introduzida no formulário TODO: verificar
        # primeiro
        wants_to_cancel = messagebox.askyesno(message='Tem a certeza que deseja cancelar a introdução de dados? Toda a informação não guardada será eliminada de forma irreversível.',
                                              default='no',
                                              parent=self)
        if wants_to_cancel:
            self.fechar_painel_entrada()
            self.master.focus()
        else:
            self.entryframe.focus()

    def inserir_msg(self, msg_id=0, rep_num=0, utilizador="", data=None, texto="", msg_lida=True):
        """ Adicionar uma mensagem à lista, no painel de mensagens
        """
        str_data = f"{data.day}/{data.month}/{data.year} às {data.hour}:{int(data.minute):02}"
        texto = textwrap.fill(texto, width=45)
        texto_final = f"{utilizador}, {str_data}\n﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘﹘\n{texto}"
        ico = " ✉️" if msg_lida else " ✉️ ❗️"
        self.msgtree.insert("", "end", values=(ico, str(msg_id), str(rep_num), texto_final))


    def inserir_rep(self, rep_num=0, nome_cliente="", descr_artigo="", descr_servico="", estado=0, dias=0, tag="normal"):
        """ Adicionar uma reparação à lista, na tabela principal.
        """
        str_estado = ESTADOS[estado]
        self.tree.insert("", "end", values=(str(rep_num), nome_cliente,
            descr_artigo, descr_servico, str_estado, dias))


    def atualizar_lista_msgs(self):
        mensagens = db.obter_mensagens(self.user_id)

        for msg in mensagens:
            self.inserir_msg(msg_id=msg['evento_id'],
                rep_num=msg['repair_id'],
                utilizador=msg['remetente_nome'],
                data=msg['data'],
                texto=msg['texto'],
                msg_lida=msg['estado_msg'])

        self.atualizar_soma_msgs()
        self.alternar_cores(self.msgtree, inverso=False, fundo1='grey96')


    def atualizar_lista(self, reparacoes):
        """ Atualizar a lista de reparações na tabela principal.
        """
        for i in self.tree.get_children():  # Limpar tabela primeiro
            self.tree.delete(i)

        self.master.update()
        for reparacao in reparacoes:
            self.inserir_rep(rep_num=reparacao['id'],
                nome_cliente=reparacao['cliente_nome'],
                descr_artigo=reparacao['descr_artigo'],
                descr_servico=reparacao['descr_servico'],
                estado=reparacao['estado'],
                dias=reparacao['dias'],
                tag=reparacao['prioridade'])

        self.atualizar_soma_processos()
        self.alternar_cores(self.tree)
