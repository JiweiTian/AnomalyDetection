import pandas as pd

from utils.shared.lstm_hyper_parameters import lstm_hyper_parameters
from utils.shared.routes import *
from utils.shared.models.lstm_autoencoder import get_lstm_autoencoder_model
#from utils.shared.lstm_hyper_parameters import LSTM_WINDOW_SIZE, LSTM_ENCODING_DIMENSION, \
 #   LSTM_THRESHOLD_FROM_TRAINING_PERCENT
from utils.shared.helper_methods import get_training_data_lstm, get_testing_data_lstm, anomaly_score_multi, \
    get_threshold, report_results, get_previous_method_scores, is_excluded_flight, load_exclude_flights, \
    load_attacks, load_flight_routes

from tensorflow.python.keras.models import load_model
from sklearn.preprocessing import MaxAbsScaler
from utils.windows import windows
from collections import defaultdict

def subdirectories(path):
    directories = []
    for directory in os.listdir(path):
        if os.path.isdir(os.path.join(path, directory)):
            directories.append(directory)
    return directories


def run_model(training_data_dir,test_data_dir,similarity_score):
    window_size = lstm_hyper_parameters.get_window_size()
    encoding_dimension = lstm_hyper_parameters.get_encoding_dimension()
    activation = lstm_hyper_parameters.get_activation()
    loss = lstm_hyper_parameters.get_loss()
    optimizer = lstm_hyper_parameters.get_optimizer()
    threshold = lstm_hyper_parameters.get_threshold()

    FLIGHT_ROUTES = subdirectories(training_data_dir)
    for flight_route in FLIGHT_ROUTES:
        tpr_scores, fpr_scores, delay_scores =execute(flight_route,
                                                    training_data_dir = training_data_dir,
                                                    test_data_dir = test_data_dir,
                                                    similarity_score = similarity_score,
                                                    window_size = window_size,
                                                    encoding_dimension = encoding_dimension,
                                                    activation = activation,
                                                    loss = loss,
                                                    optimizer = optimizer,
                                                    threshold = threshold)

    #     df = pd.DataFrame(tpr_scores)
    #     df.to_csv(f'export/results/lstm/{flight_route}_tpr.csv', index=False)
    #
    #     df = pd.DataFrame(fpr_scores)
    #     df.to_csv(f'export/results/lstm/{flight_route}_fpr.csv', index=False)
    #
    #     df = pd.DataFrame(delay_scores)
    #     df.to_csv(f'export/results/lstm/{flight_route}_delay.csv', index=False)
    #
    # report_results('export/results/lstm')

def execute(flight_route,
            train=True,
            add_plots=True,
            training_data_dir = None,
            test_data_dir = None,
            similarity_score = None,
            window_size = None,
            encoding_dimension = None,
            activation = None,
            loss = None,
            optimizer = None,
            threshold = None):
    fligth_dir = os.path.join(training_data_dir, flight_route)
    ATTACKS = subdirectories(fligth_dir)

    # nab_scores = defaultdict(list)
    tpr_scores = defaultdict(list)
    fpr_scores = defaultdict(list)
    delay_scores = defaultdict(list)

    os.path.join(training_data_dir, flight_route)


    without_anom_dir = os.path.join(flight_route, 'without_anom.csv')
    df_train = pd.read_csv(without_anom_dir)

    df_train = df_train[
        ['Direction', 'Speed', 'Altitude', 'lat', 'long', 'first_dis', 'second_dis', 'third_dis', 'fourth_dis']
    ]

    scalar = MaxAbsScaler()

    X_train = scalar.fit_transform(df_train)
    X_train = get_training_data_lstm(X_train, window_size)

    if train:
        lstm = get_lstm_autoencoder_model(window_size, df_train.shape[1],
                                          encoding_dimension,activation,loss,optimizer)
        history = lstm.fit(X_train, X_train, epochs=10, verbose=1).history
        # lstm.save(f'export/models/lstm/model_{flight_route}.h5')
        # if add_plots:
        #     plot(history['loss'], ylabel='loss', xlabel='epoch', title="Epoch Loss")
    #else:
        #lstm = load_model(f'export/models/lstm/model_{flight_route}.h5')

    X_pred = lstm.predict(X_train, verbose=1)
    scores_train = []
    for i, pred in enumerate(X_pred):
        scores_train.append(anomaly_score_multi(X_train[i], pred))

    # choose threshold for which <LSTM_THRESHOLD_FROM_TRAINING_PERCENT> % of training were lower
    THRESHOLD = get_threshold(scores_train, threshold)

    for attack in ATTACKS:
        for flight_csv in os.listdir(f'{training_data_dir}/{flight_route}/{attack}'):
            if is_excluded_flight(flight_route, flight_csv):
                continue

            df_test = pd.read_csv(f'{training_data_dir}/{flight_route}/{attack}/{flight_csv}')
            df_test_labels = df_test[['label']].values
            df_test = df_test[
                ['Direction', 'Speed', 'Altitude', 'lat', 'long', 'first_dis', 'second_dis', 'third_dis', 'fourth_dis']]
            X_test = scalar.transform(df_test)
            X_test, y_test = get_testing_data_lstm(X_test, df_test_labels, window_size)

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



















    # if __name__ == "__main__":
        #FLIGHT_ROUTES = load_flight_routes()
        #
        # for flight_route in FLIGHT_ROUTES:
        #     tpr_scores, fpr_scores, delay_scores = execute(flight_route, train=True, add_plots=False) # nab_scores
        #
        #     # df = pd.DataFrame(nab_scores)
        #     # df.to_csv(f'export/results/lstm/{flight_route}_nab.csv', index=False)
        #
        #     df = pd.DataFrame(tpr_scores)
        #     df.to_csv(f'export/results/lstm/{flight_route}_tpr.csv', index=False)
        #
        #     df = pd.DataFrame(fpr_scores)
        #     df.to_csv(f'export/results/lstm/{flight_route}_fpr.csv', index=False)
        #
        #     df = pd.DataFrame(delay_scores)
        #     df.to_csv(f'export/results/lstm/{flight_route}_delay.csv', index=False)
        #
        # report_results('export/results/lstm')
