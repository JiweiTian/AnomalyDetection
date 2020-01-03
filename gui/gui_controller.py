import tkinter as tk
from tkinter import font as tkfont

from gui.algorithms_window import AlgorithmsWindow
from gui.feature_selection_window import FeatureSelectionWindow
from gui.load_model_window import LoadModel
from gui.main_window import MainWindow
from gui.model_controller import model_controller
from gui.new_model_window import NewModel
from gui.similarity_functions_window import SimilarityFunctionsWindow


class AnomalyDetectionGUI(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.model_controller = model_controller(self)

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        self.geometry('800x600')
        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # container.title('Anomaly Detection Classifier')
        # container.geometry("650x400")
        # container.option_add('*tearOff', 'FALSE')  # Disables ability to tear menu bar into own window
        self.frames = {}
        for F in (MainWindow, NewModel, LoadModel, AlgorithmsWindow, FeatureSelectionWindow, SimilarityFunctionsWindow):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("MainWindow")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()


    def set_new_model_training_input_path(self,input):
        self.model_controller.set_training_data_dir(input)

    def set_new_model_test_input_path(self,input):
        self.model_controller.set_test_data_dir(input)

    def set_algorithm_parameters(self,algorithm_name,algorithm_parameters):
        self.model_controller.set_algorithm_parameters(algorithm_name,algorithm_parameters)

    def remove_algorithm_parameters(self,algorithm_name, algorithm_parameters):
        self.model_controller.remove_algorithm_parameters(algorithm_name, algorithm_parameters)

    def set_similarity_score(self,similarity_list):
        self.model_controller.set_similarity_score(similarity_list)

    def run_models(self):
        self.model_controller.run_models()


if __name__ == "__main__":
    app = AnomalyDetectionGUI()
    app.mainloop()
