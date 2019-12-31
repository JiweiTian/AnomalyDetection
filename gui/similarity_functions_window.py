import tkinter as tk

from gui.checkbox import Checkbar
from gui.utils.helper_methods import load_similarity_list


class SimilarityFunctionsWindow(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # Create Widgets
        self.similarity_functions_title = tk.Label(self, text="Choose similarity functions",
                                                   font=controller.title_font)

        self.similarity_functions = Checkbar(self, load_similarity_list())

        self.back_button = tk.Button(self, text="Back",
                                     command=lambda: controller.show_frame("FeatureSelectionWindow"))

        self.run_button = tk.Button(self, text="Run")  # , command=lambda: controller.create_function_to_run)

        # Layout using grid
        self.similarity_functions_title.grid(row=0, column=2, pady=3)
        self.similarity_functions.grid(row=2, column=2, pady=3)

        self.back_button.grid(row=15, column=0, pady=3)
        self.run_button.grid(row=15, column=3, pady=3)
