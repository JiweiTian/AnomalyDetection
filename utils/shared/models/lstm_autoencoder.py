from keras.models import Sequential
from keras.layers import LSTM
from keras.layers import Dense
from keras.layers import RepeatVector
from keras.layers import TimeDistributed

from keras.utils import plot_model


def get_lstm_autoencoder_model(timesteps, features, incoding_dimension):
    model = Sequential()
    model.add(LSTM(incoding_dimension, activation='relu', input_shape=(timesteps, features)))
    model.add(RepeatVector(timesteps))
    model.add(LSTM(incoding_dimension, activation='relu', return_sequences=True))
    model.add(TimeDistributed(Dense(features)))
    model.compile(optimizer='adam', loss='mse')

    plot_model(model, to_file='model.png')

    return model
