from lstm_execution import run_model
from utils.shared.input_settings import input_settings


class models_execution:


    @staticmethod
    def run_models():
        algorithms = input_settings.get_algorithms()
        similarity_score = input_settings.get_similarity()
        training_data_dir = input_settings.get_training_data_dir()
        test_data_dir = input_settings.get_test_data_dir()
        for algorithm in algorithms:
            model_execution_function = getattr(models_execution, algorithm+"_execution")
            model_execution_function(training_data_dir,
                                     test_data_dir,similarity_score,)

    @staticmethod
    def LSTM_execution(training_data_dir,
                       test_data_dir,similarity_score):
        run_model(training_data_dir,test_data_dir
                           ,similarity_score)
