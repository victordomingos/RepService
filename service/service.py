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
from tkinter import ttk

from global_setup import *
from gui.base_app import AppStatus
from gui.main_window import App


if __name__ == "__main__":
    estado_app = AppStatus()
    root = tk.Tk()
    estado_app.janela_principal = App(root, estado_app)
    estilo_global = ttk.Style(root)
    estilo_global.theme_use(ESTILO_APP)
    # estilo_global.theme_use("clam")
    root.configure(background='grey95')
    root.title('RepService')
    root.geometry(ROOT_GEOMETRIA)
    root.bind_all("<Mod2-q>", root.quit)

    root.mainloop()
