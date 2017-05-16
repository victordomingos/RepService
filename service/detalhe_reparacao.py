#!/usr/bin/env python3.6
# encoding: utf-8
"""
Este módulo é parte integrante da aplicação RepService, desenvolvida por
Victor Domingos e distribuída sob os termos da licença Creative Commons
Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)
"""
import tkinter as tk
from tkinter import ttk
from global_setup import *
from extra_tk_classes import *


class repairDetailWindow(ttk.Frame):
    """ Classe de base para a janela de detalhes de reparações """
    def __init__(self, master, num_reparacao, *args,**kwargs):
        super().__init__(master,*args,**kwargs)
        self.master = master
        self.num_reparacao = num_reparacao
        self.tipo_processo = "Cliente" if True else "Stock"  #TODO: Substituir True por função que busca tipo na info da base de dados
        self.estado = ESTADOS[EM_PROCESSAMENTO] #TODO: Obter estado a partir da base de dados

        if self.tipo_processo == "Cliente":
            self.numero_contacto = "12345" #TODO numero de cliente
            self.nome = "Norberto Plutarco Keppler" #TODO Nome do cliente
            self.telefone = "+351 900 000 000" #TODO Telefone do cliente
            self.email = "repservice@the-NPK-programming-team.py" #TODO Email do cliente
        else:
            self.numero_contacto = "90000" #TODO numero de fornecedor
            self.nome = "That International Provider of Great Stuff, Inc." #TODO Nome do fornecedor
            self.telefone = "+351 200 000 000" #TODO Telefone do fornecedor
            self.email = "repservice@the-NPK-programming-team.py" #TODO Email do fornecedor


        self.configurar_frames_e_estilos()
        self.montar_barra_de_ferramentas()
        self.montar_painel_principal()
        self.montar_rodape()
        self.composeFrames()


    def montar_barra_de_ferramentas(self):
        self.lbl_titulo = ttk.Label(self.topframe, style="Panel_Title.TLabel", foreground=self.btnTxtColor, text=f"Reparação nº {self.num_reparacao}")

        # Reincidência apenas aparece se reparação está entregue, anulado, abandonado, sem_informacao
        if self.estado >= ESTADOS[ENTREGUE]:
            self.btn_reincidencia = ttk.Button(self.topframe, text="➕", width=4, command=None)
            self.lbl_reincidencia = ttk.Label(self.topframe, font=self.btnFont, foreground=self.btnTxtColor, text="Criar reincidência")

        # Botão para registar entrega apenas aparece se reparação ainda não está entregue
        if self.estado != ESTADOS[ENTREGUE]:
            self.btn_entregar = ttk.Button(self.topframe, text=" ✅", width=4, command=None)
            self.lbl_entregar = ttk.Label(self.topframe, font=self.btnFont, foreground=self.btnTxtColor, text="Entregar")

        # ----------- Botão com menu "Alterar estado" --------------
        self.label_mbtn_alterar_estado = ttk.Label(self.topframe, font=self.btnFont, foreground=self.btnTxtColor, text="Atualizar")
        self.mbtn_alterar_estado = ttk.Menubutton(self.topframe, style="TMenubutton", text="Estado")
        self.mbtn_alterar_estado.menu = tk.Menu(self.mbtn_alterar_estado, tearoff=0)
        self.mbtn_alterar_estado["menu"] = self.mbtn_alterar_estado.menu

        self.mbtn_alterar_estado.menu.add_command(label=ESTADOS[EM_PROCESSAMENTO], command=None)
        self.mbtn_alterar_estado.menu.add_command(label=ESTADOS[AGUARDA_ENVIO], command=None)
        self.mbtn_alterar_estado.menu.add_command(label=ESTADOS[AGUARDA_RESP_FORNECEDOR], command=None)
        self.mbtn_alterar_estado.menu.add_command(label=ESTADOS[AGUARDA_RESP_CLIENTE], command=None)
        self.mbtn_alterar_estado.menu.add_command(label=ESTADOS[AGUARDA_RECECAO], command=None)
        self.mbtn_alterar_estado.menu.add_command(label=ESTADOS[RECEBIDO], command=None)
        self.mbtn_alterar_estado.menu.add_command(label=ESTADOS[DISPONIVEL_P_LEVANTAMENTO], command=None)
        self.mbtn_alterar_estado.menu.add_separator()
        self.mbtn_alterar_estado.menu.add_command(label=ESTADOS[ENTREGUE], command=None)
        self.mbtn_alterar_estado.menu.add_separator()
        self.mbtn_alterar_estado.menu.add_command(label=ESTADOS[ANULADO], command=None)
        self.mbtn_alterar_estado.menu.add_command(label=ESTADOS[ABANDONADO], command=None)
        self.mbtn_alterar_estado.menu.add_command(label=ESTADOS[SEM_INFORMACAO], command=None)
        # ----------- fim de Botão com menu "Alterar estado" -------------


        # ----------- Botão com menu "Alterar Prioridade" --------------
        self.label_mbtn_alterar_prioridade = ttk.Label(self.topframe, font=self.btnFont, foreground=self.btnTxtColor, text="Alterar")
        self.mbtn_alterar_prioridade = ttk.Menubutton(self.topframe, text="Prioridade")
        self.mbtn_alterar_prioridade.menu = tk.Menu(self.mbtn_alterar_prioridade, tearoff=0)
        self.mbtn_alterar_prioridade["menu"] = self.mbtn_alterar_prioridade.menu

        self.mbtn_alterar_prioridade.menu.add_command(label="Baixa", command=None)
        self.mbtn_alterar_prioridade.menu.add_command(label="Normal", command=None)
        self.mbtn_alterar_prioridade.menu.add_command(label="Alta", command=None)
        self.mbtn_alterar_prioridade.menu.add_command(label="Urgente", command=None)
        # ----------- fim de Botão com menu "Alterar Prioridade" -------------



        # ----------- Botão com menu "Copiar" --------------
        self.label_mbtn_copiar = ttk.Label(self.topframe, font=self.btnFont, foreground=self.btnTxtColor, text="Copiar")
        self.mbtn_copiar = ttk.Menubutton(self.topframe, text=" ⚡")
        self.mbtn_copiar.menu = tk.Menu(self.mbtn_copiar, tearoff=0)
        self.mbtn_copiar["menu"] = self.mbtn_copiar.menu

        if self.tipo_processo == "Cliente":
            self.mbtn_copiar.menu.add_command(label="Nome", command=None)
            self.mbtn_copiar.menu.add_command(label="NIF", command=None)
            self.mbtn_copiar.menu.add_command(label="Morada", command=None)
            self.mbtn_copiar.menu.add_command(label="Código Postal", command=None)
            self.mbtn_copiar.menu.add_command(label="Localidade", command=None)

        self.mbtn_copiar.menu.add_command(label="Email", command=None)
        self.mbtn_copiar.menu.add_command(label="Telefone", command=None)
        self.mbtn_copiar.menu.add_separator()
        self.mbtn_copiar.menu.add_command(label="Número de série", command=None)
        self.mbtn_copiar.menu.add_command(label="Descrição do equipamento", command=None)

        self.mbtn_copiar.menu.add_command(label=ESTADOS[SEM_INFORMACAO], command=None)
        # ----------- fim de Botão com menu "Copiar" -------------


        # ----------- Botão com menu "Imprimir" --------------
        self.label_mbtn_imprimir = ttk.Label(self.topframe, font=self.btnFont, foreground=self.btnTxtColor, text="Imprimir")
        self.mbtn_imprimir = ttk.Menubutton(self.topframe, text="Imprimir")
        self.mbtn_imprimir.menu = tk.Menu(self.mbtn_imprimir, tearoff=0)
        self.mbtn_imprimir["menu"] = self.mbtn_imprimir.menu

        self.mbtn_imprimir.menu.add_command(label="Guia de receção: loja e cliente", command=None)
        self.mbtn_imprimir.menu.add_command(label="Guia de receção: loja e serviço técnico", command=None)

        # TODO - Ocultar ou desativar estas opções se não houver um orçamento criado para esta reparação
        self.mbtn_imprimir.menu.add_separator()
        self.mbtn_imprimir.menu.add_command(label="Orçamento", command=None)
        self.mbtn_imprimir.menu.add_command(label="Recibo de pagamento: orçamento", command=None)

        # TODO - Ocultar ou desativar estas opções se não houver um empréstimo criado para esta reparação
        self.mbtn_imprimir.menu.add_separator()
        self.mbtn_imprimir.menu.add_command(label="Documento de empréstimo", command=None)
        self.mbtn_imprimir.menu.add_command(label="Recibo de pagamento: caução de empréstimo", command=None)
        # ----------- fim de Botão com menu "Imprimir" -------------


        icon_path = APP_PATH + "/images/icon.gif"
        self.icon = tk.PhotoImage(file=(APP_PATH+"/images/icon.gif"))

        self.btn_comunicacao = ttk.Button(self.topframe, text="✉️", width=4, command=None)
        self.lbl_comunicacao = ttk.Label(self.topframe, font=self.btnFont, foreground=self.btnTxtColor, text="Comunicação")


        self.lbl_titulo.grid(column=0, row=0, rowspan=2)

        self.mbtn_alterar_estado.grid(column=4, row=0)
        #self.label_mbtn_alterar_estado.grid(column=4, row=1)
        self.mbtn_alterar_prioridade.grid(column=5, row=0)
        #self.label_mbtn_alterar_prioridade.grid(column=5, row=1)

        self.btn_comunicacao.grid(column=7, row=0)
        #self.lbl_comunicacao.grid(column=7, row=1)
        self.mbtn_copiar.grid(column=8, row=0)
        #self.label_mbtn_copiar.grid(column=8, row=1)
        self.mbtn_imprimir.grid(column=9, row=0)
        #self.label_mbtn_imprimir.grid(column=9, row=1)


        # Reincidência apenas aparece se reparação está entregue, anulado, abandonado, sem_informacao
        if self.estado >= ESTADOS[ENTREGUE]:
            self.btn_reincidencia.grid(column=10, row=0)
            self.lbl_reincidencia.grid(column=10, row=1)

        # Botão para registar entrega apenas aparece se reparação ainda não está entregue
        if self.estado != ESTADOS[ENTREGUE]:
            self.btn_entregar.grid(column=11, row=0)
            #self.lbl_entregar.grid(column=11, row=1)


        #self.estilo.configure("TSeparator", width=10, relief="flat", background="blue", foreground="red")
        #self.separador1 = ttk.Separator(self.centerframe, style="TSeparator", orient='horizontal').pack(side='top', pady=5, expand=True, fill='x')
        self.topframe.grid_columnconfigure(2, weight=1)
        #self.topframe.grid_columnconfigure(6, weight=1)


    def montar_painel_principal(self):
        print(f"A mostrar detalhes da reparação nº {self.num_reparacao}")
        self.note = ttk.Notebook(self.centerframe, padding="3 20 3 3")

        self.tab_geral = ttk.Frame(self.note, padding=10)
        self.tab_historico = ttk.Frame(self.note, padding=10)
        self.tab_orcamentos = ttk.Frame(self.note, padding=10)
        self.tab_emprestimos = ttk.Frame(self.note, padding=10)

        self.note.add(self.tab_geral, text="Geral")
        self.note.add(self.tab_historico, text = "Histórico")
        self.note.add(self.tab_orcamentos, text = "Orçamentos")
        self.note.add(self.tab_emprestimos, text = "Empréstimos")

        self.geral_fr1 = ttk.Frame(self.tab_geral)
        self.geral_fr2 = ttk.Frame(self.tab_geral)
        self.geral_fr3 = ttk.Frame(self.tab_geral)
        self.geral_fr4 = ttk.Frame(self.tab_geral)


        # TAB Geral ~~~~~~~~~~~~~~~~

        # TODO - obter valor da base de dados
        self.txt_numero_contacto = ttk.Entry(self.geral_fr1, width=5)
        self.txt_numero_contacto.insert(0, self.numero_contacto)
        self.btn_buscar_cliente = ttk.Button(self.geral_fr1, width=1, text="+", command=lambda *x: self.create_window_contacts(criar_novo_contacto="Cliente")) # TODO - abrir ficha de cliente
        self.txt_nome = ttk.Entry(self.geral_fr1, width=35)
        self.txt_nome.insert(0, self.nome)
        self.lbl_telefone = ttk.Label(self.geral_fr1, style="Panel_Body.TLabel", text=f"Tel.:{self.telefone}")
        self.lbl_email = ttk.Label(self.geral_fr1, style="Panel_Body.TLabel", text=f"Email:{self.email}")

        self.ltxt_descr_equipamento = LabelText(self.geral_fr2, "Descrição:", style="Panel_Body.TLabel", height=2)
        self.ltxt_descr_equipamento.scrolledtext.insert('insert', 'Texto de exemplo para experimentar como sai na prática.\nIsto fica noutra linha...')

        estado = f'Estado: {"Marcas de acidente"}'  # TODO: obter string do estado do equipamento
        self.ltxt_obs_estado_equipamento = LabelText(self.geral_fr2, estado, style="Panel_Body.TLabel", height=2)
        self.ltxt_obs_estado_equipamento.scrolledtext.insert('insert', 'Texto de exemplo para experimentar como sai na prática.\n Eqauipamento muito danificado!...')

        garantia = True
        if garantia:
            self.ltxt_data_compra = LabelEntry(self.geral_fr2, "Data de compra:", style="Panel_Body.TLabel")
            self.ltxt_data_compra.entry.insert(0, '29-07-2035')
            self.ltxt_num_fatura = LabelEntry(self.geral_fr2, "Nº da fatura:", style="Panel_Body.TLabel")
            self.ltxt_num_fatura.entry.insert(0, 'FCR 1234567890/2035')
            self.ltxt_garantia = LabelEntry(self.geral_fr2, "Garantia em:", style="Panel_Body.TLabel")
            self.ltxt_garantia.entry.insert(0, 'NPK International Online Store')
        else:
            self.lbl_garantia = ttk.Label(self.geral_fr2, text="Garantia:\nFora de garantia", style="Panel_Body.TLabel")

        self.ltxt_cod_artigo = LabelEntry(self.geral_fr2, "Código de artigo:", style="Panel_Body.TLabel")
        self.ltxt_cod_artigo.entry.insert(0, 'Z0GV2345623P')
        self.ltxt_num_serie = LabelEntry(self.geral_fr2, "Nº de série:", style="Panel_Body.TLabel")
        self.ltxt_num_serie.entry.insert(0, 'C02G387HJG7865BNFV')
        self.ltxt_local_intervencao = LabelEntry(self.geral_fr2, "Local da intervenção:", style="Panel_Body.TLabel")
        self.ltxt_local_intervencao.entry.insert(0, 'Aquele Tal Centro Técnico')

        self.ltxt_descr_avaria = LabelText(self.geral_fr2, "Avaria/Serviço:", style="Panel_Body.TLabel")
        self.ltxt_descr_avaria.scrolledtext.insert('insert', 'Texto de exemplo para experimentar como sai na prática.\nIsto fica noutra linha...')

        self.ltxt_acessorios = LabelText(self.geral_fr2, "Acessórios entregues:", style="Panel_Body.TLabel")
        self.ltxt_acessorios.scrolledtext.insert('insert', 'Texto de exemplo para experimentar como sai na prática.\nIsto fica noutra linha...')
        self.ltxt_notas = LabelText(self.geral_fr2, "Notas:", style="Panel_Body.TLabel")
        self.ltxt_notas.scrolledtext.insert('insert', 'Texto de exemplo para experimentar como sai na prática.\nIsto fica noutra linha...')


        # Desativar todos os campos de texto para não permitir alterações. TODO: verificar se todos os widgets foram mesmo criados garantia/fora de garantia, stock/cliente
        for widget in (self.txt_numero_contacto, 
                       self.txt_nome,
                       self.ltxt_descr_equipamento.scrolledtext,
                       self.ltxt_obs_estado_equipamento.scrolledtext,
                       self.ltxt_data_compra.entry,
                       self.ltxt_num_fatura.entry,
                       self.ltxt_cod_artigo.entry,
                       self.ltxt_num_serie.entry,
                       self.ltxt_garantia.entry,
                       self.ltxt_local_intervencao.entry,
                       self.ltxt_descr_avaria.scrolledtext,
                       self.ltxt_acessorios.scrolledtext,
                       self.ltxt_notas.scrolledtext,
                    ):
            widget.configure(state="disabled")
        
        
        """
        
        self.ef_ltxt_num_fatura_fornecedor = LabelEntry(self.ef_lf_equipamento, "Nº fatura fornecedor:", width=15)
        self.ef_ltxt_data_fatura_fornecedor = LabelEntry(self.ef_lf_equipamento, "Data fatura fornecedor:", width=15)
        self.ef_ltxt_nar = LabelEntry(self.ef_lf_equipamento, "NAR:", width=15)
        self.ef_ltxt_num_guia_rececao = LabelEntry(self.ef_lf_equipamento, "Guia de receção:", width=15)
        self.ef_ltxt_data_entrada_stock = LabelEntry(self.ef_lf_equipamento, "Data de entrada em stock:", width=15)
        self.ef_ltxt_num_quebra_stock = LabelEntry(self.ef_lf_equipamento, "Nº de quebra de stock:", width=15)

        

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
        """
        self.txt_numero_contacto.grid(column=0, row=0)
        self.btn_buscar_cliente.grid(column=1, row=0)
        self.txt_nome.grid(column=2, sticky='we', row=0)
        self.lbl_telefone.grid(column=3, sticky='w', row=0)
        self.lbl_email.grid(column=4, sticky='we', row=0)

        self.geral_fr1.grid_columnconfigure(4, weight=1)
        self.geral_fr1.grid_columnconfigure(3, weight=1)
        self.geral_fr1.grid_columnconfigure(2, weight=1)


        self.ltxt_descr_equipamento.grid(column=0, row=0, columnspan=2, rowspan=4, sticky='we', padx=4)
        self.ltxt_obs_estado_equipamento.grid(column=2, row=0, columnspan=2, rowspan=4, sticky='we', padx=4)

        self.ltxt_cod_artigo.grid(column=4, row=0, rowspan=2,  sticky='we', padx=4)
        self.ltxt_num_serie.grid(column=4, row=2, rowspan=2, sticky='we', padx=4)

        ttk.Separator(self.geral_fr2).grid(column=0, row=4, columnspan=5, sticky='we', pady=10)
        
        self.ltxt_garantia.grid(column=0, row=5, columnspan=2, rowspan=2, sticky='we', padx=4)
        self.ltxt_data_compra.grid(column=2, row=5, rowspan=2, sticky='we', padx=4)
        self.ltxt_num_fatura.grid(column=3, row=5, rowspan=2, sticky='we', padx=4)
        self.ltxt_local_intervencao.grid(column=4, row=5, rowspan=2, sticky='we', padx=4)

        ttk.Separator(self.geral_fr2).grid(column=0, row=7, columnspan=5, sticky='we', pady=10)
        self.ltxt_descr_avaria.grid(column=0, row=8, columnspan=2, rowspan=4, sticky='we', padx=4)

        ttk.Separator(self.geral_fr2).grid(column=0, row=12, columnspan=5, sticky='we', pady=10)
        self.ltxt_acessorios.grid(column=0, row=13, columnspan=2, rowspan=3, sticky='wes', padx=4)
        self.ltxt_notas.grid(column=2, row=13, columnspan=3, rowspan=3, sticky='wes', padx=4)

        self.geral_fr2.grid_columnconfigure(0, weight=2)
        for i in range(1,5):
            self.geral_fr2.grid_columnconfigure(i, weight=1)

        self.geral_fr1.pack(side='top', expand=True, fill='x')
        ttk.Separator(self.tab_geral).pack(side='top', expand=False, fill='both', pady=10)
        self.geral_fr2.pack(side='top', expand=True, fill='both')
        """
        ttk.Separator(self.tab_geral).pack(side='top', expand=True, fill='both', pady=10)
        self.geral_fr3.pack(side='top', expand=True, fill='both')
        ttk.Separator(self.tab_geral).pack(side='top', expand=True, fill='both', pady=10)
        self.geral_fr4.pack(side='top', expand=True, fill='both')
        """


        # TAB Histórico ~~~~~~~~~~~~~~~


        # TAB Orçamentos (ocultar se reparação de stock) ~~~~~~~~~~~~~~~~~~~~~~~~~~~ TODO


        # TAB Empréstimos (ocultar se reparação de stock) ~~~~~~~~~~~~~~~~~~~~ TODO


        self.note.pack(side='top', expand=True, fill='both')
        self.note.enable_traversal()



    def montar_rodape(self):
        #TODO - obter dados da base de dados
        txt_esquerda = "Criado por Victor Domingos em 12/05/2021 18:01."
        txt_direita = "Fechado por Victor Domingos em 13/05/2021 17:01."

        self.rodapeFont = tk.font.Font(family="Lucida Grande", size=9)
        self.rodapeTxtColor = "grey22"

        self.esquerda = ttk.Label(self.bottomframe, anchor='w', text=txt_esquerda, font=self.rodapeFont, foreground=self.rodapeTxtColor)
        self.direita = ttk.Label(self.bottomframe, anchor='e', text=txt_direita, font=self.rodapeFont, foreground=self.rodapeTxtColor)
        self.esquerda.pack(side="left")
        self.direita.pack(side="right")



    def configurar_frames_e_estilos(self):
        #self.master.minsize(W_DETALHE_REP_MIN_WIDTH, W_DETALHE_REP_MIN_HEIGHT)
        #self.master.maxsize(W_DETALHE_REP_MAX_WIDTH, W_DETALHE_REP_MAX_HEIGHT)
        #self.master.geometry(W_DETALHE_REP_GEOMETRIA)
        self.master.title(f"Reparação nº{self.num_reparacao} ({self.tipo_processo})")

        self.mainframe = ttk.Frame(self.master)
        self.topframe = ttk.Frame(self.mainframe, padding="5 8 5 5")
        self.centerframe = ttk.Frame(self.mainframe)
        self.bottomframe = ttk.Frame(self.mainframe, padding="3 1 3 1")

        self.estilo = ttk.Style()
        self.estilo.configure("Panel_Title.TLabel", pady=10, foreground="grey25", font=("Helvetica Neue", 18, "bold"))
        self.estilo.configure("Panel_Body.TLabel", font=("Lucida Grande", 11))
        self.estilo.configure("TMenubutton", font=("Lucida Grande", 11))

        self.btnFont = tk.font.Font(family="Lucida Grande", size=10)
        self.btnTxtColor = "grey22"


    def composeFrames(self):
        self.topframe.pack(side=tk.TOP, fill=tk.X)
        self.centerframe.pack(side=tk.TOP, expand=True, fill=tk.BOTH)
        self.bottomframe.pack(side=tk.BOTTOM, fill=tk.X)
        self.mainframe.pack(side=tk.TOP, expand=True, fill=tk.BOTH)
