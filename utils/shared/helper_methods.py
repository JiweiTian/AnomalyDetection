import numpy as np
from numpy import dot
from numpy.linalg import norm
import pandas as pd
import yaml


def cosine_similarity(x, y):
    """
    calculate cosine similarity between 2 given vectors
    :param x: vector
    :param y: vector
    :return: cosine similarity
    """
    return dot(x, y) / (norm(x) * norm(y))


def euclidean_distance(x, y):
    """
    calculate the euclidean distance between 2 given vectors
    :param x: vector
    :param y: vector
    :return: euclidean distance
    """
    return np.linalg.norm(x - y)


def anomaly_score(input_vector, output_vector, dist='cosine'):
    """
    calculate the anomaly of single output decoder
    :param x: input vector
    :param y: output vector
    :return: anomaly score based on cosine similarity
    """
    assert len(input_vector) == len(output_vector)
    assert len(input_vector) > 0
    assert dist == 'cosine' or dist == 'euclidean'

    switcher = {
        "cosine": 1 - cosine_similarity(input_vector, output_vector),
        "euclidean_distance": euclidean_distance(input_vector, output_vector)
    }

    return switcher.get(dist, euclidean_distance(input_vector, output_vector))


def anomaly_score_multi(input_vectors, output_vectors):
    """
    calculate the anomaly of a multiple output decoder
    :param input_vectors: list of input vectors
    :param output_vectors: list of output vectors
    :return: anomaly score based on cosine similarity
    """
    sum = 0
    input_length = len(input_vectors)

    assert input_length == len(output_vectors)
    assert input_length > 0

    for i in range(input_length):
        sum += anomaly_score(input_vectors[i], output_vectors[i])

    return sum / input_length


def rolled(list, window_size):
    """
    generator to yield batches of rows from a data frame of <window_size>
    :param list: list
    :param window_size: window size
    :return: batch of rows
    """
    count = 0
    while count <= len(list) - window_size:
        yield list[count: count + window_size]
        count += 1


def get_training_data_lstm(list, window_size):
    """
    get training data for lstm autoencoder
    :param list: the list for training
    :param window_size: window size for each instance in training
    :return: X for training
    """

    X = []
    for val in rolled(list, window_size):
        X.append(val)

    return np.array(X)


def get_testing_data_lstm(list, labels, window_size):
    """
    get testing data for lstm autoencoder
    :param list: the list for testing
    :param labels: labels
    :param window_size: window size for each instance in training
    :return: (X, Y) for testing
    """
    X = []
    for val in rolled(list, window_size):
        X.append(val)

    Y = []
    for val in rolled(labels, window_size):
        Y.append(max(val))

    return np.array(X), np.array(Y)


def get_threshold(scores, percent):
    """
    get threshold for classification from this percent of training set that had lower scores
    (e.g get the threshold error in which 95% of training set had lower values than)
    :param scores:
    :param percent:
    :return: threshold
    """
    assert percent <= 1 and percent > 0

    index = int(len(scores) * percent)

    return sorted(scores)[index - 1]


def get_thresholds(list_scores, percent):
    """
    get threshold for classification from this percent of training set that had lower scores
    (e.g get the threshold error in which 95% of training set had lower values than)
    :param scores: list of scores
    :param percent:
    :return: list of thresholds
    """
    return [get_threshold(scores, percent) for scores in list_scores]


def get_previous_method_scores(prediction, windows):
    """
    get previous method scores (TPR, FPR, delay)
    :param prediction: predictions
    :param windows: list of dictionaries that define lower and upper bounds for attack injections
    :return: TPR, FPR, delay
    """
    fp = 0
    fn = 0
    tp = 0
    tn = 0

    detection_delay = -1

    for window in windows:
        upper = window["upper"]
        lower = window["lower"]
        assert len(prediction) >= upper
        assert upper > lower

        was_detected = False

        for i in range(lower):
            if prediction[i] == 1:
                fp += 1
            else:
                tn += 1

        for i in range(lower, upper):
            if prediction[i] == 1:
                tp += 1
                if not was_detected:
                    was_detected = True
                    detection_delay = i - lower
            else:
                fn += 1

        for i in range(upper, len(prediction)):
            if prediction[i] == 1:
                fp += 1
            else:
                tn += 1

        if not was_detected:
            detection_delay = upper - lower

    tpr = tp / (tp + fn)
    fpr = fp / (fp + tn)

    return tpr, fpr, detection_delay


def report_results(results_dir_path, verbose=1):
    """

    :param results_dir_path:
    :param verbose:
    :return:
    """
    ATTACKS = load_attacks()
    FLIGHT_ROUTES = load_flight_routes()

    for result in ["nab", "fpr", "tpr", "delay"]:
        results = pd.DataFrame(columns=ATTACKS)
        for i, flight_route in enumerate(FLIGHT_ROUTES):
            df = pd.read_csv(f'{results_dir_path}/{flight_route}_{result}.csv')
            mean = df.mean(axis=0).values
            std = df.std(axis=0).values
            output = [f'{round(x, 2)}±{round(y, 2)}%' for x, y in zip(mean, std)]
            results.loc[i] = output

        results.index = FLIGHT_ROUTES

        if verbose:
            print(results)

        results.to_csv(f'{results_dir_path}/final_{result}.csv')


def is_excluded_flight(route, csv):
    """
    return if excluded flight
    :param route: flight route
    :param csv: csv of a flight
    :return:  if excluded
    """
    EXCLUDE_FLIGHTS = load_exclude_flights()

    return route in EXCLUDE_FLIGHTS and csv in EXCLUDE_FLIGHTS[route]


def load_from_yaml(filename, key):
    with open(r'.\\' + filename + '.yaml') as file:
        loaded_file = yaml.load(file, Loader=yaml.FullLoader)
        return loaded_file.get(key)


def load_exclude_flights():
    return load_from_yaml('lstm_model_settings', 'EXCLUDE_FLIGHTS')


def load_attacks():
    return load_from_yaml('names', 'ATTACKS')


def load_flight_routes():
    return load_from_yaml('names', 'FLIGHT_ROUTES')
