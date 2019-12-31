import tkinter
from tkinter import ttk


class Menubar(ttk.Frame):
    """Builds a menu bar for the top of the main window"""

    def __init__(self, parent, *args, **kwargs):
        ''' Constructor'''
        ttk.Frame.__init__(self, parent, *args, **kwargs)
        self.root = parent
        self.init_menubar()

    def on_exit(self):
        '''Exits program'''
        quit()

    def display_help(self):
        '''Displays help document'''
        pass

    def display_about(self):
        '''Displays info about program'''
        pass

    def init_menubar(self):
        self.menubar = tkinter.Menu(self.root)
        self.menu_file = tkinter.Menu(self.menubar)  # Creates a "File" menu
        self.menu_file.add_command(label='Exit', command=self.on_exit)  # Adds an option to the menu
        self.menubar.add_cascade(menu=self.menu_file,
                                 label='File')  # Adds File menu to the bar. Can also be used to create submenus.

        self.menu_help = tkinter.Menu(self.menubar)  # Creates a "Help" menu
        self.menu_help.add_command(label='Help', command=self.display_help)
        self.menu_help.add_command(label='About', command=self.display_about)
        self.menubar.add_cascade(menu=self.menu_help, label='Help')

        self.root.config(menu=self.menubar)
