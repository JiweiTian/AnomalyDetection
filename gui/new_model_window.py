import tkinter as tk

from gui.utils.helper_methods import set_training_path, set_test_path


class NewModel(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # Create Widgets
        self.new_model_title = tk.Label(self, text="New model", font=controller.title_font)

        self.training_label = tk.Label(self, text="Training directory")
        self.training_input = tk.Entry(self)
        self.training_btn = tk.Button(self, text="Browse", command=set_training_path)

        self.test_label = tk.Label(self, text="Test directory")
        self.test_input = tk.Entry(self)
        self.test_btn = tk.Button(self, text="Browse", command=set_test_path)

        self.back_button = tk.Button(self, text="Back",
                                     command=lambda: controller.show_frame("MainWindow"))

        self.next_button = tk.Button(self, text="Next",
                                     command=lambda: controller.show_frame("AlgorithmsWindow"))

        # Layout using grid
        self.new_model_title.grid(row=0, column=2, pady=3)

        self.training_label.grid(row=1, column=0, pady=3)
        self.training_input.grid(row=1, column=1, pady=3)
        self.training_btn.grid(row=1, column=2, pady=3)

        self.test_input.grid(row=2, column=1, pady=3)
        self.test_label.grid(row=2, column=0, pady=3)
        self.test_btn.grid(row=2, column=2, pady=3)

        self.back_button.grid(row=15, column=0, pady=3)
        self.next_button.grid(row=15, column=3, pady=3)