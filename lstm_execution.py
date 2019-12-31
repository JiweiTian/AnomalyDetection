import pandas as pd
from utils.shared.routes import *
from utils.shared.models.lstm_autoencoder import get_lstm_autoencoder_model
from utils.shared.lstm_hyper_parameters import LSTM_WINDOW_SIZE, LSTM_ENCODING_DIMENSION, \
    LSTM_THRESHOLD_FROM_TRAINING_PERCENT
from utils.shared.helper_methods import get_training_data_lstm, get_testing_data_lstm, anomaly_score_multi, \
    get_threshold, report_results, get_previous_method_scores, is_excluded_flight, load_exclude_flights, \
    load_attacks, load_flight_routes

from tensorflow.python.keras.models import load_model
from sklearn.preprocessing import MaxAbsScaler
from utils.windows import windows
from collections import defaultdict


def execute(flight_route, train=True, add_plots=True):
    ATTACKS = load_attacks()

    # nab_scores = defaultdict(list)
    tpr_scores = defaultdict(list)
    fpr_scores = defaultdict(list)
    delay_scores = defaultdict(list)

    df_train = pd.read_csv(f'{DATA_TRANSFORMED_DIR}/{flight_route}/without_anom.csv')
    df_train = df_train[
        ['Direction', 'Speed', 'Altitude', 'lat', 'long', 'first_dis', 'second_dis', 'third_dis', 'fourth_dis']
    ]

    scalar = MaxAbsScaler()

    X_train = scalar.fit_transform(df_train)
    X_train = get_training_data_lstm(X_train, LSTM_WINDOW_SIZE)

    if train:
        lstm = get_lstm_autoencoder_model(LSTM_WINDOW_SIZE, df_train.shape[1], LSTM_ENCODING_DIMENSION)
        history = lstm.fit(X_train, X_train, epochs=10, verbose=1).history
        # lstm.save(f'export/models/lstm/model_{flight_route}.h5')
        # if add_plots:
        #     plot(history['loss'], ylabel='loss', xlabel='epoch', title="Epoch Loss")
    else:
        lstm = load_model(f'export/models/lstm/model_{flight_route}.h5')

    X_pred = lstm.predict(X_train, verbose=1)
    scores_train = []
    for i, pred in enumerate(X_pred):
        scores_train.append(anomaly_score_multi(X_train[i], pred))

    # choose threshold for which <LSTM_THRESHOLD_FROM_TRAINING_PERCENT> % of training were lower
    THRESHOLD = get_threshold(scores_train, LSTM_THRESHOLD_FROM_TRAINING_PERCENT)

    for attack in ATTACKS:
        for flight_csv in os.listdir(f'{DATA_TRANSFORMED_DIR}/{flight_route}/{attack}'):
            if is_excluded_flight(flight_route, flight_csv):
                continue

            df_test = pd.read_csv(f'{DATA_TRANSFORMED_DIR}/{flight_route}/{attack}/{flight_csv}')
            df_test_labels = df_test[['label']].values
            df_test = df_test[
                ['Direction', 'Speed', 'Altitude', 'lat', 'long', 'first_dis', 'second_dis', 'third_dis', 'fourth_dis']]
            X_test = scalar.transform(df_test)
            X_test, y_test = get_testing_data_lstm(X_test, df_test_labels, LSTM_WINDOW_SIZE)

            X_pred = lstm.predict(X_test, verbose=1)
            scores_test = []
            for i, pred in enumerate(X_pred):
                scores_test.append(anomaly_score_multi(X_test[i], pred))

            # if add_plots:
            #     plot_reconstruction_error_scatter(scores=scores_train, labels=[0] * len(scores_train),
            #                                       threshold=THRESHOLD, title=f'Outlier Score Training ({attack})')
            #     plot_reconstruction_error_scatter(scores=scores_test, labels=y_test, threshold=THRESHOLD,
            #                                       title=f'Outlier Score Testing ({attack})')

            predictions = [1 if x >= THRESHOLD else 0 for x in scores_test]

            # nab_scores[attack].append(get_nab_score(predictions, windows=windows["flight_lstm"]))
            previous_method_scores = get_previous_method_scores(predictions, windows=windows["flight_lstm"])

            tpr_scores[attack].append(previous_method_scores[0])
            fpr_scores[attack].append(previous_method_scores[1])
            delay_scores[attack].append(previous_method_scores[2])

    return tpr_scores, fpr_scores, delay_scores # nab_scores,


if __name__ == "__main__":
    FLIGHT_ROUTES = load_flight_routes()

    for flight_route in FLIGHT_ROUTES:
        tpr_scores, fpr_scores, delay_scores = execute(flight_route, train=True, add_plots=False) # nab_scores

        # df = pd.DataFrame(nab_scores)
        # df.to_csv(f'export/results/lstm/{flight_route}_nab.csv', index=False)

        df = pd.DataFrame(tpr_scores)
        df.to_csv(f'export/results/lstm/{flight_route}_tpr.csv', index=False)

        df = pd.DataFrame(fpr_scores)
        df.to_csv(f'export/results/lstm/{flight_route}_fpr.csv', index=False)

        df = pd.DataFrame(delay_scores)
        df.to_csv(f'export/results/lstm/{flight_route}_delay.csv', index=False)

    report_results('export/results/lstm')
