#from utils.settings import LSTM_WINDOW_SIZE

windows = {
    "flight": [
        {
            "lower": 180,
            "upper": 250,
        }
    ],
    "flight_lstm": [
        {
            #"lower": 180 - LSTM_WINDOW_SIZE + 1,
            "upper": 249
        }
    ]
}
