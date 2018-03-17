#!/usr/bin/env python3
# encoding: utf-8
"""
Este módulo é parte integrante da aplicação Promais Service, desenvolvida por
Victor Domingos e distribuída sob os termos da licença Creative Commons
Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)
"""

from typing import Dict, List, Union

from local_db import db_models


class DBEvent(object):

    @staticmethod
    def get_messages(session, user_id: int) -> List[Dict[str, Union[int, str]]]:
        """ Obtém lista de dicionários contendo todas as mensagens visíveis, para
            o utilizador atual, para apresentar na janela principal (inclui apenas
            os campos necessários).
        """
        utilizador = session.query(db_models.User).get(user_id)

        msgs = session.query(db_models.UtilizadorNotificadoPorEvento_link) \
            .filter_by(is_visible=1, user=utilizador)

        return [{'evento_id': msg.evento_id,
                 'repair_id': msg.event.repair.id,
                 'remetente_nome': msg.event.criado_por_utilizador.nome,
                 'data': msg.event.created_on,
                 'texto': msg.event.descricao,
                 'estado_msg': msg.is_open}
                for msg in msgs]


    @staticmethod
    def get_event(session, event_id: int) -> Dict[str, Union[int, str]]:
        """ Obtém um dicionário contendo a informação referente a uma mensagem ou
            evento (inclui os campos necessários para preencher a janela de detalhes
            de mensagem/evento).
        """
        evento = session.query(db_models.Event).get(event_id)

        return {'repair_id': evento.repair.id,
                'cliente_nome': evento.repair.cliente.nome,
                'remetente_nome': evento.criado_por_utilizador.nome,
                'artigo': evento.repair.product.descr_product,
                'data': evento.created_on,
                'texto': evento.descricao,
                'estado_atual': evento.repair.estado_reparacao,
                'resultado': evento.repair.cod_resultado_reparacao}
