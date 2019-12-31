import tkinter as tk

from gui.checkbox import Checkbar
from gui.utils.helper_methods import load_anomaly_detection_list


class AlgorithmsWindow(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # Create Widgets
        self.algorithms_title = tk.Label(self, text="Choose anomaly detection algorithms", font=controller.title_font)

        self.anomaly_detection_methods = Checkbar(self, load_anomaly_detection_list())

        self.back_button = tk.Button(self, text="Back to menu",
                                     command=lambda: controller.show_frame("MainWindow"))

        self.next_button = tk.Button(self, text="Next",
                                     command=lambda: controller.show_frame("FeatureSelectionWindow"))

        # Layout using grid
        self.algorithms_title.grid(row=0, column=2, pady=3)
        self.anomaly_detection_methods.grid(row=2, column=2, pady=3)

        self.back_button.grid(row=15, column=0, pady=3)
        self.next_button.grid(row=15, column=3, pady=3)
