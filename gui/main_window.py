import tkinter as tk
from gui.menubar import Menubar


class MainWindow(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.menubar = Menubar(controller)

        controller.title('Anomaly Detection Classifier')
        controller.geometry('500x200')
        controller.option_add('*tearOff', 'FALSE')  # Disables ability to tear menu bar into own window

        label = tk.Label(self, text="Anomaly Detection Classifier", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10, padx=30)

        button1 = tk.Button(self, text="New model", pady=5, padx=5,
                            command=lambda: controller.show_frame("NewModel"))
        button2 = tk.Button(self, text="Load existing model", pady=5, padx=5,
                            command=lambda: controller.show_frame("LoadModel"))

        button1.pack(side="left", fill="x", pady=10, padx=50)
        button2.pack(side="right", fill="x", pady=10, padx=50)
