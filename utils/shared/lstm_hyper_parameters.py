
class lstm_hyper_parameters:
    # number of training samples to use for encoding and decoding each time for the LSTM
    LSTM_WINDOW_SIZE = None

    # encoding dimension for LSTM autoencoder
    LSTM_ENCODING_DIMENSION = None

    # determine threshold for classification from this percent of training set that had lower errors
    # (e.g get the threshold error in which 99% of training set had lower values than)
    LSTM_THRESHOLD_FROM_TRAINING_PERCENT = None

    LSTM_ACTIVATION = None

    LSTM_LOSS = None

    LSTM_OPTIMIZER = None

    @staticmethod
    def set_window_size(window_size):
        lstm_hyper_parameters.LSTM_WINDOW_SIZE = int(window_size)

    @staticmethod
    def remove_window_size(window_size):
        lstm_hyper_parameters.LSTM_WINDOW_SIZE = None

    @staticmethod
    def get_window_size():
        return lstm_hyper_parameters.LSTM_WINDOW_SIZE

    @staticmethod
    def set_encoding_dimension(encoding_dimension):
        lstm_hyper_parameters.LSTM_ENCODING_DIMENSION = int(encoding_dimension)

    @staticmethod
    def remove_encoding_dimension(encoding_dimension):
        lstm_hyper_parameters.LSTM_ENCODING_DIMENSION = None

    @staticmethod
    def get_encoding_dimension():
        return lstm_hyper_parameters.LSTM_ENCODING_DIMENSION

    @staticmethod
    def set_activation(activation):
        lstm_hyper_parameters.LSTM_ACTIVATION = activation

    @staticmethod
    def remove_activation(activation):
        lstm_hyper_parameters.LSTM_ACTIVATION = None

    @staticmethod
    def get_activation():
        return lstm_hyper_parameters.LSTM_ACTIVATION

    @staticmethod
    def set_loss (loss ):
        lstm_hyper_parameters.LSTM_LOSS = loss

    @staticmethod
    def remove_loss (loss ):
        lstm_hyper_parameters.LSTM_LOSS = None

    @staticmethod
    def get_loss():
        return lstm_hyper_parameters.LSTM_LOSS

    @staticmethod
    def set_optimizer (optimizer ):
        lstm_hyper_parameters.LSTM_OPTIMIZER = optimizer

    @staticmethod
    def remove_optimizer (optimizer ):
        lstm_hyper_parameters.LSTM_OPTIMIZER = None

    @staticmethod
    def get_optimizer():
        return lstm_hyper_parameters.LSTM_OPTIMIZER

    @staticmethod
    def set_threshold (threshold ):
        lstm_hyper_parameters.LSTM_THRESHOLD_FROM_TRAINING_PERCENT = float(threshold)

    @staticmethod
    def remove_threshold (threshold ):
        lstm_hyper_parameters.LSTM_THRESHOLD_FROM_TRAINING_PERCENT = None

    @staticmethod
    def get_threshold():
        return lstm_hyper_parameters.LSTM_THRESHOLD_FROM_TRAINING_PERCENT



