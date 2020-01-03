from tkinter import *
from tkinter.ttk import Combobox

from gui.utils.helper_methods import load_lstm_activation_list, load_lstm_loss_list, load_lstm_optimizer_list, \
    load_lstm_window_size_list, load_lstm_encoder_dimension_list, load_lstm_threshold_list


class lstm_frame_option(Frame):

    def __init__(self, parent=None):
        Frame.__init__(self, parent)
        self.parent = parent
        self.parameters ={}
        self.activation = load_lstm_activation_list()
        self.loss = load_lstm_loss_list()
        self.optimizer = load_lstm_optimizer_list()
        self.window_size = load_lstm_window_size_list()
        self.encoder_dimension = load_lstm_encoder_dimension_list()
        self.encoder_threshold = load_lstm_threshold_list()



        Label(self, text="LSTM activation").grid(row=0,column=10)
        self.lstm_activation_combo = Combobox(self, values=self.activation)
        self.lstm_activation_combo.grid(row=0, column=13, columnspan=2)
        self.lstm_activation_combo.current(0)
        self.parameters["activation"] = self.lstm_activation_combo
        self.lstm_activation_combo.bind("<<ComboboxSelected>>", self.combo_selected)

        self.grid_rowconfigure(1, minsize=10)

        Label(self, text="LSTM loss").grid(row=2,column=10)
        self.lstm_loss_combo = Combobox(self, values=self.loss)
        self.lstm_loss_combo.grid(row=2, column=13, columnspan=2)
        self.lstm_loss_combo.current(0)
        self.parameters["loss"] = self.lstm_loss_combo
        self.lstm_loss_combo.bind("<<ComboboxSelected>>", self.combo_selected)

        self.grid_rowconfigure(3, minsize=10)

        Label(self, text="LSTM optimizer").grid(row=4,column=10)
        self.lstm_optimizer_combo = Combobox(self, values=self.optimizer)
        self.lstm_optimizer_combo.grid(row=4, column=13, columnspan=2)
        self.lstm_optimizer_combo.current(0)
        self.parameters["optimizer"] = self.lstm_optimizer_combo
        self.lstm_optimizer_combo.bind("<<ComboboxSelected>>", self.combo_selected)

        self.grid_rowconfigure(5, minsize=10)

        Label(self, text="LSTM window size").grid(row=6,column=10)
        self.lstm_window_combo = Combobox(self, values=self.window_size)
        self.lstm_window_combo.grid(row=6, column=13, columnspan=2)
        self.lstm_window_combo.current(0)
        self.parameters["window_size"] = self.lstm_window_combo
        self.lstm_window_combo.bind("<<ComboboxSelected>>", self.combo_selected)

        self.grid_rowconfigure(7, minsize=10)

        Label(self, text="LSTM encoding dimension").grid(row=8,column=10)
        self.lstm_encoder_dimension_combo = Combobox(self, values=self.encoder_dimension)
        self.lstm_encoder_dimension_combo.grid(row=8, column=13, columnspan=2)
        self.lstm_encoder_dimension_combo.current(0)
        self.parameters["encoding_dimension"] = self.lstm_encoder_dimension_combo
        self.lstm_encoder_dimension_combo.bind("<<ComboboxSelected>>", self.combo_selected)

        self.grid_rowconfigure(9, minsize=10)

        Label(self, text="LSTM threshold").grid(row=10,column=10)
        self.lstm_threshold_combo = Combobox(self, values=self.encoder_threshold)
        self.lstm_threshold_combo.grid(row=10, column=13, columnspan=2)
        self.lstm_threshold_combo.current(0)
        self.parameters["threshold"] = self.lstm_threshold_combo
        self.lstm_threshold_combo.bind("<<ComboboxSelected>>", self.combo_selected)

        self.grid_rowconfigure(9, minsize=10)

    def get_algorithm_parameters(self): # This function can be done in a single line - check how to do it right
        sol = {}
        for parameter in self.parameters.keys():
            sol[parameter] = self.parameters[parameter].get()
        return sol

    def combo_selected(self,event):
        self.parent.set_algorithm_parameters("LSTM",self.get_algorithm_parameters())







