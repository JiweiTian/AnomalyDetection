from utils.shared.input_settings import input_settings
#from utils.shared.models_execution import models_execution
from utils.shared.models_execution import models_execution


class model_controller:

    def __init__(self, gui_controller):
        self.gui_controller = gui_controller


    def set_training_data_dir(self,dir):
        input_settings.set_training_data_dir(dir)

    def get_training_data_dir(self):
        return input_settings.get_training_data_dir(dir)

    def set_test_data_dir(self,dir):
        input_settings.set_test_data_dir(dir)

    def get_test_data_dir(self):
        return input_settings.get_test_data_dir(dir)

    def set_algorithm_parameters(self,algorithm_name,algorithm_parameters):
        input_settings.set_algorithm_parameters(algorithm_name,algorithm_parameters)

    def remove_algorithm_parameters(self, algorithm_name, algorithm_parameters):
        input_settings.remove_algorithm_parameters(algorithm_name, algorithm_parameters)

    def set_similarity_score(self,similarity_list):
        input_settings.set_similarity_score(similarity_list)

    def run_models(self):
        models_execution.run_models()
