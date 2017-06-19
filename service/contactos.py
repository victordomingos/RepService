#!/usr/bin/env python3.6
# encoding: utf-8
"""
Este módulo é parte integrante da aplicação RepService, desenvolvida por
Victor Domingos e distribuída sob os termos da licença Creative Commons
Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)
"""

import tkinter as tk
from tkinter import ttk
from extra_tk_classes import *
from base_app import *
from service import *
from detalhe_contacto import *
from db_operations import *
from string import ascii_uppercase


class ContactsWindow(baseApp):
    """ base class for application """
    def __init__(self, master, estado, *args, **kwargs):
        super().__init__(master,*args,**kwargs)
        self.estado = estado
        self.contacto_newDetailsWindow = {}
        self.contact_detail_windows_count = 0
        self.contacto_selecionado = None
        self.ultimo_contacto = None

        self.master.minsize(CONTACTOS_MIN_WIDTH, CONTACTOS_MIN_HEIGHT)
        self.master.maxsize(CONTACTOS_MAX_WIDTH, CONTACTOS_MAX_HEIGHT)
        self.master.geometry(CONTACTOS_GEOMETRIA)
        self.master.title("Contactos")

        self.montar_barra_de_ferramentas()
        self.montar_tabela()
        self.gerar_menu()

        #get status bar
        self.ncontactos = 2345
        self.my_statusbar.set(f"{self.ncontactos} contactos")

        self.gerar_painel_entrada()
        self.composeFrames()
        self.inserir_dados_de_exemplo()
        self.alternar_cores(self.tree)
        if self.estado.painel_novo_contacto_aberto:
            self.mostrar_painel_entrada()


    def gerar_menu(self):
        self.menu = tk.Menu(self.master)
        #----------------Menu contextual tabela principal---------------------
        self.contextMenu = tk.Menu(self.menu)
        self.contextMenu.add_command(label="Informações", command=lambda: self.create_window_detalhe_contacto(num_contacto=self.contacto_selecionado))
        #self.contextMenu.add_command(label="Abrir no site da transportadora", command=self.abrir_url_browser)
        self.contextMenu.add_separator()
        #self.contextMenu.add_command(label="Copiar número de objeto", command=self.copiar_obj_num)
        #self.contextMenu.add_command(label="Copiar mensagem de expedição", command=self.copiar_msg)
        #self.contextMenu.add_separator()
        #self.contextMenu.add_command(label="Arquivar/restaurar remessa", command=self.del_remessa)
        #self.contextMenu.add_separator()
        #self.contextMenu.add_command(label="Registar cheque recebido", command=self.pag_recebido)
        #self.contextMenu.add_command(label="Registar cheque depositado", command=self.chq_depositado)


    def montar_tabela(self):
        self.tree = ttk.Treeview(self.leftframe, height=60, selectmode='browse')
        self.tree['columns'] = ('ID', 'Nome', 'Telefone','Email')
        self.tree.pack(side=tk.TOP, fill=tk.BOTH)
        self.tree.column('#0', anchor=tk.W, minwidth=0, stretch=0, width=0)
        self.tree.column('ID', anchor=tk.E, minwidth=37, stretch=0, width=37)
        self.tree.column('Nome', minwidth=140, stretch=1, width=140)
        self.tree.column('Telefone', anchor=tk.E, minwidth=90, stretch=1, width=90)
        self.tree.column('Email', anchor=tk.E, minwidth=130, stretch=1, width=130)

        self.configurarTree()

        self.leftframe.grid_columnconfigure(0, weight=1)
        self.leftframe.grid_rowconfigure(0, weight=1)
        self.bind_tree()


    def montar_barra_de_ferramentas(self):
        self.btn_clientes = ttk.Button(self.topframe, style="secondary.TButton", text="Clientes", command=None)
        self.btn_clientes.grid(column=0, row=0)
        self.dicas.bind(self.btn_clientes, 'Mostrar apenas clientes.')

        self.btn_fornecedores = ttk.Button(self.topframe, style="secondary.TButton", text="Fornecedores", command=None)
        self.btn_fornecedores.grid(column=1, row=0)
        self.dicas.bind(self.btn_fornecedores, 'Mostrar apenas fornecedores\ne centros técnicos.')

        self.btn_add = ttk.Button(self.topframe, text=" ➕", width=3, command=self.show_entryform)
        self.btn_add.grid(column=3, row=0)
        self.dicas.bind(self.btn_add, 'Criar novo contacto.')

        self.text_input_pesquisa = ttk.Entry(self.topframe, width=12)
        self.text_input_pesquisa.grid(column=4, row=0)
        self.dicas.bind(self.text_input_pesquisa, 'Para iniciar a pesquisa, digite\numa palavra ou frase. (⌘F)')

        #letras_etc = ascii_letters + "01234567890-., "
        #for char in letras_etc:
        #    keystr = '<KeyRelease-' + char + '>'
        #    self.text_input_pesquisa.bind(keystr, self.ativar_pesquisa)
        #self.text_input_pesquisa.bind('<Button-1>', self.clique_a_pesquisar)
        #self.text_input_pesquisa.bind('<KeyRelease-Escape>', self.cancelar_pesquisa)
        #self.text_input_pesquisa.bind('<KeyRelease-Mod2-a>', self.text_input_pesquisa.select_range(0, END))

        for col in range(1,4):
            self.topframe.columnconfigure(col, weight=0)
        self.topframe.columnconfigure(2, weight=1)


    def mostrar_painel_entrada(self, *event):
        self.estado.painel_novo_contacto_aberto = True
        #self.MenuFicheiro.entryconfig("Novo contacto", state="disabled")
        #root.unbind_all("<Command-t>")
        self.show_entryform()
        self.ef_ltxt_nome.entry.focus()


    def fechar_painel_entrada(self, *event):
        self.estado.painel_novo_contacto_aberto = False
        self.clear_text()
        self.hide_entryform()
        #root.bind_all("<Command-n>")

    def clear_text(self):
        self.entryframe.focus()
        self.ef_var_tipo_is_cliente.set(True)
        self.ef_var_tipo_is_fornecedor.set(False)
        self.ef_var_tipo_is_loja.set(False)
        self.ef_combo_pais.current(178)

        widgets = (self.ef_ltxt_nome,
                   self.ef_ltxt_empresa,
                   self.ef_ltxt_nif,
                   self.ef_ltxt_telefone,
                   self.ef_ltxt_tlm,
                   self.ef_ltxt_tel_empresa,
                   self.ef_ltxt_email,
                   self.ef_lstxt_morada,
                   self.ef_ltxt_cod_postal,
                   self.ef_ltxt_localidade,
                   self.ef_lstxt_notas)
        for widget in widgets:
            widget.clear()


    def gerar_painel_entrada(self):

        #entryfr1-----------------------------
        #TODO:adicionar campos, notebook, etc
        #criar funções para usar esses campos, ora para adicionar, ora para editar, ora para visualizar registos

        self.ef_var_tipo_is_cliente = tk.IntVar()
        self.ef_var_tipo_is_cliente.set(True)
        self.ef_var_tipo_is_fornecedor = tk.IntVar()
        if self.estado.tipo_novo_contacto == "Fornecedor":
            self.ef_var_tipo_is_fornecedor.set(True)
            self.ef_var_tipo_is_cliente.set(False)
        self.ef_var_tipo_is_loja = tk.IntVar()

        self.ef_cabecalho = ttk.Frame(self.entryfr1, padding=4)
        self.ef_lbl_titulo = ttk.Label(self.ef_cabecalho, style="Panel_Title.TLabel", text="Adicionar Contacto:\n")
        self.ef_lbl_tipo = ttk.Label(self.ef_cabecalho, text="Tipo:", style="Panel_Body.TLabel")

        self.ef_chkbtn_tipo_cliente = ttk.Checkbutton(self.ef_cabecalho, text="Cliente", style="Panel_Body.Checkbutton", variable=self.ef_var_tipo_is_cliente)
        self.ef_chkbtn_tipo_fornecedor = ttk.Checkbutton(self.ef_cabecalho, text="Fornecedor ou centro técnico", style="Panel_Body.Checkbutton", variable=self.ef_var_tipo_is_fornecedor)
        self.ef_chkbtn_tipo_loja = ttk.Checkbutton(self.ef_cabecalho, text="Loja do nosso grupo", style="Panel_Body.Checkbutton", variable=self.ef_var_tipo_is_loja)

        self.btn_adicionar = ttk.Button(self.ef_cabecalho, default="active",  style="Active.TButton", text="Adicionar", command=self.on_save_contact)
        self.btn_cancelar = ttk.Button(self.ef_cabecalho, text="Cancelar", command=self.on_contact_cancel)


        self.ef_lbl_titulo.grid(column=0, row=0, columnspan=3, sticky='w')
        self.ef_lbl_tipo.grid(column=0, row=1, sticky='e')
        self.ef_chkbtn_tipo_cliente.grid(column=1, row=1, sticky='w')
        self.ef_chkbtn_tipo_fornecedor.grid(column=1, row=2, sticky='w')
        self.ef_chkbtn_tipo_loja.grid(column=1, row=3, sticky='w')

        self.btn_adicionar.grid(column=3, row=1, sticky='we')
        self.btn_cancelar.grid(column=3, row=2, sticky='we')

        self.ef_cabecalho.grid(column=0,row=0, sticky='we')
        self.entryfr1.columnconfigure(0, weight=1)
        self.ef_cabecalho.columnconfigure(2, weight=1)

        #self.btn_adicionar.bind('<Button-1>', self.add_remessa)


        #entryfr2-----------------------------
        self.ef_lf_top = ttk.Labelframe(self.entryfr2, padding=4, text="")
        self.ef_ltxt_nome = LabelEntry(self.ef_lf_top, "Nome", style="Panel_Body.TLabel")
        self.ef_ltxt_empresa = LabelEntry(self.ef_lf_top, "Empresa", style="Panel_Body.TLabel")
        self.ef_ltxt_nif = LabelEntry(self.ef_lf_top, "NIF", style="Panel_Body.TLabel")
        self.ef_ltxt_telefone = LabelEntry(self.ef_lf_top, "\nTel.", width=14, style="Panel_Body.TLabel")
        self.ef_ltxt_tlm = LabelEntry(self.ef_lf_top, "\nTlm.", width=14, style="Panel_Body.TLabel")
        self.ef_ltxt_tel_empresa = LabelEntry(self.ef_lf_top, "\nTel. empresa", width=14, style="Panel_Body.TLabel")

        self.ef_ltxt_email = LabelEntry(self.ef_lf_top, "Email", style="Panel_Body.TLabel")
        self.ef_lstxt_morada = LabelText(self.ef_lf_top, "\nMorada", height=2, style="Panel_Body.TLabel")

        self.ef_ltxt_cod_postal = LabelEntry(self.ef_lf_top, "Código Postal", style="Panel_Body.TLabel")
        self.ef_ltxt_localidade = LabelEntry(self.ef_lf_top, "Localidade", style="Panel_Body.TLabel")

        self.ef_lbl_pais = ttk.Label(self.ef_lf_top, text="País", style="Panel_Body.TLabel")
        self.paises_value = tk.StringVar()
        self.ef_combo_pais = ttk.Combobox(self.ef_lf_top, values=TODOS_OS_PAISES,
                                          textvariable=self.paises_value, 
                                          state='readonly')
        self.ef_combo_pais.current(178)
        self.ef_combo_pais.bind("<Key>", self.procurar_em_combobox)

        self.ef_lstxt_notas = LabelText(self.ef_lf_top, "\nNotas:", height=3, style="Panel_Body.TLabel")

        self.ef_ltxt_nome.grid(column=0, row=0, columnspan=3, padx=5, sticky='we')
        self.ef_ltxt_empresa.grid(column=0, row=1, columnspan=2, padx=5, sticky='we')
        self.ef_ltxt_nif.grid(column=2, row=1, padx=5, sticky='we')

        self.ef_ltxt_telefone.grid(column=0, row=2, padx=5, sticky='we')
        self.ef_ltxt_tlm.grid(column=1, row=2, padx=5, sticky='we')
        self.ef_ltxt_tel_empresa.grid(column=2, row=2, padx=5, sticky='we')
        self.ef_ltxt_email.grid(column=0, row=3, columnspan=3, padx=5, sticky='we')
        self.ef_lstxt_morada.grid(column=0, row=4, columnspan=3, rowspan=2, padx=5, sticky='we')

        self.ef_ltxt_cod_postal.grid(column=0, row=6, padx=5, sticky='we')
        self.ef_ltxt_localidade.grid(column=1, row=6, columnspan=2, padx=5, sticky='we')

        self.ef_lbl_pais.grid(column=0, columnspan=3, row=7, padx=5, sticky='we')
        self.ef_combo_pais.grid(column=0, columnspan=3, row=8, padx=5, sticky='we')
        self.ef_lstxt_notas.grid(column=0, row=9, columnspan=3, rowspan=4, padx=5, sticky='we')

        self.ef_lf_top.grid(column=0,row=0, sticky='we')
        self.ef_lf_top.columnconfigure(0, weight=1)
        self.ef_lf_top.columnconfigure(1, weight=1)
        self.ef_lf_top.columnconfigure(2, weight=1)
        self.entryfr2.columnconfigure(0, weight=1)


        #--- acabaram os 'entryfr', apenas código geral para o entryframe a partir daqui ---
        self.entryframe.bind_all("<Command-Escape>", self.fechar_painel_entrada)

    def procurar_em_combobox(self, event):
        """
        Saltar para o primeiro país da lista (combobox) começado pela letra
        correspondente à tecla pressionada.
        """
        tecla_pressionada = event.char.upper()
        if tecla_pressionada in ascii_uppercase:
            for index, pais in enumerate(TODOS_OS_PAISES):
                if pais[0] == tecla_pressionada:
                    self.ef_combo_pais.current(index)
                    break


    def adicionar_contacto(self, *event):
        """
        Guarda o contacto acabado de criar. Caso o utilizador esteja a criar uma
        reparação, adiciona o contacto ao campo correspondente.
        """
        # guardar na base de dados e obter o nº do último contacto adicionado
        
        if self.estado.tipo_novo_contacto == "Cliente":
            print("Usar este cliente")
            self.estado.contacto_para_nova_reparacao = "123"
            self.estado.janela_principal.close_window_contactos()
            pass  # preencher o campo do nº de cliente com o último contacto de cliente criado; depois atribuir foco ao formulário da reparação e fechar a janela
        elif self.estado.tipo_novo_contacto == "Fornecedor":
            print("Usar este fornecedor")
            self.estado.janela_principal.close_window_contactos()
            pass  # preencher o campo do nº de fornecedor com o último contacto de fornecedor criado; depois atribuir foco ao formulário da reparação e fechar a janela
        else:
            print("guardar e nao fazer mais nada")
            pass  # atualizar a lista de contactos nesta janela fechar o formulário



    def bind_tree(self):
        self.tree.bind('<<TreeviewSelect>>', self.selectItem_popup)
        self.tree.bind('<Double-1>', lambda x: self.create_window_detalhe_contacto(num_contacto=self.contacto_selecionado))
        self.tree.bind("<Button-2>", self.popupMenu)
        self.tree.bind("<Button-3>", self.popupMenu)


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
        Obter contacto selecionado (após clique de rato na linha correspondente)
        """
        curItem = self.tree.focus()
        tree_linha = self.tree.item(curItem)

        contacto = tree_linha["values"][0]
        nome =  tree_linha["values"][1]
        self.my_statusbar.set(f"{contacto} • {nome}")
        self.contacto_selecionado = contacto


    def create_window_detalhe_contacto(self, *event, num_contacto=None):
        self.contact_detail_windows_count += 1
        self.contacto_newDetailsWindow[self.contact_detail_windows_count] = tk.Toplevel()
        self.contacto_newDetailsWindow[self.contact_detail_windows_count].title(f'Detalhe de contacto: {num_contacto}')
        self.janela_detalhes_contacto = contactDetailWindow(self.contacto_newDetailsWindow[self.contact_detail_windows_count], num_contacto)
        self.contacto_newDetailsWindow[self.contact_detail_windows_count].focus()


    def liga_desliga_menu_novo(self, *event):
        """
        Liga e desliga menus com base na configuração atual da janela. Por exemplo, ao
        abrir o painel de entrada de dados, desativa o menu "nova reparação", para evitar
        que o painel se feche inadvertidamente.
        """
        if self.is_entryform_visible:
            self.MenuFicheiro.entryconfigure("Novo contacto", state="disabled")
            # TODO - corrigir bug: o atalho de teclado só fica realmente inativo depois de acedermos ao menu ficheiro. Porquê??
            #root.unbind_all("<Command-Option-n>")
        else:
            self.MenuFicheiro.entryconfigure("Novo contacto", state="active")
            #root.bind_all("<Command-Option-n>")


    def on_save_contact(self, event=None):
            # reparacao = recolher todos os dados do formulário  #TODO
            contacto = "teste"
            self.ultimo_contacto = save_contact(contacto) #TODO - None se falhar
            if self.ultimo_contacto:
                self.on_contact_save_success()
            else:
                wants_to_try_again_save = messagebox.askquestion(message='Não foi possível guardar este contacto na base de dados. Deseja tentar novamente?', 
                                                                 default='yes',
                                                                 parent=self)  
                if wants_to_try_again_save == 'yes':
                    self.on_save_contact()
                else:
                    self.on_contact_cancel()
                            

    def on_contact_save_success(self):
        print("Contacto guardado com sucesso")
        self.fechar_painel_entrada()
        self.adicionar_contacto()
        """
        self.ultimo_contacto = "1234" #TODO - criar um mecanismo para obter o número da reparação acabada de introduzir na base de dados
        wants_to_create = messagebox.askquestion(message='O novo contacto foi guardado com sucesso. Deseja criar uma nova reparação?', default='yes', parent=self)  
        if wants_to_create == 'yes':
                imprimir_folhas_de_reparacao(self.ultima_reparacao)
                self.fechar_painel_entrada()
        else:
                self.entryframe.focus()
        """

    # TODO
    def on_contact_cancel(self, event=None):
        # caso haja informação introduzida no formulário TODO: verificar primeiro
        wants_to_cancel = messagebox.askyesno(message='Tem a certeza que deseja cancelar a introdução de dados? Toda a informação não guardada será eliminada de forma irreversível.', 
                                                                                    default='no',
                                                                                    parent=self)
        if wants_to_cancel:
            self.fechar_painel_entrada()
        else:
            self.entryframe.focus()



    def inserir_dados_de_exemplo(self):
        for i in range(100):
            self.tree.insert("", "end", text="", values=(str(i),"Nome do cliente", "+351000000000", "endereco@emaildocliente.com"))
