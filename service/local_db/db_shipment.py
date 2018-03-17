#!/usr/bin/env python3
# encoding: utf-8
"""
Este módulo é parte integrante da aplicação Promais Service, desenvolvida por
Victor Domingos e distribuída sob os termos da licença Creative Commons
Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)
"""


class DBShipment(object):

    def save_shipment(self, session, shipment: int) -> int:
        print("a guardar a remessa", remessa)
        db_last_remessa_number = 1984
        return db_last_remessa_number


    def get_processes_to_receive_list(self, session):
        print(
            "A obter lista atualizada de processos de reparação que falta receber dos fornecedores e/ou centros técnicos.")
        # TODO:
        lista = ["12234 - iPhone 7 128GB Space grey - José manuel da Silva Castro",
                 "85738 - MacBook Pro 15\" Retina - Manuel José de Castro Silva",
                 "32738 - iPod shuffle 2GB - Laranjas e Limões, Lda.",
                 "25720 - Beats X - NPK - Network Project for Knowledge",
                 "85738 - MacBook Pro 15\" Retina - Manuel José de Castro Silva",
                 "32738 - iPod shuffle 2GB - Laranjas e Limões, Lda."]

        return lista


    def get_processes_to_send_list(self, session):
        print(
            "A obter lista atualizada de processos de reparação que falta enviar para os "
            "fornecedores e/ou centros técnicos.")
        # TODO:
        lista = ["12234 - iPhone 7 128GB Space grey - José manuel da Silva Castro",
                 "85738 - MacBook Pro 15\" Retina - Manuel José de Castro Silva",
                 "32738 - iPod shuffle 2GB - Laranjas e Limões, Lda.",
                 "25720 - Beats X - NPK - Network Project for Knowledge",
                 "85738 - MacBook Pro 15\" Retina - Manuel José de Castro Silva",
                 "32738 - iPod shuffle 2GB - Laranjas e Limões, Lda."]

        return lista


    @staticmethod
    def count_shipments(session):
        return 0  # TODO
