#!/usr/bin/env python3.6
# encoding: utf-8
"""
Este módulo é parte integrante da aplicação Promais Service, desenvolvida por
Victor Domingos e distribuída sob os termos da licença Creative Commons
Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)
"""
import tkinter as tk
import tkinter.font
from tkinter import ttk, messagebox
import Pmw

from extra_tk_classes import LabelEntry 
from global_setup import *


class LoginWindow(ttk.Frame):
	""" base class for application """
	def __init__(self,master,*args,**kwargs):
		super().__init__(master,*args,**kwargs)
		self.master = master
		self.master.minsize(LOGIN_MIN_WIDTH, LOGIN_MIN_HEIGHT)
		self.master.maxsize(LOGIN_MAX_WIDTH, LOGIN_MAX_HEIGHT)
		
		self.estilo = ttk.Style()

		self.dicas = Pmw.Balloon(self.master, label_background='#f6f6f6',
											  hull_highlightbackground='#b3b3b3',
											  state='balloon',
											  relmouse='both',
											  yoffset=18,
											  xoffset=-2,
											  initwait=1300)

		self.mainframe = ttk.Frame(master, padding="12 25 12 5")
		self.topframe = ttk.Frame(self.mainframe, padding="5 8 5 5")
		self.centerframe = ttk.Frame(self.mainframe)


		self.bottomframe = ttk.Frame(self.mainframe)
		self.btnFont = tkinter.font.Font(family="Lucida Grande", size=10)
		self.btnTxtColor = "grey22"
		self.btnTxtColor_active = "white"
		
		w = self.master.winfo_screenwidth()
		h = self.master.winfo_screenheight()

		self.size = tuple(int(_) for _ in self.master.geometry().split('+')[0].split('x'))
		self.x = int(w/2 - LOGIN_MIN_WIDTH/2)
		self.y = int(h/3 - LOGIN_MIN_HEIGHT/2)
		#self.master.configure(background='grey92')
		self.master.geometry("{}x{}+{}+{}".format(LOGIN_MIN_WIDTH,LOGIN_MIN_HEIGHT,self.x,self.y))
		self.ltxt_username = LabelEntry(self.centerframe, label="Nome de Utilizador", width=30)
		self.ltxt_password = LabelEntry(self.centerframe, label="Senha", width=30)
		self.ltxt_password.entry.config(show="•")
		self.btn_enter = ttk.Button(self.centerframe, text="Entrar", default="active", style="Active.TButton", command=self.validate_login)
		self.btn_cancel = ttk.Button(self.centerframe, text="Cancelar", command=exit)

		self.btn_alterar_senha = ttk.Button(self.centerframe, text="Alterar senha...", command=self.change_password)
		self.ltxt_username.entry.focus_set()
		self.ltxt_username.pack(side=tk.TOP, expand=False)
		self.ltxt_password.pack(side=tk.TOP, expand=False)
		self.btn_enter.pack(side=tk.RIGHT)
		self.btn_cancel.pack(side=tk.RIGHT)
		self.btn_alterar_senha.pack(side=tk.LEFT)

		self.centerframe.pack(side=tk.TOP, expand=True, fill='both')
		self.mainframe.pack(side=tk.TOP, expand=True, fill='both')


	def validate_login(self):
		print("a validar informação de login...")
		pass

	def change_password(self):
		print("a alterar senha...")
		pass


root = tk.Tk()
login_window = LoginWindow(root)
root.configure(background='grey92')
root.title('Login')
root.bind_all("<Mod2-q>", exit)
root.mainloop()
