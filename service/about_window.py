#!/usr/bin/env python3.6
# encoding: utf-8
"""
Este módulo é parte integrante da aplicação Promais Service, desenvolvida por
Victor Domingos e distribuída sob os termos da licença Creative Commons
Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)
"""

import tkinter as tk
import tkinter.font
from tkinter import ttk

from global_setup import *


__app_name__ = "RepService 2018"
__author__ = "Victor Domingos"
__copyright__ = "Copyright 2018 Victor Domingos"
__license__ = "Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)"
__version__ = "v0.17 development"
__email__ = "web@victordomingos.com"
__status__ = "Development"


class thanks_window:
    def __init__(self):
        self.about_w = 320
        self.about_h = 370

        self.thanksRoot = tk.Toplevel()
        self.thanksRoot.title("Agradecimentos")

        self.thanksRoot.focus()

        self.thanksRoot.update_idletasks()
        w = self.thanksRoot.winfo_screenwidth()
        h = self.thanksRoot.winfo_screenheight()
        self.size = tuple(
            int(_) for _ in self.thanksRoot.geometry().split('+')[0].split('x'))
        self.x = int(w / 2 - self.about_w / 2)
        self.y = int(h / 3 - self.about_h / 2)
        self.thanksRoot.configure(background='grey92')
        self.thanksRoot.geometry(
            "{}x{}+{}+{}".format(self.about_w, self.about_h, self.x, self.y))
        self.thanksframe = ttk.Frame(self.thanksRoot, padding="10 10 10 10")
        self.thanksframe_bottom = ttk.Frame(
            self.thanksRoot, padding="10 10 10 10")

        self.campo_texto = tk.Text(self.thanksframe, height=20)
        self.campo_texto.insert("end", "\n".join(CREDITS))
        self.campo_texto.tag_configure("center", justify='center')
        self.campo_texto.tag_add("center", 1.0, "end")
        self.campo_texto.pack(side='top')

        self.close_button = ttk.Button(
            self.thanksframe_bottom, text="Obrigado!", command=self.thanksRoot.destroy)
        self.close_button.pack()
        self.thanksframe.pack(side=tk.TOP)
        self.thanksframe_bottom.pack(side=tk.BOTTOM)
        self.thanksRoot.bind("<Command-w>", self.close_window)

    def close_window(self, event):
        window = event.widget.winfo_toplevel()
        window.destroy()
        return "break"


class about_window:
    def __init__(self, *event):
        self.about_w = 320
        self.about_h = 370

        self.popupRoot = tk.Toplevel()
        self.popupRoot.title("")

        self.popupRoot.focus()

        self.popupRoot.update_idletasks()
        w = self.popupRoot.winfo_screenwidth()
        h = self.popupRoot.winfo_screenheight()
        size = tuple(int(_)
                     for _ in self.popupRoot.geometry().split('+')[0].split('x'))
        x = int(w / 2 - self.about_w / 2)
        y = int(h / 3 - self.about_h / 2)
        self.popupRoot.configure(background='grey92')
        self.popupRoot.geometry(
            "{}x{}+{}+{}".format(self.about_w, self.about_h, x, y))

        self.pframe_topo = ttk.Frame(self.popupRoot, padding="10 10 10 2")
        self.pframe_meio = ttk.Frame(self.popupRoot, padding="10 2 2 10")
        self.pframe_fundo = ttk.Frame(self.popupRoot, padding="10 2 10 10")

        icon_path = APP_PATH + "/images/icon.gif"
        self.icon = tk.PhotoImage(file=icon_path)
        self.label = ttk.Label(self.pframe_topo, image=self.icon)
        self.label.pack(side='top')
        self.label.bind('<Button-1>', thanks)

        self.appfont = tkinter.font.Font(size=15, weight='bold')
        self.copyfont = tkinter.font.Font(size=10)

        #---------- TOPO -----------
        self.app_lbl = ttk.Label(
            self.pframe_topo, font=self.appfont, text=__app_name__)
        self.assin_lbl = ttk.Label(
            self.pframe_topo, text="\nO seu gestor avançado de reparações.\n")
        self.version_lbl = ttk.Label(
            self.pframe_topo, font=self.copyfont, text="Versão {}\n\n\n".format(__version__))

        #---------- MEIO -----------

        #---------- FUNDO -----------
        self.copyright_lbl = ttk.Label(
            self.pframe_fundo, font=self.copyfont, text="\n\n\n© 2018 Victor Domingos")
        self.license_lbl = ttk.Label(
            self.pframe_fundo, font=self.copyfont, text=__license__)

        self.app_lbl.pack()
        self.assin_lbl.pack()
        self.version_lbl.pack()

        self.copyright_lbl.pack()
        self.license_lbl.pack()
        self.pframe_topo.pack(side=tk.TOP)
        self.pframe_meio.pack(side=tk.TOP)
        self.pframe_fundo.pack(side=tk.TOP)

        self.pframe_topo.focus()
        self.popupRoot.bind("<Command-w>", self.close_window)


    def close_window(self, event):
        window = event.widget.winfo_toplevel()
        window.destroy()
        return "break"


def thanks(*event):
    janela_thanks = thanks_window()


def about(*event):
    janela_thanks.destroy()
    janela_about = about_window()
