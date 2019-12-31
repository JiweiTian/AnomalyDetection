import os
import yaml
import tkinter

from tkinter import ttk
from tkinter.filedialog import askdirectory
from gui.checkbox import Checkbar
from gui.menubar import Menubar



"""
~~~~~~~~~~~~~~~~~~~~~~~~  Class Description ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    This class contains the main configuration of graphic user interface
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
ANOMALY_DETECTION_METHODS = 'anomaly_detection_methods'
FEATURE_SELECTION_METHODS = 'feature_selection_methods'
SIMILARITY_FUNCTIONS = 'similarity_functions'


# Remove all strings to yaml files (including labels and titles)

class GUI(ttk.Frame):
    """Main GUI class"""

    def __init__(self, parent, *args, **kwargs):
        ttk.Frame.__init__(self, parent, *args, **kwargs)
        self.load_classification_methods()
        self.init_gui(parent)

    # def openwindow(self):
    #     self.new_win = tkinter.Toplevel(self.root)  # Set parent

    def load_classification_methods(self):
        with open(r'.\shared\classification_methods.yaml') as file:
            classification_methods = yaml.load(file, Loader=yaml.FullLoader)
            self.anomaly_detection_list = classification_methods.get(ANOMALY_DETECTION_METHODS)
            self.feature_selection_list = classification_methods.get(FEATURE_SELECTION_METHODS)
            self.similarity_list = classification_methods.get(SIMILARITY_FUNCTIONS)

    def run_classifier(self):
        'not implemented here'

    def exit_window(self):
        'should be implemented here'

    def set_path(self):
        tkinter.Tk().withdraw()
        dirname = askdirectory(initialdir=os.getcwd(), title='Please select a directory')
        if len(dirname) > 0:
            return dirname
        else:
            return ""

    def set_training_path(self):
        global training_path
        training_path = self.set_path()

    def set_test_path(self):
        global test_path
        test_path = self.set_path()

    def init_gui(self, window):
        window.title('Anomaly Detection Classifier')
        window.geometry("650x400")
        window.option_add('*tearOff', 'FALSE')  # Disables ability to tear menu bar into own window

        # Menu Bar
        self.menubar = Menubar(window)

        # Create Widgets
        self.training_label = ttk.Label(window, text="Training directory")
        self.training_input = ttk.Entry(window)
        self.training_btn = ttk.Button(window, text="Browse", command=self.set_training_path)

        self.test_label = ttk.Label(window, text="Test directory")
        self.test_input = ttk.Entry(window)
        self.test_btn = ttk.Button(window, text="Browse", command=self.set_test_path)

        self.anomaly_detection_label = ttk.Label(window, text="Anomaly detection methods")
        self.feature_selection_label = ttk.Label(window, text="Feature selection methods")
        self.similarity_label = ttk.Label(window, text="Similarity functions")

        self.anomaly_detection_methods = Checkbar(window, self.anomaly_detection_list)
        self.feature_selection_methods = Checkbar(window, self.feature_selection_list)
        self.similarity_functions = Checkbar(window, self.similarity_list)

        self.similarity_threshold_label = ttk.Label(window, text="Similarity function threshold")
        self.similarity_threshold_input = ttk.Entry(window)

        self.start_btn = ttk.Button(window, text="Run", command=self.run_classifier)
        self.quit_btn = ttk.Button(window, text="Quit", command=self.exit_window)

        # Layout using grid
        self.training_label.grid(row=1, column=0, pady=3)
        self.training_input.grid(row=1, column=1, pady=3)
        self.training_btn.grid(row=1, column=2, pady=3)

        self.test_input.grid(row=2, column=1, pady=3)
        self.test_label.grid(row=2, column=0, pady=3)
        self.test_btn.grid(row=2, column=2, pady=3)

        self.anomaly_detection_label.grid(row=3, column=0, padx=3, pady=3)
        self.anomaly_detection_methods.grid(row=3, column=1, padx=3, pady=7)

        self.feature_selection_label.grid(row=4, column=0, pady=3)
        self.feature_selection_methods.grid(row=4, column=1, pady=7)

        self.similarity_label.grid(row=5, column=0, pady=3)
        self.similarity_functions.grid(row=5, column=1, pady=7)

        self.similarity_threshold_label.grid(row=6, column=0, pady=3)
        self.similarity_threshold_input.grid(row=6, column=1, pady=7)

        self.start_btn.grid(row=7, column=1, pady=7)
        self.quit_btn.grid(row=7, column=0, pady=7)


if __name__ == '__main__':
    root = tkinter.Tk()
    GUI(root)
    root.mainloop()
