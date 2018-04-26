from typing import Dict, List, Union

from sqlalchemy import or_, and_

from local_db import db_models
from local_db import db_main as db
from misc.constants import ESTADOS, PRIORIDADES
from misc.misc_funcs import calcular_dias_desde, clean_data, clean_data_field_txt, clean_data_field_int


class DBRepair(object):

    def save_repair(self, session, repair) -> int:
        print("a guardar o processo de reparação", repair)
        new_repair = db_models.Repair(**repair)
        session.add(new_repair)
        session.commit()
        return new_repair.id


    def update_repair_status(self, session, rep_num: int, status: int):
        print(f"A atualizar o estado da reparação nº {rep_num}: {status} ({ESTADOS[status]})")
        reparacao = self.get_repair(session, rep_num)
        pass  # TODO atualizar reparacao com novo estado.


    def update_repair_priority(self, session, rep_num, priority):
        print(
            f"A atualizar a prioridade da reparação nº {rep_num}: {priority} ({PRIORIDADES[priority]})")
        reparacao = self._get_repair(session, rep_num)
        pass  # TODO atualizar reparacao com prioridade.


    @staticmethod
    def count_repairs(session):
        return session.query(db_models.Repair).count()


    @staticmethod
    def get_all_repairs(session) -> List[Dict[str, Union[int, str]]]:
        """ Obtém lista de dicionários contendo todas as reparações, para preencher
            a tabela principal (inclui apenas os campos necessários).
        """
        reps = [{'id': rep.id,
                 'cliente_nome': rep.cliente.nome,
                 'descr_artigo': rep.descr_product,
                 'sn': rep.sn,
                 'descr_servico': rep.descr_servico,
                 'estado': rep.estado_reparacao,
                 'dias': calcular_dias_desde(rep.created_on),
                 'prioridade': rep.prioridade}
                for rep in session.query(db_models.Repair)]

        return reps


    @staticmethod
    def get_repairs_by_status(session, status_list: List[int]) -> List[Dict[str, Union[int, str]]]:
        """ Obtem lista de dicionários contendo todas as reparações que se
            encontram num dado estado, para preencher a tabela principal (inclui
            apenas os campos necessários).
        """
        if not status_list:
            return obter_todas_reparacoes()

        reparacoes = session.query(db_models.Repair) \
            .filter(db_models.Repair.estado_reparacao.in_(status_list))

        reps = [{'id': rep.id,
                 'nome': rep.fornecedor.nome,
                 'descr_artigo': rep.descr_product,
                 'sn': rep.sn,
                 'descr_servico': rep.descr_servico,
                 'estado': rep.estado_reparacao,
                 'dias': calcular_dias_desde(rep.created_on),
                 'prioridade': rep.prioridade}
                if rep.is_stock
                else {'id': rep.id,
                      'nome': rep.cliente.nome,
                      'descr_artigo': rep.descr_product,
                      'sn': rep.sn,
                      'descr_servico': rep.descr_servico,
                      'estado': rep.estado_reparacao,
                      'dias': calcular_dias_desde(rep.created_on),
                      'prioridade': rep.prioridade}
                for rep in reparacoes
                ]

        return reps


    @staticmethod
    def get_repairs_by_contact(session, contact_id: int) -> List[Dict[str, Union[int, str]]]:
        """ Obtem lista de dicionários contendo todas as reparações relacionadas
            com um determinado contacto (cliente ou fornecedor), para preencher a
            tabela do separador Reparações na janela de detalhes de contacto
            (inclui apenas os campos necessários).
        """
        reparacoes = session.query(db_models.Repair) \
            .filter(or_(db_models.Repair.cliente_id == contact_id,
                        db_models.Repair.fornecedor_id == contact_id))

        reps = [{'id': rep.id,
                 'data': rep.created_on,
                 'descr_artigo': rep.descr_product,
                 'descr_servico': rep.descr_servico,
                 'resultado': rep.cod_resultado_reparacao,
                 'reincidencia_id': rep.reincidencia_processo_id}
                for rep in reparacoes]

        return reps


    @staticmethod
    def search_repairs(session, txt_pesquisa: str, estados: List[int] = None) -> List[
        Dict[str, Union[int, str]]]:
        """ Obtem lista de dicionários contendo todas as reparações que se
            correspondem ao termos de pesquisa indicado e que se encontram num
            dado estado, para preencher a tabela principal (inclui apenas os
            campos necessários). Para permitir um melhor desempenho, apenas é
            mostrada uma parte dos registos.
        """
        if estados is None:
            estados = []

        termo_pesquisa = txt_pesquisa

        for c in txt_pesquisa:
            if c in "1234567890.":
                numeric = True
            else:
                numeric = False
                break

        if not numeric:
            if '*' in txt_pesquisa or '_' in txt_pesquisa or '?' in txt_pesquisa:
                termo_pesquisa = txt_pesquisa.replace('_', '__').replace('*', '%').replace('?', '_')
            else:
                termo_pesquisa = f"%{txt_pesquisa}%"

        reps = session.query(db_models.Repair, db_models.Contact) \
                   .filter(db_models.Repair.cliente_id == db_models.Contact.id) \
                   .filter(and_(db_models.Repair.estado_reparacao.in_(estados),
                                or_(
                                    db_models.Repair.id.like(termo_pesquisa),
                                    db_models.Contact.nome.ilike(termo_pesquisa),
                                    db_models.Contact.telefone.ilike(termo_pesquisa),
                                    db_models.Contact.telemovel.ilike(termo_pesquisa),
                                    db_models.Contact.email.ilike(termo_pesquisa),
                                    db_models.Repair.descr_product.ilike(termo_pesquisa),
                                    db_models.Repair.part_number.ilike(termo_pesquisa),
                                    db_models.Repair.descr_servico.ilike(termo_pesquisa),
                                    db_models.Repair.notas.ilike(termo_pesquisa),
                                    db_models.Repair.num_fatura.ilike(termo_pesquisa),
                                    db_models.Repair.sn.ilike(termo_pesquisa)
                                ))) \
                   .order_by(db_models.Repair.created_on)[:3000]

        #TODO: verificar se não é necessário ajustar para reparação de stock/cliente.

        return [clean_data({'id': rep[0].id,
                 'cliente_nome': rep[1].nome,
                 'descr_artigo': rep[0].descr_product,
                 'sn': rep[0].sn,
                 'descr_servico': rep[0].descr_servico,
                 'estado': rep[0].estado_reparacao,
                 'dias': calcular_dias_desde(rep[0].created_on),
                 'prioridade': rep[0].prioridade})
                for rep in reps]


    @staticmethod
    def _get_repair(session, num_rep: int):
        """ Returns a Repair object."""
        return session.query(db_models.Repair).get(num_rep)


    def get_repair(self, session, num_rep: int) -> Dict[str, Union[int, str]]:
        """ Obtém um dicionário contendo a informação referente a uma reparação
                (inclui os campos necessários para preencher a janela de detalhes
                de reparação).
            """

        rep = self._get_repair(session, num_rep)

        # TODO: verificar se é mesmo preciso fazer este tipo de validção de dados aqui,
        # ou se é melhor fazer de outro modo noutro local.
        if not rep:
            return {'id': 0}

        if rep.is_stock:
            rep_data = clean_data(
               {'id': rep.id,
                'cliente_id': 0,
                'cliente_nome': "",
                'cliente_telefone': "",
                'cliente_email': "",
                'product_descr': clean_data_field_txt(rep.descr_product),
                'product_part_number': clean_data_field_txt(rep.part_number),
                'sn': clean_data_field_txt(rep.sn),
                'fornecedor_id': clean_data_field_int(rep.fornecedor.id),
                'fornecedor_nome': clean_data_field_txt(rep.fornecedor.nome),
                'fornecedor_telefone': rep.fornecedor.telefone,
                'fornecedor_email': rep.fornecedor.email,
                'estado_artigo': rep.estado_artigo,
                'obs_estado': clean_data_field_txt(rep.obs_estado),
                'is_garantia': rep.is_garantia,
                'data_compra': rep.data_compra,
                'num_fatura': clean_data_field_txt(rep.num_fatura),
                'loja_compra': clean_data_field_txt(rep.loja_compra),
                'descr_servico': clean_data_field_txt(rep.descr_servico),
                'avaria_reprod_loja': rep.avaria_reprod_loja,
                'requer_copia_seg': rep.requer_copia_seg,
                'is_find_my_ativo': rep.is_find_my_ativo,
                'senha': clean_data_field_txt(rep.senha),
                'acessorios_entregues': clean_data_field_txt(rep.acessorios_entregues),
                'notas': clean_data_field_txt(rep.notas),
                'local_reparacao_id': clean_data_field_int(rep.local_reparacao_id),
                'local_reparacao_nome': db.obter_contacto(rep.local_reparacao_id)['nome'],
                'estado_reparacao': rep.estado_reparacao,
                'fatura_fornecedor': clean_data_field_txt(rep.fatura_fornecedor),
                'nar_autorizacao_rep': clean_data_field_txt(rep.nar_autorizacao_rep),
                'data_fatura_fornecedor': rep.data_fatura_fornecedor,
                'num_guia_rececao': clean_data_field_txt(rep.num_guia_rececao),
                'data_guia_rececao': rep.data_guia_rececao,
                'cod_resultado_reparacao': rep.cod_resultado_reparacao,
                'descr_detalhe_reparacao': clean_data_field_txt(rep.descr_detalhe_reparacao),
                'novo_sn_artigo': clean_data_field_txt(rep.novo_sn_artigo),
                'notas_entrega': clean_data_field_txt(rep.notas_entrega),
                'utilizador_entrega_id': clean_data_field_int(rep.utilizador_entrega_id),
                'data_entrega': clean_data_field_txt(rep.data_entrega),
                'num_quebra_stock': clean_data_field_txt(rep.num_quebra_stock),
                'is_rep_stock': rep.is_stock,
                'is_rep_cliente': not rep.is_stock,
                'modo_entrega': rep.modo_entrega,
                'cliente_pagou_portes': rep.cliente_pagou_portes,
                'reincidencia_processo_id': clean_data_field_int(rep.reincidencia_processo_id),
                'morada_entrega': clean_data_field_txt(rep.morada_entrega),
                'prioridade': rep.prioridade,
                'criado_por_utilizador_id': rep.criado_por_utilizador_id,
                'ult_atualizacao_por_utilizador_id': clean_data_field_int(rep.ult_atualizacao_por_utilizador_id),

                'created_on': rep.created_on.isoformat(sep=' ', timespec='minutes'),
                'updated_on': rep.updated_on.isoformat(sep=' ', timespec='minutes'),

                'utilizador_entrega': clean_data_field_int(rep.utilizador_entrega_id),
                'criado_por_utilizador': rep.criado_por_utilizador_id,
                'atualizado_por_utilizador': clean_data_field_int(rep.ult_atualizacao_por_utilizador_id),
                })
        else:
            rep_data = clean_data(
               {'id': rep.id,
                'cliente_id': clean_data_field_int(rep.cliente.id),
                'cliente_nome': clean_data_field_txt(rep.cliente.nome),
                'cliente_telefone': clean_data_field_txt(rep.cliente.telefone),
                'cliente_email': clean_data_field_txt(rep.cliente.email),
                'product_descr': clean_data_field_txt(rep.descr_product),
                'product_part_number': clean_data_field_txt(rep.part_number),
                'sn': clean_data_field_txt(rep.sn),
                'fornecedor_id': 0,
                'fornecedor_nome': "",
                'estado_artigo': rep.estado_artigo,
                'obs_estado': clean_data_field_txt(rep.obs_estado),
                'is_garantia': rep.is_garantia,
                'data_compra': rep.data_compra,
                'num_fatura': clean_data_field_txt(rep.num_fatura),
                'loja_compra': clean_data_field_txt(rep.loja_compra),
                'descr_servico': clean_data_field_txt(rep.descr_servico),
                'avaria_reprod_loja': rep.avaria_reprod_loja,
                'requer_copia_seg': rep.requer_copia_seg,
                'is_find_my_ativo': rep.is_find_my_ativo,
                'senha': clean_data_field_txt(rep.senha),
                'acessorios_entregues': clean_data_field_txt(rep.acessorios_entregues),
                'notas': clean_data_field_txt(rep.notas),
                'local_reparacao_id': clean_data_field_int(rep.local_reparacao_id),
                'local_reparacao_nome': db.obter_contacto(rep.local_reparacao_id)['nome'],
                'estado_reparacao': rep.estado_reparacao,
                'fatura_fornecedor': clean_data_field_txt(rep.fatura_fornecedor),
                'nar_autorizacao_rep': clean_data_field_txt(rep.nar_autorizacao_rep),
                'data_fatura_fornecedor': rep.data_fatura_fornecedor,
                'num_guia_rececao': clean_data_field_txt(rep.num_guia_rececao),
                'data_guia_rececao': rep.data_guia_rececao,
                'cod_resultado_reparacao': rep.cod_resultado_reparacao,
                'descr_detalhe_reparacao': clean_data_field_txt(rep.descr_detalhe_reparacao),
                'novo_sn_artigo': clean_data_field_txt(rep.novo_sn_artigo),
                'notas_entrega': clean_data_field_txt(rep.notas_entrega),
                'utilizador_entrega_id': clean_data_field_int(rep.utilizador_entrega_id),
                'data_entrega': clean_data_field_txt(rep.data_entrega),
                'num_quebra_stock': clean_data_field_txt(rep.num_quebra_stock),
                'is_rep_stock': rep.is_stock,
                'is_rep_cliente': not rep.is_stock,
                'modo_entrega': rep.modo_entrega,
                'cliente_pagou_portes': rep.cliente_pagou_portes,
                'reincidencia_processo_id': clean_data_field_int(rep.reincidencia_processo_id),
                'morada_entrega': clean_data_field_txt(rep.morada_entrega),
                'prioridade': rep.prioridade,
                'criado_por_utilizador_id': rep.criado_por_utilizador_id,
                'ult_atualizacao_por_utilizador_id': clean_data_field_int(rep.ult_atualizacao_por_utilizador_id),

                'created_on': rep.created_on.isoformat(sep=' ', timespec='minutes'),
                'updated_on': rep.updated_on.isoformat(sep=' ', timespec='minutes'),

                'utilizador_entrega': clean_data_field_int(rep.utilizador_entrega_id),
                'criado_por_utilizador': rep.criado_por_utilizador_id,
                'atualizado_por_utilizador': clean_data_field_int(rep.ult_atualizacao_por_utilizador_id),
                }
                )

        return rep_data



    def get_serial_number(self, session, num_rep: int) -> str:
        rep = self._get_repair(session, num_rep)
        return rep.sn
