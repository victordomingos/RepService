#!/usr/bin/env python3.6
# encoding: utf-8
"""
Este módulo é parte integrante da aplicação RepService, desenvolvida por
Victor Domingos e distribuída sob os termos da licença Creative Commons
Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)
"""
from tkinter import ttk, messagebox
import Pmw
from string import ascii_uppercase

from pyisemail import is_email

from gui.extra_tk_classes import AutoScrollbar, LabelEntry, LabelText
from gui import detalhe_reparacao
from global_setup import *
from misc.constants import TODOS_OS_PAISES, TIPO_REP_STOCK, TIPO_REP_CLIENTE, RESULTADOS
from misc.misc_funcs import check_and_normalize_phone_number, validate_phone_entry

if USE_LOCAL_DATABASE:
    from local_db import db_main as db
else:
    from remote_db import db_main as db


class contactDetailWindow(ttk.Frame):
    """ Classe de base para a janela de detalhes de reparações """

    def __init__(self, master, num_contacto, estado_app, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master = master
        self.estado_app = estado_app
        self.main_statusbar = estado_app.janela_principal.my_statusbar
        self.main_statusbar.show_progress(value=50, mode="determinate")
        self.master.bind("<Command-w>", self.on_btn_fechar)
        self.master.focus()
        self.num_contacto = num_contacto
        self.contacto = db.obter_contacto(num_contacto)
        self.reparacoes = db.obter_reparacoes_por_contacto(num_contacto)

        self.main_statusbar.hide_progress(last_update=100)
        self.contacto_selecionado = ""
        self.rep_newDetailsWindow = {}
        self.rep_detail_windows_count = 0
        self.contacto_newDetailsWindow = {}
        self.contact_detail_windows_count = 0
        self.soma_reparacoes = 0
        self.soma_reincidencias = 0
        self.new_contact_telefone = ""
        self.new_contact_telemovel = ""
        self.new_contact_tel_emp = ""

        self.var_tipo_is_cliente = tk.IntVar()
        self.var_tipo_is_fornecedor = tk.IntVar()
        #self.var_tipo_is_loja = tk.IntVar()

        self.configurar_frames_e_estilos()
        self.montar_barra_de_ferramentas()

        self.gerar_painel_principal()
        if self.var_tipo_is_cliente.get():
            self.atualizar_soma()
            self.alternar_cores(self.tree)

        self.mostrar_painel_principal()
        self.montar_rodape()
        self.composeFrames()


    def _on_criar_nova_reparacao(self, *event):
        """ Cria uma nova reparação utilizando o contacto atual.
        """
        if self.contacto['is_cliente']:
            self.estado_app.contacto_para_nova_reparacao = self.num_contacto
            self.estado_app.tipo_novo_contacto = "Cliente"
            self.estado_app.janela_principal.ef_var_tipo.set(TIPO_REP_CLIENTE)
        elif self.contacto['is_fornecedor']:
            self.estado_app.contacto_para_nova_reparacao = self.num_contacto
            self.estado_app.tipo_novo_contacto = "Fornecedor"
            self.estado_app.janela_principal.ef_var_tipo.set(TIPO_REP_STOCK)

        self.estado_app.janela_principal.mostrar_painel_entrada()
        self.estado_app.janela_principal.radio_tipo_command()


    def montar_barra_de_ferramentas(self):
        self.lbl_titulo = ttk.Label(self.topframe, style="Panel_Title.TLabel",
                                    foreground=self.btnTxtColor, text=f"Contacto nº {self.num_contacto}")

        # ----------- Botão com menu "Copiar" --------------
        self.mbtn_copiar = ttk.Menubutton(self.topframe, text=" ⚡")
        self.mbtn_copiar.menu = tk.Menu(self.mbtn_copiar, tearoff=0)
        self.mbtn_copiar["menu"] = self.mbtn_copiar.menu
        self.mbtn_copiar.menu.add_command(label="Nome", command=None)
        self.mbtn_copiar.menu.add_command(label="NIF", command=None)
        self.mbtn_copiar.menu.add_command(label="Morada", command=None)
        self.mbtn_copiar.menu.add_command(label="Código Postal", command=None)
        self.mbtn_copiar.menu.add_command(label="Localidade", command=None)
        self.mbtn_copiar.menu.add_command(label="Email", command=None)
        self.mbtn_copiar.menu.add_command(label="Telefone", command=None)
        self.dicas.bind(
            self.mbtn_copiar, 'Clique para selecionar e copiar\ndados referentes a este contacto\npara a Área de Transferência.')
        # ----------- fim de Botão com menu "Copiar" -------------

        self.btn_nova_rep = ttk.Button(
            self.topframe, text="Criar reparação", style="secondary.TButton", command=self._on_criar_nova_reparacao)
        self.dicas.bind(self.btn_nova_rep, 'Criar um novo processo de reparação.')

        self.btn_guardar_alteracoes = ttk.Button(
            self.topframe, text="Guardar", style="secondary.TButton",
            command=self._on_update_contact)
        self.dicas.bind(self.btn_guardar_alteracoes,
                        'Clique para guardar quaisquer alterações\nefetuadas a esta ficha de contacto.')

        self.lbl_titulo.grid(column=0, row=0, rowspan=2)
        self.mbtn_copiar.grid(column=7, row=0)
        self.btn_nova_rep.grid(column=8, row=0)
        self.btn_guardar_alteracoes.grid(column=9, row=0)

        self.topframe.grid_columnconfigure(2, weight=1)

    def gerar_painel_principal(self):
        # Preparar o notebook da secção principal ------------------------
        self.note = ttk.Notebook(self.centerframe, padding="3 20 3 3")
        self.note.bind_all("<<NotebookTabChanged>>", self._on_tab_changed)

        self.tab_geral = ttk.Frame(self.note, padding=10)
        self.tab_notas = ttk.Frame(self.note, padding=10)
        self.note.add(self.tab_geral, text="Contactos")
        self.note.add(self.tab_notas, text="Informação Adicional")
        self.gerar_tab_geral()
        self.montar_tab_geral()
        self.gerar_tab_notas()
        self.montar_tab_notas()

        if self.var_tipo_is_cliente.get():
            self.tab_reparacoes = ttk.Frame(self.note, padding=0)
            self.note.add(self.tab_reparacoes, text="Reparações")
            self.gerar_tab_reparacoes()
            self.montar_tab_reparacoes()


    def _on_tab_changed(self, event):
        w = event.widget  # get the current widget
        w.update_idletasks()
        # get the tab widget where we're going to
        tab = w.nametowidget(w.select())
        # get the tab widget where we're going to
        tab_name = self.note.tab(self.note.select(), "text")
        if tab_name == "Reparações":
            w.update_idletasks()
            self.master.state("zoomed")
            self.master.minsize(820, W_DETALHE_CONTACTO_MIN_HEIGHT)
        elif tab_name == "Informação Adicional":
            self.master.minsize(W_DETALHE_CONTACTO_MIN_WIDTH, 360)
            w.update_idletasks()
            self.master.state("normal")
            w.configure(height=tab.winfo_reqheight(),
                        width=tab.winfo_reqwidth())
        else:
            self.master.minsize(W_DETALHE_CONTACTO_MIN_WIDTH,
                                W_DETALHE_CONTACTO_MIN_HEIGHT)
            w.update_idletasks()
            self.master.state("normal")
            w.configure(height=tab.winfo_reqheight(),
                        width=tab.winfo_reqwidth())

    def gerar_tab_geral(self):
        # TAB Geral ~~~~~~~~~~~~~~~~
        self.geral_fr1 = ttk.Frame(self.tab_geral)
        self.morada_fr1 = ttk.Frame(self.tab_geral)

        #self.geral_fr2 = ttk.Frame(self.tab_geral)

        # Criar widgets para este separador -----------------------------------
        #self.txt_numero_contacto = ttk.Entry(self.geral_fr1, font=("Helvetica-Neue", 12), width=5)
        #self.txt_nome = ttk.Entry(self.geral_fr1, font=("Helvetica-Neue", 12), width=35)

        # entryfr2-----------------------------
        self.ef_ltxt_nome = LabelEntry(
            self.geral_fr1, "Nome", style="Panel_Body.TLabel")
        self.ef_ltxt_empresa = LabelEntry(
            self.geral_fr1, "Empresa", style="Panel_Body.TLabel")
        self.ef_ltxt_nif = LabelEntry(
            self.geral_fr1, "NIF", style="Panel_Body.TLabel")
        self.ef_ltxt_nif.bind("<FocusOut>", self.validar_nif)
        self.ef_ltxt_telefone = LabelEntry(
            self.geral_fr1, "\nTel.", width=14, style="Panel_Body.TLabel")
        self.ef_ltxt_tlm = LabelEntry(
            self.geral_fr1, "\nTlm.", width=14, style="Panel_Body.TLabel")
        self.ef_ltxt_tel_empresa = LabelEntry(
            self.geral_fr1, "\nTel. empresa", width=14, style="Panel_Body.TLabel")

        self.ef_ltxt_email = LabelEntry(
            self.geral_fr1, "Email", style="Panel_Body.TLabel")

        self.ef_lstxt_morada = LabelText(
            self.morada_fr1, "\n\nMorada", height=2, style="Panel_Body.TLabel")

        self.ef_ltxt_cod_postal = LabelEntry(
            self.morada_fr1, "Código Postal", style="Panel_Body.TLabel", width=10)
        self.ef_ltxt_localidade = LabelEntry(
            self.morada_fr1, "Localidade", style="Panel_Body.TLabel", width=35)

        self.ef_lbl_pais = ttk.Label(
            self.morada_fr1, text="País", style="Panel_Body.TLabel")
        self.paises_value = tk.StringVar()
        self.ef_combo_pais = ttk.Combobox(self.morada_fr1, values=TODOS_OS_PAISES,
                                          textvariable=self.paises_value,
                                          state='readonly')

        self.ef_combo_pais.bind("<Key>", self.procurar_em_combobox)

        # Preencher com dados da base de dados --------------------------------
        self.ef_ltxt_nome.set(self.contacto['nome'])
        self.ef_ltxt_empresa.set(self.contacto['empresa'])
        self.ef_ltxt_nif.set(self.contacto['nif'])
        self.ef_ltxt_telefone.set(self.contacto['telefone'])
        self.ef_ltxt_tlm.set(self.contacto['telemovel'])
        self.ef_ltxt_tel_empresa.set(self.contacto['telefone_empresa'])

        self.ef_ltxt_telefone.entry.bind("<FocusOut>", self._on_tel_exit)
        self.ef_ltxt_tlm.entry.bind("<FocusOut>", self._on_tel_exit)
        self.ef_ltxt_tel_empresa.entry.bind("<FocusOut>", self._on_tel_exit)
        self._validar_telefones()

        self.ef_ltxt_email.set(self.contacto['email'])
        self.ef_lstxt_morada.set(self.contacto['morada'])
        self.ef_ltxt_cod_postal.set(self.contacto['cod_postal'])
        self.ef_ltxt_localidade.set(self.contacto['localidade'])

        for index, pais in enumerate(TODOS_OS_PAISES):
            if pais == self.contacto['pais']:
                self.ef_combo_pais.current(index)
                break


    def montar_tab_geral(self):
        # Montar todos os campos na grid --------------------------------------
        self.ef_ltxt_nome.grid(
            column=0, row=0, columnspan=3, padx=5, sticky='we')
        self.ef_ltxt_empresa.grid(
            column=0, row=1, columnspan=2, padx=5, sticky='we')
        self.ef_ltxt_nif.grid(column=2, row=1, padx=5, sticky='we')

        self.ef_ltxt_telefone.grid(column=0, row=2, padx=5, sticky='we')
        self.ef_ltxt_tlm.grid(column=1, row=2, padx=5, sticky='we')
        self.ef_ltxt_tel_empresa.grid(column=2, row=2, padx=5, sticky='we')
        self.ef_ltxt_email.grid(
            column=0, row=3, columnspan=3, padx=5, sticky='we')

        self.geral_fr1.grid_columnconfigure(0, weight=1)
        self.geral_fr1.grid_columnconfigure(1, weight=1)
        self.geral_fr1.grid_columnconfigure(2, weight=1)

        self.geral_fr1.pack(side='top', expand=False, fill='x')
        #ttk.Separator(self.tab_geral).pack(side='top', expand=False, fill='x', pady=10)
        #self.geral_fr2.pack(side='top', expand=True, fill='both')

        self.ef_lstxt_morada.grid(
            column=0, row=4, columnspan=3, rowspan=2, padx=5, sticky='we')

        self.ef_ltxt_cod_postal.grid(column=0, row=6, padx=5, sticky='we')
        self.ef_ltxt_localidade.grid(
            column=1, row=6, columnspan=2, padx=5, sticky='we')

        self.ef_lbl_pais.grid(column=0, columnspan=3,
                              row=7, padx=5, sticky='we')
        self.ef_combo_pais.grid(column=0, columnspan=3,
                                row=8, padx=5, sticky='we')

        self.morada_fr1.grid_columnconfigure(0, weight=1)
        self.morada_fr1.grid_columnconfigure(1, weight=1)
        self.morada_fr1.grid_columnconfigure(2, weight=1)

        self.morada_fr1.pack(side='top', expand=False, fill='x')

    def gerar_tab_notas(self):
        self.notas_fr1 = ttk.Frame(self.tab_notas)
        #self.notas_fr2 = ttk.Frame(self.tab_notas)
        self.ef_cabecalho = ttk.Frame(self.notas_fr1, padding=4)
        self.ef_lbl_tipo = ttk.Label(
            self.ef_cabecalho, text="Tipo:", style="Panel_Body.TLabel")
        self.ef_chkbtn_tipo_cliente = ttk.Checkbutton(
            self.ef_cabecalho, text="Cliente", variable=self.var_tipo_is_cliente)
        self.ef_chkbtn_tipo_fornecedor = ttk.Checkbutton(
            self.ef_cabecalho, text="Fornecedor ou centro técnico", variable=self.var_tipo_is_fornecedor)
        #self.ef_chkbtn_tipo_loja = ttk.Checkbutton(self.ef_cabecalho, text="Loja do nosso grupo", style="Panel_Body.Checkbutton", variable=self.var_tipo_is_loja)

        self.ef_lstxt_notas = LabelText(
            self.notas_fr1, "\nNotas:", height=3, style="Panel_Body.TLabel")


        self.var_tipo_is_cliente.set(self.contacto['is_cliente'])
        self.var_tipo_is_fornecedor.set(self.contacto['is_fornecedor'])
        # self.var_tipo_is_loja.set(False)
        self.ef_lstxt_notas.set(self.contacto['notas'])


    def montar_tab_notas(self):
        self.ef_lstxt_notas.grid(
            column=0, row=9, columnspan=3, rowspan=4, padx=5, sticky='wens')
        self.ef_cabecalho.columnconfigure(2, weight=1)
        #self.notas_fr1.columnconfigure(0, weight=1)

        self.ef_lbl_tipo.grid(column=0, row=1, sticky='e')
        self.ef_chkbtn_tipo_cliente.grid(column=1, row=1, sticky='w')
        self.ef_chkbtn_tipo_fornecedor.grid(column=1, row=2, sticky='w')
        #self.ef_chkbtn_tipo_loja.grid(column=1, row=3, sticky='w')

        self.ef_cabecalho.grid(column=0, row=0, sticky='we')

        self.notas_fr1.columnconfigure(0, weight=1)
        self.notas_fr1.rowconfigure(10, weight=1)

        self.notas_fr1.pack(side='top', expand=True, fill='both')
        #ttk.Separator(self.tab_notas).pack(side='top', expand=False, fill='x', pady=10)
        #self.notas_fr2.pack(side='top', expand=True, fill='both')

    def gerar_tab_reparacoes(self):  # TODO
        self.reparacoes_fr1 = ttk.Frame(self.tab_reparacoes)
        self.treeframe = ttk.Frame(self.reparacoes_fr1, padding="0 0 0 0")

        self.tree = ttk.Treeview(
            self.treeframe, height=1, selectmode='browse', style="Reparacoes_Remessa.Treeview")
        self.tree['columns'] = (
            'Nº', 'Data', 'Equipamento', 'Serviço', 'Resultado', 'Reincid.')
        self.tree.column('#0', anchor='w', minwidth=0, stretch=0, width=0)
        self.tree.column('Nº', anchor='ne', minwidth=50, stretch=0, width=50)
        self.tree.column('Data', anchor='nw', minwidth=80, stretch=0, width=80)
        self.tree.column('Equipamento', anchor='nw',
                         minwidth=200, stretch=1, width=200)
        self.tree.column('Serviço', anchor='nw',
                         minwidth=200, stretch=1, width=200)
        self.tree.column('Resultado', anchor='nw',
                         minwidth=180, stretch=1, width=180)
        self.tree.column('Reincid.', anchor='nw',
                         minwidth=50, stretch=0, width=50)

        for col in self.tree['columns']:
            self.tree.heading(col, text=col.title(),
                              command=lambda c=col: self.sortBy(self.tree, c, 0))

        # Barra de deslocação para a tabela
        self.tree.grid(column=0, row=0, sticky="nsew", in_=self.treeframe)
        self.vsb = AutoScrollbar(
            self.treeframe, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.vsb.set)
        self.vsb.grid(column=1, row=0, sticky="ns", in_=self.treeframe)

        for rep in self.reparacoes:
            self.tree.insert("", "end", values=(str(rep['id']),
                                                rep['data'],
                                                rep['descr_artigo'],
                                                rep['descr_servico'],
                                                RESULTADOS[rep['resultado']],
                                                rep['reincidencia_id']))

        self.bind_tree()
        self.alternar_cores(self.tree)

        self.lbl_soma_processos = ttk.Label(
            self.reparacoes_fr1, text=f"Nº de processos deste contacto: {self.soma_reparacoes} ({self.soma_reincidencias} reincidências)", style="Panel_Body.TLabel")

    def montar_tab_reparacoes(self):
        self.reparacoes_fr1.pack(side='top', expand=True, fill='both')
        self.treeframe.grid(column=0, row=0, sticky="nsew")
        self.treeframe.grid_columnconfigure(0, weight=1)
        self.treeframe.grid_rowconfigure(0, weight=1)

        self.lbl_soma_processos.grid(
            column=0, row=2, sticky='ne', pady="5 10", padx=3)

        self.reparacoes_fr1.grid_columnconfigure(0, weight=1)
        self.reparacoes_fr1.grid_rowconfigure(0, weight=1)
        self.atualizar_soma()

    def validar_nif(self, *event):
        """ Verifica se já existe na base de dados um contacto criado com o NIF
            indicado. Se existir, propor abrir a janela de detalhes. Se não
            existir, continuar a criar o novo contacto.
        """

        nif = self.ef_ltxt_nif.get().strip()
        if nif:
            contacto = db.contact_exists(nif)
        else:
            contacto = None

        if contacto:
            msg = f"Já existe na base de dados um outro contacto com o NIF indicado ({contacto['id']} " \
                  f"- {contacto['nome']}). Pretende verificar o contacto existente?"
            verificar = messagebox.askquestion(message=msg, default='yes', parent=self)
            if verificar == 'yes':
                self.create_window_detalhe_contacto(num_contacto=contacto['id'])

    def _on_tel_exit(self, event):
        validate_phone_entry(self, event.widget)


    def _validar_telefones(self, *event) -> bool:
            self.new_contact_telemovel = ""
            self.new_contact_telefone = ""
            self.new_contact_tel_emp = ""

            try:
                self.new_contact_telefone = check_and_normalize_phone_number(self.ef_ltxt_telefone.get()).replace(" ","")
            except Exception as e:
                pass

            try:
                self.new_contact_telemovel = check_and_normalize_phone_number(self.ef_ltxt_tlm.get()).replace(" ", "")
            except Exception as e:
                pass

            try:
                self.new_contact_tel_emp = check_and_normalize_phone_number(self.ef_ltxt_tel_empresa.get()).replace(" ", "")
            except Exception as e:
                pass

            # Verificar já se temos pelo menos um contacto telefónico
            if (self.new_contact_telefone
                 or self.new_contact_telemovel
                 or self.new_contact_tel_emp):
                return True
            else:
                return False

    def _is_form_data_valid(self) -> bool:
        """ Verifica se todos os campos obrigatórios foram preenchidos e se os
            dados introduzidos estão corretos.
        """
        if not self.ef_ltxt_nome.get().strip():
            msg = 'O campo "Nome" é de preenchimento obrigatório.'
            messagebox.showwarning(message=msg, parent=self)
            self.ef_ltxt_nome.entry.focus()
            return False
        elif not self._validar_telefones():
            msg = 'Deverá indicar, pelo menos, um número de contacto telefónico.'
            messagebox.showwarning(message=msg, parent=self)
            return False
        elif not is_email(self.ef_ltxt_email.get().strip()):
            msg = 'O endereço de email introduzido não parece ser válido.'
            messagebox.showwarning(message=msg, parent=self)
            self.ef_ltxt_email.entry.focus()
            return False
        elif not (self.var_tipo_is_cliente.get()
                  or self.var_tipo_is_fornecedor.get()):
            msg = 'Por favor, especifique qual a categoria (cliente/fornecedor) a atribuir a este contacto.'
            messagebox.showwarning(message=msg, parent=self)
            self.ef_chkbtn_tipo_cliente.focus()
            return False
        else:
            return True


    def _on_update_contact(self, event=None):
        """ Recolhe todos os dados do formulário e guarda um novo contacto"""

        if not self._is_form_data_valid():
            return

        new_contact = {
            'id': self.num_contacto,
            'nome': self.ef_ltxt_nome.get(),
            'empresa': self.ef_ltxt_empresa.get(),
            'telefone': self.new_contact_telefone,
            'telemovel': self.new_contact_telemovel,
            'telefone_empresa': self.new_contact_tel_emp,
            'email': self.ef_ltxt_email.get(),
            'morada': self.ef_lstxt_morada.get(),
            'cod_postal': self.ef_ltxt_cod_postal.get(),
            'localidade': self.ef_ltxt_localidade.get(),
            'pais': self.ef_combo_pais.get(),
            'nif': self.ef_ltxt_nif.get(),
            'notas': self.ef_lstxt_notas.get(),
            'is_cliente': self.var_tipo_is_cliente.get(),
            'is_fornecedor': self.var_tipo_is_fornecedor.get(),
            'atualizado_por_utilizador_id': self.estado_app.janela_principal.user_id,
        }

        is_upd_successful = db.update_contact(new_contact)

        if is_upd_successful:
            self._on_contact_upd_success()
        else:
            wants_to_try_again_save = messagebox.askquestion(message='Não foi possível guardar este contacto na base de dados. Pretende tentar novamente?',
                                                             default='yes',
                                                             parent=self)
            if wants_to_try_again_save == 'yes':
                self._on_update_contact()
            else:
                self.on_contact_cancel()

    def create_window_detalhe_contacto(self, *event, num_contacto=None):
        self.contact_detail_windows_count += 1
        self.contacto_newDetailsWindow[self.contact_detail_windows_count] = tk.Toplevel(
        )
        self.contacto_newDetailsWindow[self.contact_detail_windows_count].title(
            f'Detalhe de contacto: {num_contacto}')
        self.janela_detalhes_contacto = contactDetailWindow(
            self.contacto_newDetailsWindow[self.contact_detail_windows_count],
            num_contacto,
            self.estado_app)
        self.contacto_newDetailsWindow[self.contact_detail_windows_count].focus()


    def _on_contact_upd_success(self):
        print("Contacto atualizado com sucesso!")
        self.atualizar_rodape()
        if self.estado_app.janela_contactos_aberta:
            if self.var_tipo_is_cliente:
                self.estado_app.janela_principal.janela_contactos.mostrar_clientes()
            elif self.var_tipo_is_fornecedor:
                self.estado_app.janela_principal.janela_contactos.mostrar_fornecedores()


    def on_btn_fechar(self, event):
        """ will test for some condition before closing, save if necessary and
                then call destroy()
        """
        window = event.widget.winfo_toplevel()
        window.destroy()

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

    def mostrar_painel_principal(self):
        self.note.pack(side='top', expand=True, fill='both')
        self.note.enable_traversal()

    def montar_rodape(self):
        nome_cr = self.contacto['criado_por_utilizador_nome']
        data_cr = self.contacto['created_on']
        txt_esquerda = f"Criado por {nome_cr} em {data_cr}."

        if self.contacto['atualizado_por_utilizador_nome'] is None:
            txt_direita = ""
        else:
            nome_updt = self.contacto['atualizado_por_utilizador_nome']
            data_updt = self.contacto['updated_on']
            txt_direita = f"Atualizado por {nome_updt} em {data_updt}."

        self.rodapeFont = tk.font.Font(family="Lucida Grande", size=9)
        self.rodapeTxtColor = "grey22"

        self.esquerda = ttk.Label(self.bottomframe, anchor='w', text=txt_esquerda,
                                  font=self.rodapeFont, foreground=self.rodapeTxtColor)
        self.direita = ttk.Label(self.bottomframe, anchor='e', text=txt_direita,
                                 font=self.rodapeFont, foreground=self.rodapeTxtColor)
        self.esquerda.pack(side="left")
        self.direita.pack(side="right")


    def atualizar_rodape(self):
        try:
            self.contacto = db.obter_contacto(self.num_contacto)
            nome_updt = self.contacto['atualizado_por_utilizador_nome']
            data_updt = self.contacto['updated_on']
            txt_direita = f"Atualizado por {nome_updt} em {data_updt}."
            self.direita.config(text=txt_direita)
        except:
            pass

    def bind_tree(self):
        self.tree.bind('<<TreeviewSelect>>', self.selectItem_popup)
        self.tree.bind('<Double-1>', lambda x: self.create_window_detalhe_rep(
            num_reparacao=self.reparacao_selecionada))
        self.tree.bind("<Button-2>", self.popupMenu)
        self.tree.bind("<Button-3>", self.popupMenu)
        self.update_idletasks()

    def unbind_tree(self):
        self.tree.bind('<<TreeviewSelect>>', None)
        self.tree.bind('<Double-1>', None)
        self.tree.bind("<Button-2>", None)
        self.tree.bind("<Button-3>", None)
        self.update_idletasks()

    # ------ Permitir que a tabela possa ser ordenada clicando no cabeçalho --
    def isNumeric(self, s):
        """
        test if a string s is numeric
        """
        if s == "":
            return False

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
        data = [(tree.set(child, col), child)
                for child in tree.get_children('')]
        # if the data to be sorted is numeric change to float
        data = self.changeNumeric(data)
        # now sort the data in place
        data.sort(reverse=descending)
        for ix, item in enumerate(data):
            tree.move(item[1], '', ix)
        # switch the heading so that it will sort in the opposite direction
        tree.heading(col, command=lambda col=col: self.sortBy(
            tree, col, int(not descending)))
        self.alternar_cores(tree)
    # ------ Fim das funções relacionadas c/ o ordenamento da tabela ---------

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

    def selectItem(self, *event):
        """
        Obter reparação selecionada (após clique de rato na linha correspondente)
        """
        curItem = self.tree.focus()
        tree_linha = self.tree.item(curItem)
        self.reparacao_selecionada = tree_linha["values"][0]


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
        # self.update_idletasks()

    def create_window_detalhe_rep(self, num_reparacao=None):
        self.rep_detail_windows_count += 1
        self.rep_newDetailsWindow[self.rep_detail_windows_count] = tk.Toplevel()
        self.janela_detalhes_rep = detalhe_reparacao.repairDetailWindow(
            self.rep_newDetailsWindow[self.rep_detail_windows_count],
            num_reparacao, self.estado_app)

    def contar_linhas(self):
        """ Obtém o número de linhas da tabela de processos desta remessa. """
        linhas = self.tree.get_children("")
        return len(linhas)

    def contar_reincidencias(self):
        """ Obtém o número processos deste contacto referentes a reincidências. """
        soma_reincidencias = 0
        for child in self.tree.get_children():
            if self.tree.item(child)["values"][5] != "":
                soma_reincidencias += 1
        return soma_reincidencias

    def atualizar_soma(self):
        """
        Atualiza o texto referente ao número de processos na remessa atual.
        """
        self.soma_reparacoes = self.contar_linhas()
        self.soma_reincidencias = self.contar_reincidencias()
        texto = f"Nº de processos deste contacto: {self.soma_reparacoes} ({self.soma_reincidencias} reincidências)"
        self.lbl_soma_processos.config(text=texto)

    def configurar_frames_e_estilos(self):
        self.master.minsize(W_DETALHE_CONTACTO_MIN_WIDTH, W_DETALHE_CONTACTO_MIN_HEIGHT)
        self.master.maxsize(W_DETALHE_CONTACTO_MAX_WIDTH, W_DETALHE_CONTACTO_MAX_HEIGHT)
        # self.master.geometry(W_DETALHE_CONTACTO_GEOMETRIA)  # Se ativada esta
        # linha, deixa de atualizar as medidas da janela ao mudar de separador
        self.master.title(f"Contacto nº{self.num_contacto}")

        self.dicas = Pmw.Balloon(self.master, label_background='#f6f6f6',
                                 hull_highlightbackground='#b3b3b3',
                                 state='balloon',
                                 relmouse='both',
                                 yoffset=18,
                                 xoffset=-2,
                                 initwait=1300)

        self.mainframe = ttk.Frame(self.master)
        self.topframe = ttk.Frame(self.mainframe, padding="5 8 5 5")
        self.centerframe = ttk.Frame(self.mainframe)
        self.bottomframe = ttk.Frame(self.mainframe, padding="3 1 3 1")

        self.estilo = ttk.Style()
        self.estilo.configure("Panel_Title.TLabel", pady=10, foreground="grey25", font=(
            "Helvetica Neue", 18, "bold"))
        self.estilo.configure("Panel_Body.TLabel", font=("Lucida Grande", 11))
        self.estilo.configure("TMenubutton", font=("Lucida Grande", 11))
        self.estilo.configure('Reparacoes_Remessa.Treeview', rowheight=42)

        self.btnFont = tk.font.Font(family="Lucida Grande", size=10)
        self.btnTxtColor = "grey22"

    def composeFrames(self):
        self.topframe.pack(side=tk.TOP, fill=tk.X)
        self.centerframe.pack(side=tk.TOP, expand=True, fill=tk.BOTH)
        self.bottomframe.pack(side=tk.BOTTOM, fill=tk.X)
        self.mainframe.pack(side=tk.TOP, expand=True, fill=tk.BOTH)
