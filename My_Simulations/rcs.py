import pymorse
import math
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



class RCS():
    """This class aims to simulate if 2 robots can communicate each other according to specific models"""

    __models = ('distance', 'line_of_sight', 'free_space_loss', 'empiric_1')
    __default_model = 'distance'
    __default_distance_threshold = 10   # In Morse: 1 unit --> 1 meter
    __default_frequency = 800           # MHz
    __default_path_loss_threshold = 115 # dB

    def __init__(self, robot_1, robot_2, **kwargs):
        """ Initialization / Constructor
        Robot names are assumed to be correct! Here, the communication model (and specifications) can be settled.
        Default values are settled, in case the respective arguments are not passed. 
        Kwown arguments: 'model', 'distance_threshold', 'freq' and 'pathloss_threshold'
        Available Models: 'distance', 'line_of_sight', 'free_space_loss'
        Usage examples:
            r0r1 = rcs.RCS('r0', 'r1') 
            r0r1 = rcs.RCS('r0', 'r1', model = "free_space_loss")                 
            r0r1 = rcs.RCS('r0', 'r1', model = "free_space_loss", freq = 800)
            r0r1 = rcs.RCS('r0', 'r1', model = "free_space_loss", pathloss_threshold = 120)
            ...
            r0r1 = rcs.RCS('r0', 'r1', model = "free_space_loss", freq = 800, pathloss_threshold = 120)
            r0r1 = rcs.RCS('r0', 'r1', model = "distance", pathloss_threshold = 100)

            Of course, the last example doesn't make sense because the model 'distance' is not related with the loss threshold.
            So, this method has to be used consciously.
            Distance Threshold --> In Morse: 1 unit = 1 meter
            Frequency --> MHz
            Path Loss Threshold --> dB """

        self.morse = pymorse.Morse()
        self.__r1 = robot_1
        self.__r2 = robot_2
        self.__model = None
        self.__distance_threshold = None
        self.__frequency = None
        self.__pathloss_threshold = None
        self.set_model_specifications(**kwargs)
        
    
    def __del__(self):
        """ Destructor """
        self.morse.close()
        logger.info('Morse socket closed')        


    def can_communicate(self):
        """ This public method returns 'True' or 'False' if the 2 robots can communicate or not. """
                
        if self.__model == 'distance':
            return self.__simulate_comm_distance()
        elif self.__model == 'line_of_sight':
            return self.__simulate_comm_lineofsight()
        elif self.__model == 'free_space_loss':
            return self.__simulate_comm_freespaceloss()
        else:
            logger.debug("An error occurred in the 'Class -> RCS.can_communicate() method.")
            return False


    def set_model_specifications(self, **kwargs):
        """ This public method set a communication model and its specifications between the 2 robots.
            Kwown arguments: 'model', 'freq' and 'pathloss_threshold'
            Usage examples:\
                    r0r1.set_model_specifications(model = "free_space_loss", freq = 800, pathloss_threshold = 120))
                    r0r1.set_model_specifications(freq = 500)
                    ...
                    r0r1.set_model_specifications(model = "distance", pathloss_threshold = 100)

            Of course, the last example doesn't make sense because the model 'distance' is not related with the loss threshold.
            So, this method has to be used consciously.                
            Distance Threshold --> In Morse: 1 unit = 1 meter
            Frequency --> MHz
            Path Loss Threshold --> dB """
        
        if ("model" in kwargs) and self.model_exists(kwargs["model"]):
            self.__model = kwargs["model"]
        else:
            if self.__model is None:
                self.__model = self.__default_model
            #else:  Keeping the previous one

        logger.info("Communication model '%s' was settled between '%s' and '%s'."\
                %(self.__model.upper(), self.__r1.upper(), self.__r2.upper()))
        #---------------------------------------

        if "distance_threshold" in kwargs:
            self.__distance_threshold = kwargs["distance_threshold"]
        else:
            if self.__distance_threshold is None:
                self.__distance_threshold = self.__default_distance_threshold
            #else: Keeping the previous value
        
        logger.info("Distance Threshold (m): %i" %self.__distance_threshold)
        #---------------------------------------

        if "freq" in kwargs:
            self.__frequency = kwargs["freq"]
        else:
            if self.__frequency is None:
                self.__frequency = self.__default_frequency
            #else: Keeping the previous value

        logger.info("Frequency (MHz): %i" %self.__frequency)
        #---------------------------------------
        
        if "pathloss_threshold" in kwargs:
            self.__pathloss_threshold = kwargs["pathloss_threshold"]
        else:
            if self.__pathloss_threshold is None:
                self.__pathloss_threshold = self.__default_path_loss_threshold
        
        logger.info("Path Loss Threshold (dB): %s" %self.__pathloss_threshold)


    def model_exists(self, model):
        """ This public method returns 'True' or 'False' if the model exists or not in this module. """
        if model.lower() in self.__models:  return True
        else:                               return False


    def get_model(self):
        """ This public method returns the current communication model between the 2 robots. """
        return self.__model
    
    
    def __simulate_comm_distance(self):
        """ If the distance between the 2 robots is greater than DISTANCE THRESHOLD, they can't communicate (return False). """

        result = self.__get_distance_and_lineofsight()
        if result[0] < self.__distance_threshold: 
            logger.info("Communications Simulator: Robots '%s' and '%s' can communicate\
                    because DISTANCE is: %i (<%i)"%(self.__r1.upper(), self.__r2.upper(), result[0], self.__distance_threshold))
            return True
            
        else:  
            logger.info("Communications Simulator: Robots '%s' and '%s' CANNOT communicate\
                    because DISTANCE is: %i (>=%i)"%(self.__r1.upper(), self.__r2.upper(), result[0], self.__distance_threshold))
            return False


    def __simulate_comm_lineofsight(self):
        """ If the 2 robots can see each other, they can communicate (return True). """
        
        result = self.__get_distance_and_lineofsight()
        if result[1]:
            logger.info("Communications Simulator: Robots '%s' and '%s' can communicate\
                    because LINE-of-SIGHT is: %s"%(self.__r1.upper(), self.__r2.upper(), result[1]))
        else:            
            logger.info("Communications Simulator: Robots '%s' and '%s' CANNOT communicate\
                    because LINE-of-SIGHT is: %s"%(self.__r1.upper(), self.__r2.upper(), result[1]))
        return result[1]


    def __simulate_comm_freespaceloss(self):
        """ If the path loss is greater than PATHLOSS THRESHOLD, they can't communicate (return False)
        Formula obtained from: 'Propagation Path Loss Models for Mobile Communication', Klozar and Prokopec, IEEE 2011
        This formula doesn't consider effects of propagation in real environment, i. e., with no distortion. """
        # TODO: When the antennas will be defined on Morse, then get the gain Gt, Gr and apply the generic formula (paper 2002)


        # frequency in MHz:
        result = self.__get_distance_and_lineofsight()
        loss = 32.44 + 20*math.log(self.__frequency, 10) + 20*math.log(result[0], 10)

        if loss < self.__pathloss_threshold: 
            
            logger.info("Communications Simulator: Robots '%s' and '%s' can communicate\
                    because PATH LOSS is: %i (<%i)"%(self.__r1.upper(), self.__r2.upper(), loss, self.__pathloss_threshold))
            return True
            
        else:  
            logger.info("Communications Simulator: Robots '%s' and '%s' CANNOT communicate\
                    because PATH LOSS is: %i (>=%i)"%(self.__r1.upper(), self.__r2.upper(), loss, self.__pathloss_threshold))
            return False

    def __get_distance_and_lineofsight(self):
        """ Return a list with 2 arguments: distance, (boolean) line of sight. """

        try:
                return self.morse.rpc('communication', 'distance_and_view', self.__r1, self.__r2)
        
        except  pymorse.MorseServerError as mse:
            print('Oups! An error occurred!')
            print(mse)

    def print_models(self):
        # This method was only for debugging...
        print("\n---------------------------------\nAvailable models:\n\t")
        print("\n".join(self.__models))
        print("\n---------------------------------\n")



