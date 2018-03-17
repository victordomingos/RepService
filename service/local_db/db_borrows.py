#!/usr/bin/env python3
# encoding: utf-8
"""
Este módulo é parte integrante da aplicação Promais Service, desenvolvida por
Victor Domingos e distribuída sob os termos da licença Creative Commons
Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)
"""


class DBBorrow(object):

    def get_products_to_borrow_list(self, session):
        """ Devolve um dicionário em que as chaves correspondem ao ID de artigo, sendo
            o artigo definido através de uma tupla que contém a descrição e o número de
            série.
        """
        print("A obter lista atualizada de artigos de empréstimo. ")
        # TODO:
        artigos = {"12234": ("iPhone 7 128GB Space grey", ""),
                   "85738": ("MacBook Pro 15\" Retina", ""),
                   "32738": ("iPod shuffle 2GB", ""),
                   "25720": ("Beats X", "XWD45123456PTXCH"),
                   "85737": ("MacBook Pro 15\" Retina", ""),
                   "32736": ("iPod shuffle 2GB", ""),
                   "25725": ("Beats X - NPK - Network Project for Knowledge", ""),
                   "85734": ("MacBook Pro 15\" Retina", ""),
                   "32733": ("iPod shuffle 2GB", ""),
                   "25722": ("Beats X - NPK - Network Project for Knowledge", ""),
                   "85731": ("MacBook Pro 15\" Retina", "XWD45123456PTXCH"),
                   "32730": ("iPod shuffle 2GB", "WXBG23123GB654P"),
                   "25729": ("Beats X - NPK - Network Project for Knowledge", "")
                   }
        return artigos
