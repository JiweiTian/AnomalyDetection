from keras.models import Sequential
from keras.layers import LSTM
from keras.layers import Dense
from keras.layers import RepeatVector
from keras.layers import TimeDistributed


def get_lstm_autoencoder_model(timesteps,
                               features,
                               encoding_dimension,
                               activation,
                               loss,
                               optimizer):
    model = Sequential()
    model.add(LSTM(encoding_dimension, activation=activation, input_shape=(timesteps, features)))
    model.add(RepeatVector(timesteps))
    model.add(LSTM(encoding_dimension, activation=activation, return_sequences=True))
    model.add(TimeDistributed(Dense(features)))
    model.compile(optimizer=optimizer, loss=loss)

    return model
