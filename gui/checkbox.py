from tkinter import *


class Checkbar(Frame):

    def __init__(self, parent=None, picks=[], side=LEFT, anchor=W, callback=None):
        Frame.__init__(self, parent)
        self.vars = []
        self.checks = []
        row=2
        col=2
        for pick in picks:
            var = IntVar()
            check_button = Checkbutton(self, text=pick, variable=var, command=callback)
            #chk = Checkbutton(self, text=pick, variable=var)
            #chk.pack(side=side, anchor=anchor, expand=YES)
            check_button.grid(sticky="W",row=row, column=col)
            self.grid_rowconfigure(row, minsize=90)
            self.vars.append(var)
            self.checks.append(check_button)
            row=row+50

    def state(self):
        return map((lambda var: var.get()), self.vars)

    def get_checkbar_state(self):
        return self.checks,self.vars

    def get_checks(self):
        return self.checks

    def get_vars(self):
        return self.vars




