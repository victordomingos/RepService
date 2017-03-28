#!/usr/bin/env python3.6
# encoding: utf-8
"""
Este módulo é parte integrante da aplicação RepService, desenvolvida por
Victor Domingos e distribuída sob os termos da licença Creative Commons
Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)
"""

from extra_tk_classes import *
from base_app import *


class RemessasWindow(baseApp):
    """ base class for application """
    def __init__(self,master, estado, *args,**kwargs):
        super().__init__(master,*args,**kwargs)
        self.estado = estado
        self.master.minsize(REMESSAS_MIN_WIDTH, REMESSAS_MIN_HEIGTH)
        self.master.maxsize(REMESSAS_MAX_WIDTH, REMESSAS_MAX_HEIGTH)
        self.centerframe = ttk.Frame(self.mainframe, padding="4 0 4 0")
        self.montar_barra_de_ferramentas()
        self.montar_tabela()

        #get status bar
        self.nremessas = 2345
        self.my_statusbar.set(f"{self.nremessas} remessas")
        
        self.gerar_painel_entrada()

        self.composeFrames()
        self.inserir_dados_de_exemplo()
        self.alternar_cores(self.tree)


    def montar_tabela(self):
        self.tree = ttk.Treeview(self.leftframe, height=60, selectmode='browse')
        self.tree['columns'] = ('ID', 'Destino', 'Qtd.', 'Data')
        self.tree.pack(side=tk.TOP, fill=tk.BOTH)
        self.tree.column('#0', anchor=tk.W, minwidth=0, stretch=0, width=0)
        self.tree.column('ID', anchor=tk.E, minwidth=37, stretch=0, width=37)
        self.tree.column('Destino', minwidth=110, stretch=1, width=110)
        self.tree.column('Qtd.', anchor=tk.E, minwidth=40, stretch=0, width=40)
        self.tree.column('Data', anchor=tk.E, minwidth=90, stretch=0, width=90)

        self.configurarTree()    
        self.leftframe.grid_columnconfigure(0, weight=1)
        self.leftframe.grid_rowconfigure(0, weight=1)


    def montar_barra_de_ferramentas(self):
        # Barra de ferramentas / botões -------------------------------------------------------------------------------

        self.btn_entrada = ttk.Button(self.topframe, text="Entrada", command=None)
        self.btn_entrada.grid(column=0, row=0)

        self.btn_saida = ttk.Button(self.topframe, text="Saída", command=None)
        self.btn_saida.grid(column=1, row=0)

        self.btn_add = ttk.Button(self.topframe, text=" ➕", width=3, command=self.show_entryform)
        self.btn_add.grid(column=3, row=0)

        self.text_input_pesquisa = ttk.Entry(self.topframe, width=12)
        self.text_input_pesquisa.grid(column=4, row=0)

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
        #self.MenuFicheiro.entryconfig("Novo contacto", state="disabled")
        #root.unbind_all("<Command-n>")
        self.show_entryform()        


    def fechar_painel_entrada(self, *event):
        #self.clear_text()
        self.hide_entryform()
        #root.bind_all("<Command-n>")


    def gerar_painel_entrada(self):

        #entryfr1-----------------------------
        #TODO:adicionar campos, notebook, etc
        #criar funções para usar esses campos, ora para adicionar, ora para editar, ora para visualizar registos
        pass
        """
        self.ef_var_tipo = IntVar()
        self.ef_var_estado = IntVar()
        self.ef_var_garantia = IntVar()
        self.ef_var_repr_loja = IntVar()
        self.ef_var_repr_loja.set(0)
        self.ef_var_efetuar_copia = IntVar()
        self.ef_var_find_my = IntVar()
        self.ef_var_local_intervencao = IntVar()
        self.ef_var_local_intervencao.set("Promais")
        
        self.ef_cabecalho = ttk.Frame(self.entryfr1, padding=4)
        self.ef_lbl_titulo = ttk.Label(self.ef_cabecalho, style="BW.TLabel", text="Adicionar Reparação:\n")
        self.ef_lbl_tipo = ttk.Label(self.ef_cabecalho, text="Tipo de processo:")
        self.ef_radio_tipo_cliente = ttk.Radiobutton(self.ef_cabecalho, text="Cliente", variable=self.ef_var_tipo, value=TIPO_REP_CLIENTE, command=self.radio_tipo_command)
        self.ef_radio_tipo_stock = ttk.Radiobutton(self.ef_cabecalho, text="Stock", variable=self.ef_var_tipo, value=TIPO_REP_STOCK, command=self.radio_tipo_command)        
        self.btn_adicionar = ttk.Button(self.ef_cabecalho, text="Adicionar", command=None)
        self.btn_cancelar = ttk.Button(self.ef_cabecalho, text="Cancelar", command=self.fechar_painel_entrada)

        
        self.ef_lbl_titulo.grid(column=0, row=0, columnspan=3, sticky=W)
        self.ef_lbl_tipo.grid(column=0, row=1, sticky=E)
        self.ef_radio_tipo_cliente.grid(column=1, row=1, sticky=W)
        self.ef_radio_tipo_stock.grid(column=2, row=1, sticky=W)
        self.btn_adicionar.grid(column=3, row=1, sticky=W+E)
        self.btn_cancelar.grid(column=3, row=2, sticky=W+E)
        
        self.ef_cabecalho.grid(column=0,row=0, sticky='we')
        self.entryfr1.columnconfigure(0, weight=1)
        self.ef_cabecalho.columnconfigure(0, weight=0)
        self.ef_cabecalho.columnconfigure(2, weight=1)

        #self.btn_adicionar.bind('<Button-1>', self.add_remessa)        


        #entryfr2-----------------------------
        self.ef_lf_cliente = ttk.Labelframe(self.entryfr2, padding=4, text="Dados do cliente")
        self.ef_txt_num_cliente = ttk.Entry(self.ef_lf_cliente, text="Nº", width=5)
        self.ef_btn_buscar_cliente = ttk.Button(self.ef_lf_cliente, width=1, text="?")
        self.ef_txt_nome_cliente = ttk.Entry(self.ef_lf_cliente, width=45)
        self.ef_lbl_telefone_lbl = ttk.Label(self.ef_lf_cliente, text="Tel.:")
        self.ef_lbl_telefone_info = ttk.Label(self.ef_lf_cliente, text="00 351 000 000 000")
        self.ef_lbl_email_lbl = ttk.Label(self.ef_lf_cliente, text="Email:")
        self.ef_lbl_email_info = ttk.Label(self.ef_lf_cliente, text="email.address@portugalmail.com")

        self.ef_lf_fornecedor = ttk.Labelframe(self.entryfr2, padding=4, text="Dados do fornecedor")
        self.ef_txt_num_fornecedor = ttk.Entry(self.ef_lf_fornecedor, text="Nº", width=5)
        self.ef_btn_buscar_fornecedor = ttk.Button(self.ef_lf_fornecedor, width=1, text="?")
        self.ef_txt_nome_fornecedor = ttk.Entry(self.ef_lf_fornecedor, width=45)
        self.ef_lbl_telefone_lbl_fornecedor = ttk.Label(self.ef_lf_fornecedor, text="Tel.:")
        self.ef_lbl_telefone_info_fornecedor = ttk.Label(self.ef_lf_fornecedor, text="00 351 000 000 000")
        self.ef_lbl_email_lbl_fornecedor = ttk.Label(self.ef_lf_fornecedor, text="Email:")
        self.ef_lbl_email_info_fornecedor = ttk.Label(self.ef_lf_fornecedor, text="email.address@portugalmail.com")

        self.ef_txt_num_cliente.grid(column=0, row=0, padx=5, sticky=W)
        self.ef_btn_buscar_cliente.grid(column=2, row=0, sticky=W)
        self.ef_txt_nome_cliente.grid(column=3, row=0,  padx=5, sticky=W)
        self.ef_lbl_telefone_lbl.grid(column=5, row=0, padx=5, sticky=E)
        self.ef_lbl_telefone_info.grid(column=6, row=0, padx=5,  sticky=W)
        self.ef_lbl_email_lbl.grid(column=7, row=0,  padx=5, sticky=E)
        self.ef_lbl_email_info.grid(column=8, row=0,  padx=5, sticky=W)

        self.ef_txt_num_fornecedor.grid(column=0, row=0, padx=5, sticky=W)
        self.ef_btn_buscar_fornecedor.grid(column=2, row=0, sticky=W)
        self.ef_txt_nome_fornecedor.grid(column=3, row=0,  padx=5, sticky=W)
        self.ef_lbl_telefone_lbl_fornecedor.grid(column=5, row=0,  padx=5, sticky=E)
        self.ef_lbl_telefone_info_fornecedor.grid(column=6, row=0,  padx=5, sticky=W)
        self.ef_lbl_email_lbl_fornecedor.grid(column=7, row=0,  padx=5, sticky=E)
        self.ef_lbl_email_info_fornecedor.grid(column=8, row=0,  padx=5, sticky=W)

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
        self.ef_lbl_descr_equipamento = ttk.Label(self.ef_lf_equipamento, text="Descrição:")
        self.ef_text_descr_equipamento = scrolledtext.ScrolledText(self.ef_lf_equipamento, highlightcolor="LightSteelBlue2", width=30, height=4)
        self.ef_lbl_estado_equipamento = ttk.Label(self.ef_lf_equipamento, text="Estado:")
        self.ef_radio_estado_marcas_uso = ttk.Radiobutton(self.ef_lf_equipamento, text="Marcas de uso", variable=self.ef_var_estado, value=0, command=self.radio_estado_command)
        self.ef_radio_estado_bom = ttk.Radiobutton(self.ef_lf_equipamento, text="Bom estado geral", variable=self.ef_var_estado, value=1, command=self.radio_estado_command)        
        self.ef_radio_estado_marcas_acidente = ttk.Radiobutton(self.ef_lf_equipamento, text="Marcas de acidente", variable=self.ef_var_estado, value=2, command=self.radio_estado_command)
        self.ef_radio_estado_faltam_pecas = ttk.Radiobutton(self.ef_lf_equipamento, text="Faltam peças", variable=self.ef_var_estado, value=3, command=self.radio_estado_command)        
        self.ef_lbl_obs_estado = ttk.Label(self.ef_lf_equipamento, text="Observações acerca do estado:")
        self.ef_text_obs_estado_equipamento = scrolledtext.ScrolledText(self.ef_lf_equipamento, highlightcolor="LightSteelBlue2", width=27, height=4)

        self.ef_lbl_garantia = ttk.Label(self.ef_lf_equipamento, text="Garantia:")
        self.ef_radio_garantia_fora_garantia = ttk.Radiobutton(self.ef_lf_equipamento, text="Fora de garantia", variable=self.ef_var_garantia, value=0, command=self.radio_garantia_command)
        self.ef_radio_garantia_neste = ttk.Radiobutton(self.ef_lf_equipamento, text="Sim, neste estabelecimento", variable=self.ef_var_garantia, value=1, command=self.radio_garantia_command)
        self.ef_radio_garantia_noutro = ttk.Radiobutton(self.ef_lf_equipamento, text="Sim, noutro estabelecimento", variable=self.ef_var_garantia, value=2, command=self.radio_garantia_command)
        self.ef_lbl_cod_artigo = ttk.Label(self.ef_lf_equipamento, text="\nCódigo de artigo:")
        self.ef_txt_cod_artigo = ttk.Entry(self.ef_lf_equipamento, width=15)
        self.ef_lbl_num_serie = ttk.Label(self.ef_lf_equipamento, text="\nNº de série:")
        self.ef_txt_num_serie = ttk.Entry(self.ef_lf_equipamento, width=15)
        self.ef_lbl_data_compra = ttk.Label(self.ef_lf_equipamento, text="\nData de compra:")
        self.ef_txt_data_compra = ttk.Entry(self.ef_lf_equipamento, width=15)
        self.ef_lbl_num_fatura = ttk.Label(self.ef_lf_equipamento, text="\nNº da fatura:")
        self.ef_txt_num_fatura = ttk.Entry(self.ef_lf_equipamento, width=15)
        self.ef_lbl_local_compra = ttk.Label(self.ef_lf_equipamento, text="\nEstabelecimento:")
        self.ef_txt_local_compra = ttk.Entry(self.ef_lf_equipamento, width=15)
        
        self.ef_lbl_num_fatura_fornecedor = ttk.Label(self.ef_lf_equipamento, text="Nº fatura fornecedor:")
        self.ef_txt_num_fatura_fornecedor = ttk.Entry(self.ef_lf_equipamento, width=18)
        self.ef_lbl_data_fatura_fornecedor = ttk.Label(self.ef_lf_equipamento, text="Data fatura fornecedor:")
        self.ef_txt_data_fatura_fornecedor = ttk.Entry(self.ef_lf_equipamento, width=18)
        self.ef_lbl_nar = ttk.Label(self.ef_lf_equipamento, text="NAR:")
        self.ef_txt_nar = ttk.Entry(self.ef_lf_equipamento, width=18)
        self.ef_lbl_num_guia_rececao = ttk.Label(self.ef_lf_equipamento, text="Guia de receção:")
        self.ef_txt_num_guia_rececao = ttk.Entry(self.ef_lf_equipamento, width=18)
        self.ef_lbl_data_entrada_stock = ttk.Label(self.ef_lf_equipamento, text="Data de entrada em stock:")
        self.ef_txt_data_entrada_stock = ttk.Entry(self.ef_lf_equipamento, width=18)
        self.ef_lbl_num_quebra_stock = ttk.Label(self.ef_lf_equipamento, text="Nº de quebra de stock:")
        self.ef_txt_num_quebra_stock = ttk.Entry(self.ef_lf_equipamento, width=18)

        self.ef_lbl_descr_equipamento.grid(column=0, row=0, padx=5, sticky=W)
        self.ef_text_descr_equipamento.grid(column=0, row=1, columnspan=2, rowspan=4, padx=5, sticky=W+E+N+S)
        self.ef_lbl_estado_equipamento.grid(column=2, row=0, padx=5, sticky=W)
        self.ef_radio_estado_marcas_uso.grid(column=2, row=1, padx=5, sticky=W)
        self.ef_radio_estado_bom.grid(column=2, row=2, padx=5, sticky=W)
        self.ef_radio_estado_marcas_acidente.grid(column=2, row=3, padx=5, sticky=W)
        self.ef_radio_estado_faltam_pecas.grid(column=2, row=4, padx=5, sticky=W)
        self.ef_lbl_obs_estado.grid(column=3, row=0, padx=5, sticky=W)
        self.ef_text_obs_estado_equipamento.grid(column=3, row=1, rowspan=4, padx=5, sticky=W+E+N+S)
        self.ef_lbl_garantia.grid(column=4, row=0, padx=5, sticky=W)
        self.ef_radio_garantia_fora_garantia.grid(column=4, row=1, padx=5, sticky=W)
        self.ef_radio_garantia_neste.grid(column=4, row=2, padx=5, sticky=W)
        self.ef_radio_garantia_noutro.grid(column=4, row=3, padx=5, sticky=W)
        self.ef_lbl_cod_artigo.grid(column=0, row=5, padx=5, sticky=W+E)
        self.ef_txt_cod_artigo.grid(column=0, row=6, padx=5, sticky=W+E)
        self.ef_lbl_num_serie.grid(column=1, row=5, padx=5, sticky=W+E)
        self.ef_txt_num_serie.grid(column=1, row=6, padx=5, sticky=W+E)
        self.ef_lbl_data_compra.grid(column=2, row=5, padx=5, sticky=W+E)
        self.ef_txt_data_compra.grid(column=2, row=6, padx=5, sticky=W+E)
        self.ef_lbl_num_fatura.grid(column=3, row=5, padx=5, sticky=W+E)
        self.ef_txt_num_fatura.grid(column=3, row=6, padx=5, sticky=W+E)

        self.ef_lf_equipamento.grid(column=0,row=0, sticky='we')
        self.entryfr3.columnconfigure(0, weight=1)

        self.ef_lf_equipamento.columnconfigure(0, weight=1)
        self.ef_lf_equipamento.columnconfigure(1, weight=1)
        self.ef_lf_equipamento.columnconfigure(2, weight=1)
        self.ef_lf_equipamento.columnconfigure(3, weight=1)
        self.ef_lf_equipamento.columnconfigure(4, weight=1)


        #entryfr4-----------------------------
        self.ef_lf_servico = ttk.Labelframe(self.entryfr4, padding=4, text="\nAvaria e/ou serviço a realizar")
        self.ef_text_descr_avaria_servico = scrolledtext.ScrolledText(self.ef_lf_servico, highlightcolor="LightSteelBlue2", width=20, height=5)
        self.ef_chkbtn_avaria_reprod_loja = ttk.Checkbutton(self.ef_lf_servico, variable=self.ef_var_repr_loja, width=27, text="Avaria reproduzida na loja")
        self.ef_lbl_senha = ttk.Label(self.ef_lf_servico, text="Senha:")
        self.ef_txt_senha = ttk.Entry(self.ef_lf_servico, width=22)
        self.ef_lbl_find_my = ttk.Label(self.ef_lf_servico, width=27, text="Find my iPhone ativo?")
        self.ef_radio_find_my_sim = ttk.Radiobutton(self.ef_lf_servico, text="Sim", variable=self.ef_var_find_my, value=1, command=self.radio_find_my)
        self.ef_radio_find_my_nao = ttk.Radiobutton(self.ef_lf_servico, text="Não", variable=self.ef_var_find_my, value=0, command=self.radio_find_my)
        self.ef_radio_find_my_nao_aplic = ttk.Radiobutton(self.ef_lf_servico, text="Não aplicável", variable=self.ef_var_find_my, value=2, command=self.radio_find_my)
        self.ef_lbl_espaco = ttk.Label(self.ef_lf_servico, text=" ")
        self.ef_lbl_efetuar_copia = ttk.Label(self.ef_lf_servico, text="Efetuar cópia de segurança?")
        self.ef_radio_efetuar_copia_sim = ttk.Radiobutton(self.ef_lf_servico, text="Sim", variable=self.ef_var_efetuar_copia, value=1, command=self.radio_copia_command)
        self.ef_radio_efetuar_copia_nao = ttk.Radiobutton(self.ef_lf_servico, text="Não", variable=self.ef_var_efetuar_copia, value=0, command=self.radio_copia_command)
        self.ef_radio_efetuar_copia_n_aplic = ttk.Radiobutton(self.ef_lf_servico, text="Não aplicável", variable=self.ef_var_efetuar_copia, value=2, command=self.radio_copia_command)

        self.ef_text_descr_avaria_servico.grid(column=0, row=0, columnspan=3, rowspan=5, padx=5, sticky=W+E+N+S)
        self.ef_chkbtn_avaria_reprod_loja.grid(column=3, row=0, columnspan=3, padx=5, sticky=N+W)
        self.ef_lbl_senha.grid(column=3, row=3, columnspan=3, padx=5, sticky=W)
        self.ef_txt_senha.grid(column=3, row=4, columnspan=3, padx=5, sticky=W)
        self.ef_lbl_find_my.grid(column=6, row=0, columnspan=3, padx=5, sticky=W)
        self.ef_radio_find_my_sim.grid(column=6, row=1, padx=5, sticky=W)
        self.ef_radio_find_my_nao.grid(column=7, row=1, sticky=W)
        self.ef_radio_find_my_nao_aplic.grid(column=8, row=1, sticky=W)
        self.ef_lbl_espaco.grid(column=8, row=2, sticky=W)
        self.ef_lbl_efetuar_copia.grid(column=6, row=3, columnspan=3, padx=5, sticky=W)
        self.ef_radio_efetuar_copia_sim.grid(column=6, row=4, padx=5, sticky=W)
        self.ef_radio_efetuar_copia_nao.grid(column=7, row=4, sticky=W)
        self.ef_radio_efetuar_copia_n_aplic.grid(column=8, row=4, sticky=W)

        self.ef_lf_servico.grid(column=0,row=0, sticky='we')
        self.entryfr4.columnconfigure(0, weight=1)

        self.ef_lf_servico.columnconfigure(0, weight=1)

        #entryfr5-----------------------------
            #Notas: text 3 linhas
            # local intervenção lbl + combobox(contactos>fornecedores)
        self.ef_lf_outros_dados = ttk.Labelframe(self.entryfr5, padding=4, text="\nOutros dados")
        self.ef_lbl_acessorios_entregues = ttk.Label(self.ef_lf_outros_dados, text="Acessórios entregues:")
        self.ef_text_acessorios_entregues = scrolledtext.ScrolledText(self.ef_lf_outros_dados, highlightcolor="LightSteelBlue2", height=3)
        #self.ef_lbl_espaco = ttk.Label(self.ef_lf_outros_dados, text="  ")
        self.ef_lbl_notas = ttk.Label(self.ef_lf_outros_dados, width=27, text="Notas:")
        self.ef_text_notas = scrolledtext.ScrolledText(self.ef_lf_outros_dados, highlightcolor="LightSteelBlue2", height=3)
        self.ef_lbl_local_intervencao = ttk.Label(self.ef_lf_outros_dados, width=27,  text="Local de intervenção:")
        self.ef_combo_local_intervencao = ttk.Combobox(self.ef_lf_outros_dados, width=21, textvariable=self.ef_var_local_intervencao, values=("Promais", "Techdata", "Servisoft", "Minitel", "Masterproxy", "Ponto Sagres"), state='readonly')

        self.ef_lbl_acessorios_entregues.grid(column=0, row=0, padx=5, sticky=W)
        self.ef_text_acessorios_entregues.grid(column=0, row=1, rowspan=3, padx=5, sticky=W+E+N+S)
        self.ef_lbl_notas.grid(column=1, row=0, padx=5, sticky=W+E)
        self.ef_text_notas.grid(column=1, row=1, rowspan=3, padx=5, sticky=W+E+N+S)
        self.ef_lbl_local_intervencao.grid(column=2, row=0, padx=5, sticky=W)
        self.ef_combo_local_intervencao.grid(column=2, row=1, padx=5, sticky=W+E)
        
        self.ef_lf_outros_dados.grid(column=0,row=0, sticky='we')
        self.entryfr5.columnconfigure(0, weight=1)

        self.ef_lf_outros_dados.columnconfigure(0, weight=1)
        self.ef_lf_outros_dados.columnconfigure(1, weight=1)
        self.ef_lf_outros_dados.columnconfigure(2, weight=0)

        """
        #--- acabaram os 'entryfr', apenas código geral para o entryframe a partir daqui ---        
        #self.entryframe.bind_all("<Command-Escape>", self.fechar_painel_entrada)


    def liga_desliga_menu_novo(self, *event):
        """ 
        Liga e desliga menus com base na configuração atual da janela. Por exemplo, ao
        abrir o painel de entrada de dados, desativa o menu "nova reparação", para evitar
        que o painel se feche inadvertidamente.
        """
        if self.is_entryform_visible == True:
            self.MenuFicheiro.entryconfigure("Novo contacto", state="disabled")
            # TODO - corrigir bug: o atalho de teclado só fica realmente inativo depois de acedermos ao menu ficheiro. Porquê??
            root.unbind_all("<Command-Option-n>")
        else:
            self.MenuFicheiro.entryconfigure("Novo contacto", state="active")
            root.bind_all("<Command-Option-n>")


    def inserir_dados_de_exemplo(self):
        for i in range(2560):
            self.tree.insert("", "end", text="", values=(str(i),"Fornecedor", "3", "2017-12-31"))
            self.tree.insert("", "end", text="", values=(str(i),"Centro técnico", "10", "2017-01-12"))
            self.tree.insert("", "end", text="", values=(str(i),"Distribuidor internacional", "10", "2017-02-01"))


