from pymorse import Morse
import logging

# -----------------------------LOGGING CONFIGURATION -----------------------------------
logger = logging.getLogger("morse."+__name__)
logger.setLevel(logging.DEBUG)
# File Handler
fh = logging.FileHandler('robots_communications.log', mode = 'w')
fh.setLevel(logging.DEBUG)
# Console Handler
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
# Formatter for both Handlers
formatter = logging.Formatter('[%(asctime)s (%(levelname)s)]  %(message)s', "%H:%M:%S")
fh.setFormatter(formatter)
ch.setFormatter(formatter)
# Add Handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)
# --------------------------------------------------------------------------------------



class Communication_Simulator():
    """This class aims to simulate if 2 robots can communicate each other according to specific models"""

    __models = ('distance', 'line_of_sight', 'free_space_loss', 'empiric_1')
    __default_model = 'distance'

    def __init__(self, robot_1, robot_2):
        """ Initialization / Constructor """
        # Robot names are assumed to be correct
        self.__r1 = robot_1
        self.__r2 = robot_2
        self.__set_model2default()
    
    def can_communicate(self):
        """ This public method returns 'True' or 'False' if the 2 robots can communicate or not. """
        return True


    def set_model(self, model):
        """ This public method set a new communication model between the 2 robots.
        If the 'model' argument doesn't exist, it sets to the default one. 
        A log(debug) message is given in the last case. """
        
        if self.model_exists(model):
            self.__model = model
        else:
            logger.warning("Communication model '%s' doesn't exist."%model.upper())
            self.__set_model2default()
        
        logger.info("Communication model '%s' was settled between '%s' and '%s'."\
                    %(self.__model.upper(), self.__r1.upper(), self.__r2.upper()))


    def model_exists(self, model):
        """ This public method returns 'True' or 'False' if the model exists or not in this module. """
        if model.lower() in self.__models:  return True
        else:                               return False

    
    def __set_model2default(self):
        """ This (supposed) private method sets the default communication model between the 2 robots. """
        self.__model = self.__default_model


    def get_model(self):
        """ This public method returns the current communication model between the 2 robots. """
        return self.__model
    
    
    def print_models(self):
        # This method was only for debugging...
        print("\n---------------------------------\nAvailable models:\n\t")
        print("\n".join(self.__models))
        print("\n---------------------------------\n")




