import tkinter as tk

from gui.checkbox import Checkbar
from gui.utils.helper_methods import load_feature_selection_list


class FeatureSelectionWindow(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # Create Widgets
        self.feature_selection_title = tk.Label(self, text="Choose feature selection methods",
                                                font=controller.title_font)

        self.feature_selection_methods = Checkbar(self, load_feature_selection_list())

        self.back_button = tk.Button(self, text="Back",
                                     command=lambda: controller.show_frame("AlgorithmsWindow"))

        self.next_button = tk.Button(self, text="Next",
                                     command=lambda: controller.show_frame("SimilarityFunctionsWindow"))

        # Layout using grid
        self.feature_selection_title.grid(row=0, column=2, pady=3)
        self.feature_selection_methods.grid(row=2, column=2, pady=3)

        self.grid_rowconfigure(13, minsize=100)
        self.back_button.grid(row=50, column=2, pady=3)
        self.next_button.grid(row=50, column=15, pady=3)