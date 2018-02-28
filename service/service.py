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
import tkinter as tk
from tkinter import ttk

from gui.base_app import AppStatus
from gui.main import App
from global_setup import *


if __name__ == "__main__":
    estado_app = AppStatus()
    root = tk.Tk()
    estado_app.janela_principal = App(root, estado_app)
    estilo_global = ttk.Style(root)
    estilo_global.theme_use(ESTILO_APP)
    #estilo_global.theme_use("default")
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
