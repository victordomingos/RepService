#!/usr/bin/env python3
# encoding: utf-8
"""
Este módulo é parte integrante da aplicação RepService, desenvolvida por
Victor Domingos e distribuída sob os termos da licença Creative Commons
Attribution-ShareAlike 4.0 International (CC BY-SA 4.0). Contém partes
desenvolvidas inicialmente por terceiros, conforme indicado ao longo do
código.
"""

import tkinter as tk
import tkinter.font

from tkinter import ttk
from tkinter.scrolledtext import ScrolledText

from tkcalendar import Calendar


class DatePicker(ttk.Labelframe):
    def __init__(self, master, target=None):
        self.target = target
        ttk.Labelframe.__init__(self, master, width=180, height=130, labelwidget=ttk.Separator(),
                                labelanchor='s')

        self.cal = Calendar(self,
                       font="Helvetica 11",
                       locale="pt_PT",
                       selectforeground="Blue",
                       othermonthforeground="Gray80",
                       othermonthweforeground="Gray85",
                       normalforeground="Gray30",  # Cor dos números dos dias do mês selecionado
                       headersforeground="Royalblue2",
                       # Dias da semana (cabeçalho) e números de semana (coluna da esquerda)
                       cursor="hand2",
                       background="LightGray",  # Botões com setas, no cabeçalho
                       foreground="Gray",  # Mês e ano no cabeçalho
                       selectbackground="White",
                       weekendforeground="medium purple",
                       headersbackground="DarkGray",
                       borderwidth=3,
                       # selectmode="day",  # ou "none", em alternativa
                       # year=2018,
                       # month=1,
                       # day=1
                      )

        self.cal.pack(fill=None, expand=False)
        self.cal.bind("<<CalendarSelected>>", self.select_date)


    def show(self, *event):
        if self.target.calendar_open:
            return
        self.target.calendar_open = True
        self.focus()
        self.target.bind("<FocusOut>", lambda x: self.close_calendar)
        self.place(in_=self.target, relx=0, rely=1, width=210, height=148, anchor='nw')
        self.cal.focus()
        self.after_id = self.after(15000, self.close_calendar)

    def close_calendar(self):
        self.target.calendar_open = False
        self.target.unbind("<FocusOut>")
        # self.after_cancel(self.after_id)
        self.place_forget()

    def select_date(self, event):
        data = self.cal.selection_get()
        self.target.set(str(data))
        self.close_calendar()


class AutocompleteEntry(ttk.Entry):
    """
    Subclass of tkinter.Entry that features autocompletion.
    To enable autocompletion use set_completion_list(list) to define
    a list of possible strings to hit.
    To cycle through hits use down and up arrow keys.

    Created by Mitja Martini on 2008-11-29.
    Converted to Python3 by Ian Weisser on 2014-04-06.
    Edited by Victor Domingos on 2016-04-25.

    https://gist.github.com/victordomingos/3a2a143c573e49308aad392acff25b47
    """

    def set_completion_list(self, completion_list):
        self._completion_list = completion_list
        self._hits = []
        self._hit_index = 0
        self.position = 0
        self.bind('<KeyRelease>', self.handle_keyrelease)

    def autocomplete(self, delta=0):
        """autocomplete the Entry, delta may be 0/1/-1 to cycle through possible hits"""
        if delta:  # need to delete selection otherwise we would fix the current position
            self.delete(self.position, tk.END)
        else:  # set position to end so selection starts where textentry ended
            self.position = len(self.get())
        # collect hits
        _hits = []
        for element in self._completion_list:
            if element.lower().startswith(self.get().lower()):
                _hits.append(element)
        # if we have a new hit list, keep this in mind
        if _hits != self._hits:
            self._hit_index = 0
            self._hits = _hits
        # only allow cycling if we are in a known hit list
        if _hits == self._hits and self._hits:
            self._hit_index = (self._hit_index + delta) % len(self._hits)
        # now finally perform the auto completion
        if self._hits:
            self.delete(0, tk.END)
            self.insert(0, self._hits[self._hit_index])
            self.select_range(self.position, tk.END)

    def handle_keyrelease(self, event):
        """event handler for the keyrelease event on this widget"""
        if event.keysym == "BackSpace":
            if self.position < self.index(tk.END):  # delete the selection
                self.delete(self.position, tk.END)
            else:
                self.position = self.index(tk.END)
        if event.keysym == "Left":
            if self.position < self.index(tk.END):  # delete the selection
                self.delete(self.position, tk.END)
        if event.keysym == "Right":
            self.position = self.index(tk.END)  # go to end (no selection)
        if event.keysym == "Down":
            self.autocomplete(1)  # cycle to next hit
        if event.keysym == "Up":
            self.autocomplete(-1)  # cycle to previous hit
        # perform normal autocomplete if event is a single key
        if len(event.keysym) == 1:
            self.autocomplete()


class AutoScrollbar(ttk.Scrollbar):
    """
     a scrollbar that hides itself if it's not needed.  only
     works if you use the grid geometry manager.
     http://effbot.org/zone/tkinter-autoscrollbar.htm
    """

    def set(self, lo, hi):
        if float(lo) <= 0.0 and float(hi) >= 1.0:
            # grid_remove is currently missing from Tkinter!
            #self.tk.call("grid", "remove", self)
            self.grid_remove()
        else:
            self.grid()
        ttk.Scrollbar.set(self, lo, hi)

    def pack(self, **kw):
        raise tk.TclError("cannot use pack with this widget")

    def place(self, **kw):
        raise tk.TclError("cannot use place with this widget")


class LabelEntry(ttk.Frame):
    """
    Generate a ttk.Entry form field with a text label above it.
    """

    def __init__(self, parent, label, default_text="", style=None, width=0):
        ttk.Frame.__init__(self, parent)
        self.calendar_open = False

        if style:
            self.label = ttk.Label(self, text=label, style=style, anchor="w")
        else:
            self.label = ttk.Label(self, text=label, anchor="w")

        self.entry = ttk.Entry(self, font=("Helvetica-Neue", 12), width=width)
        self.entry.insert(0, default_text)

        self.label.pack(side="top", fill="x", expand=True)
        self.entry.pack(side="top", fill="x", expand=True)

    def clear(self):
        self.entry.delete(0, 'end')

    def get(self):
        return self.entry.get()

    def set(self, text):
        self.clear()
        self.entry.insert(0, text)

    def set_label(self, text):
        self.label.config(text=text)

    def disable(self):
        self.entry.configure(state="disabled")

    def enable(self):
        self.entry.configure(state="enabled")


class LabelText(ttk.Frame):
    """
    Generate an empty tkinter.scrolledtext form field with a text label above it.
    """

    def __init__(self, parent, label, style=None, width=0, height=0):
        ttk.Frame.__init__(self, parent)
        if style:
            self.label = ttk.Label(self, text=label, style=style, anchor="w")
        else:
            self.label = ttk.Label(self, text=label, anchor="w")

        self.scrolledtext = ScrolledText(self, font=("Helvetica-Neue", 12),
                                         highlightcolor="LightSteelBlue2",
                                         wrap='word',
                                         width=width,
                                         height=height)

        self.label.pack(side="top", fill="x", expand=False)
        self.scrolledtext.pack(side="top", fill="both", expand=True)

    def get(self):
        return self.scrolledtext.get(1.0, tk.END)

    def set(self, text):
        self.clear()
        self.scrolledtext.insert('insert', text)

    def clear(self):
        self.scrolledtext.delete('1.0', 'end')

    def set_label(self, text):
        self.label.config(text=text)

    def enable(self):
        self.scrolledtext.configure(state="enabled", bg="white")

    def disable(self):
        self.scrolledtext.configure(state="disabled",
                                    bg="#fafafa",
                                    highlightbackground="#fafafa",
                                    highlightthickness=1)


class StatusBar(ttk.Frame):
    """ Simple Status Bar class.
    """
    def __init__(self, master):
        ttk.Frame.__init__(self, master)
        self.right_frame = ttk.Frame(self)
        self.center_frame = ttk.Frame(self)
        self.left_frame = ttk.Frame(self)

        self.lblStatusColor = "grey22"
        self.statusFont = tkinter.font.Font(family="Lucida Grande", size=11)
        self.label = ttk.Label(
            self.center_frame, anchor=tk.W, font=self.statusFont, foreground=self.lblStatusColor)

        self.progress_bar = ttk.Progressbar(self.right_frame,
                                            length=100,
                                            mode='indeterminate')

        self.label.pack()

        self.left_frame.grid(row=1, column=0, sticky='w')
        self.center_frame.grid(row=1, column=1, sticky='we')
        self.right_frame.grid(row=1, column=2, sticky='e')
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=6)
        self.grid_columnconfigure(2, weight=1)

        self.pack(side=tk.BOTTOM, fill=tk.X)

    def set(self, texto):
        self.label.config(text=texto)
        self.label.update_idletasks()

    def clear(self):
        self.label.config(text="")
        self.label.update_idletasks()

    def show_progress(self, maximum_value=100):
        self.progress_bar.pack(side='right', padx="0 14")
        #if maximum_value:
        #    self.progress_bar['maximum'] = maximum_value
        self.progress_bar.start()
        self.progress_bar.update()
        self.right_frame.grid()
        self.left_frame.grid()
        self.master.update()

    def hide_progress(self):
        self.progress_bar.stop()
        #self.progress_bar.destroy()
        self.left_frame.grid_remove()
        self.right_frame.grid_remove()


    def progress_set(self, value=1):
        self.progress_bar['value'] = value
        self.progress_bar.update()


    def progress_reset(self, value):
        self.progress_bar['value'] = 0
        self.progress_bar.update()


'''
class StatusBar(ttk.Frame):
    """ Simple Status Bar class - based on ttk.Frame """
    def __init__(self, master):
        ttk.Frame.__init__(self, master)
        self.lblStatusColor = "grey22"
        self.statusFont = tkinter.font.Font(family="Lucida Grande", size=11)
        self.label = ttk.Label(
            self, anchor=tk.W, font=self.statusFont, foreground=self.lblStatusColor)
        self.label.pack()
        self.pack(side=tk.BOTTOM, fill=tk.X)

    def set(self, texto):
        self.label.config(text=texto)
        self.label.update_idletasks()

    def clear(self):
        self.label.config(text="")
        self.label.update_idletasks()
'''