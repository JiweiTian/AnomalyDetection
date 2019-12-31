import os
import yaml
import tkinter
from tkinter.filedialog import askdirectory
from gui.utils.constants import *


def set_path():
    tkinter.Tk().withdraw()
    dirname = askdirectory(initialdir=os.getcwd(), title='Please select a directory')
    if len(dirname) > 0:
        return dirname
    else:
        return ""


def set_training_path():
    global training_path
    training_path = set_path()


def set_test_path():
    global test_path
    test_path = set_path()


def load_classification_methods(list_name):
    with open(r'.\shared\classification_methods.yaml') as file:
        classification_methods = yaml.load(file, Loader=yaml.FullLoader)
        return classification_methods.get(list_name)


def load_anomaly_detection_list():
    return load_classification_methods(ANOMALY_DETECTION_METHODS)


def load_feature_selection_list():
    return load_classification_methods(FEATURE_SELECTION_METHODS)


def load_similarity_list():
    return load_classification_methods(SIMILARITY_FUNCTIONS)
