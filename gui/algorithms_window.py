import time
import tkinter as tk
import tkinter.ttk as ttk
from functools import partial

from gui.checkbox import Checkbar
from gui.lstm_frame_option import lstm_frame_option
from gui.utils.helper_methods import load_anomaly_detection_list


class AlgorithmsWindow(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller

        # Create Widgets
        self.algorithms_title = tk.Label(self, text="Choose anomaly detection algorithms", font=controller.title_font)

        self.anomaly_detection_methods = Checkbar(self, load_anomaly_detection_list(), callback=self.show_algorithms_options)

        self.back_button = tk.Button(self, text="Back to menu",
                                     command=lambda: controller.show_frame("MainWindow"))

        self.next_button = tk.Button(self, text="Next",
                                      command=lambda: controller.show_frame("FeatureSelectionWindow"))

        # Layout using grid
        self.algorithms_title.grid(row=0, column=2, pady=3)
        self.anomaly_detection_methods.grid(row=2, column=2, pady=3)
        #self.grid_columnconfigure(1,minsize= 9)


        #self.grid_rowconfigure(14, minsize=100)
        self.back_button.grid(row=50, column=2, pady=3)
        self.next_button.grid(row=50, column=15, pady=3)

        self.algorithms_options_to_show = {}
        self.algorithms_options_to_show["LSTM"] = lstm_frame_option(self)

    def show_algorithms_options(self):
        row=1
        col=50
        for check, var in zip(self.anomaly_detection_methods.get_checks(),
                            self.anomaly_detection_methods.get_vars()):
            algorithm_name = check.cget("text")
            if algorithm_name != "LSTM":
                continue
            parameters = self.algorithms_options_to_show[algorithm_name].get_algorithm_parameters()
            if var.get(): #show the algorithms options
                self.algorithms_options_to_show[algorithm_name].grid(row=row, column=col)
                self.set_algorithm_parameters(algorithm_name,parameters)
            else:
                self.algorithms_options_to_show[algorithm_name].grid_remove()
                self.remove_algorithm_parameters(algorithm_name,parameters)
            row = row*15

    def set_algorithm_parameters(self,algorithm_name,algorithm_parameters):
        self.controller.set_algorithm_parameters(algorithm_name,algorithm_parameters)

    def remove_algorithm_parameters(self,algorithm_name,algorithm_parameters):
        self.controller.remove_algorithm_parameters(algorithm_name,algorithm_parameters)

