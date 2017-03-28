#!/usr/bin/env python3.6
# encoding: utf-8
"""
Este módulo é parte integrante da aplicação Promais Service, desenvolvida por
Victor Domingos e distribuída sob os termos da licença Creative Commons
Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)
"""

import os.path
import os
import tkinter as tk
from tkinter import ttk
import tkinter.font

from global_setup import *


__app_name__ = "RepService 2017"
__author__ = "Victor Domingos"
__copyright__ = "Copyright 2017 Victor Domingos"
__license__ = "Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)"
__version__ = "v.0.4 development"
__email__ = "web@victordomingos.com"
__status__ = "Development"


class thanks_window:
    def __init__(self):
        self.about_w = 320
        self.about_h = 370
        os.chdir(os.path.dirname(__file__))
        file_path = os.getcwd() + "/credits.txt"

        self.thanksRoot = tk.Toplevel()
        self.thanksRoot.title("Agradecimentos")
        self.thanksRoot.focus()

        self.thanksRoot.update_idletasks()
        w = self.thanksRoot.winfo_screenwidth()
        h = self.thanksRoot.winfo_screenheight()
        self.size = tuple(int(_) for _ in self.thanksRoot.geometry().split('+')[0].split('x'))
        self.x = int(w/2 - self.about_w/2)
        self.y = int(h/3 - self.about_h/2)
        self.thanksRoot.configure(background='grey92')
        self.thanksRoot.geometry("{}x{}+{}+{}".format(self.about_w,self.about_h,self.x,self.y))
        self.thanksframe = ttk.Frame(self.thanksRoot, padding="10 10 10 10")
        self.thanksframe_bottom = ttk.Frame(self.thanksRoot, padding="10 10 10 10")


        file = open(file_path, "r")
        texto = file.read()
        file.close()
        self.campo_texto = tk.Text(self.thanksframe, height=20)
        self.campo_texto.insert(tk.END, texto)
        self.campo_texto.tag_configure("center", justify='center')
        self.campo_texto.tag_add("center", 1.0, "end")
        self.campo_texto.pack(side=tk.TOP)


        self.close_button = ttk.Button(self.thanksframe_bottom, text="Obrigado!", command=self.thanksRoot.protocol("WM_DELETE_WINDOW"))
        self.close_button.pack()
        self.thanksframe.pack(side=tk.TOP)
        self.thanksframe_bottom.pack(side=tk.BOTTOM)
            
       

class about_window:
    def __init__(self):
        about_w = 320
        about_h = 370

        popupRoot = tk.Toplevel()
        popupRoot.title("")
        popupRoot.focus()

        popupRoot.update_idletasks()
        w = popupRoot.winfo_screenwidth()
        h = popupRoot.winfo_screenheight()
        size = tuple(int(_) for _ in popupRoot.geometry().split('+')[0].split('x'))
        x = int(w/2 - about_w/2)
        y = int(h/3 - about_h/2)
        popupRoot.configure(background='grey92')
        popupRoot.geometry("{}x{}+{}+{}".format(about_w,about_h,x,y))

        pframe_topo = ttk.Frame(popupRoot, padding="10 10 10 2")
        pframe_meio = ttk.Frame(popupRoot, padding="10 2 2 10")
        pframe_fundo = ttk.Frame(popupRoot, padding="10 2 10 10")
        
        os.chdir(os.path.dirname(__file__))
        icon_path = os.getcwd()
        icon_path += "/images/icon.gif"
        icon = tk.PhotoImage(file=icon_path)
        label = ttk.Label(pframe_topo, image=icon)
        label.image = icon
        label.pack(side=tk.TOP)
        label.bind('<Button-1>', thanks)


        appfont = tkinter.font.Font(size=15, weight='bold')
        copyfont = tkinter.font.Font(size=10)
        
        #---------- TOPO -----------
        app_lbl = ttk.Label(pframe_topo, font=appfont, text=__app_name__)
        assin_lbl = ttk.Label(pframe_topo,text="\nO gestor seu avançado de reparações.\n")
        version_lbl = ttk.Label(pframe_topo, font=copyfont, text="Versão {}\n\n\n".format(__version__))

        #---------- MEIO -----------



        #---------- FUNDO -----------
        copyright_lbl = ttk.Label(pframe_fundo, font=copyfont, text="\n\n\n© 2017 Victor Domingos")
        license_lbl = ttk.Label(pframe_fundo, font=copyfont, text=__license__)


        app_lbl.pack()
        assin_lbl.pack()
        version_lbl.pack()


        copyright_lbl.pack()
        license_lbl.pack()
        pframe_topo.pack(side=tk.TOP)
        pframe_meio.pack(side=tk.TOP)
        pframe_fundo.pack(side=tk.TOP)
        
        pframe_topo.focus()

        popupRoot.mainloop()
    
    
     
def thanks(*event):
    janela_thanks = thanks_window()


def about(*event):
    janela_thanks.destroy()
    janela_about = about_window()
    
    