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


## @brief This class aims to simulate if 2 robots can communicate each other according to specific models.
# @author Paulo Simões
class RCS():
    
    ## @details Tuple including all the communication models available in this module.
    __models = ('distance', 'line_of_sight', 'free_space_loss')
    ## @details Default communication model in case it is not specified in the constructor or set_model_specifications() method.
    __default_model = 'distance'
    ## @brief In Morse: 1 unit --> 1 meter
    # @details Default distance threshold in case it is not specified in the constructor or set_model_specifications() method.
    # Only used in the 'distance' communication model.
    __default_distance_threshold = 10
    ## @brief Units: MHz
    # @details Default frequency in case it is not specified in the constructor or set_model_specifications() method.
    # Only used in the 'analytical' communication model.
    __default_frequency = 800
    ## @brief Units: dB
    # @details Default communication model in case it is not specified in the constructor or set_model_specifications() method.
    # Only used in the 'analytical' communication model.
    __default_path_loss_threshold = 45

    
    ## @param[in] robot_1 Name of one robot
    # @param[in] robot_2 Name of the other robot
    # @param[in] kwargs See the method set_model_specifications() for more information.
    # @details Robot names are assumed to be correct! Here, the communication model (and specifications) can be settled.
    # Default values are settled, in case the respective arguments are not passed.
    def __init__(self, robot_1, robot_2, **kwargs):

        ## @brief Morse connection: access to Morse services and data streams
        self.__morse = pymorse.Morse()
        ## @brief Name of Robot 1
        self.__r1 = robot_1
        ## @brief Name of Robot 2
        self.__r2 = robot_2
        ## @brief Name of the communication model applied between the 2 robots
        self.__model = None
        ## @brief In Morse: 1 unit --> 1 meter
        self.__distance_threshold = None
        ## @brief Units: MHz
        self.__frequency = None
        ## @brief Units: dB
        self.__pathloss_threshold = None

        self.set_model_specifications(**kwargs)
        
    ## @details This method closes the connection with the  morse simulation.
    def __del__(self):
        self.__morse.close()
        logger.info('Morse socket closed')        

    ## @return True (False) if the 2 robots can (cannot) communicate according to the established communication model.
    def can_communicate(self):
        if self.__model == 'distance':
            return self.__simulate_comm_distance()
        elif self.__model == 'line_of_sight':
            return self.__simulate_comm_lineofsight()
        elif self.__model == 'free_space_loss':
            return self.__simulate_comm_freespaceloss()
        else:
            logger.debug("An error occurred in the 'Class -> RCS.can_communicate() method.")
            return False

    ## @brief This method sets a communication model and its specifications between the 2 robots.
    # @param[in] kwargs 'model'
    # @param[in] kwargs 'distance_threshold' (meters)
    # @param[in] kwargs 'freq' (MHz)
    # @param[in] kwargs 'pathloss_threshold' (dB)
    # @details Available Models: 'distance', 'line_of_sight', 'free_space_loss'
    # @details Default values are settled, in case the respective arguments are not passed.
    def set_model_specifications(self, **kwargs):
        
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

    ## @param[in] model String containing the communication model.
    # @return True (False) if the model exists (or not) in this module.
    def model_exists(self, model):
        if model.lower() in self.__models:  return True
        else:                               return False

    ## @return A string with the communication model currently settled between the 2 robots.
    def get_model(self):
        return self.__model
    
    ## @return True (False) if the distance between the 2 robots is less (greater or equal) than DISTANCE THRESHOLD.    
    def __simulate_comm_distance(self):
        result = self.__get_distance_and_lineofsight()
        if result[0] < self.__distance_threshold: 
            logger.info("Communications Simulator: Robots '%s' and '%s' can communicate\
                    because DISTANCE is: %i (<%i)"%(self.__r1.upper(), self.__r2.upper(), result[0], self.__distance_threshold))
            return True
            
        else:  
            logger.info("Communications Simulator: Robots '%s' and '%s' CANNOT communicate\
                    because DISTANCE is: %i (>=%i)"%(self.__r1.upper(), self.__r2.upper(), result[0], self.__distance_threshold))
            return False

    ## @return True (False) if the 2 robots are (are not) in line-of-sight.
    def __simulate_comm_lineofsight(self):
        result = self.__get_distance_and_lineofsight()
        if result[1]:
            logger.info("Communications Simulator: Robots '%s' and '%s' can communicate\
                    because LINE-of-SIGHT is: %s"%(self.__r1.upper(), self.__r2.upper(), result[1]))
        else:            
            logger.info("Communications Simulator: Robots '%s' and '%s' CANNOT communicate\
                    because LINE-of-SIGHT is: %s"%(self.__r1.upper(), self.__r2.upper(), result[1]))
        return result[1]

    ## @return True (False) if the path loss is less (greater or equal) than PATHLOSS THRESHOLD.
    # @details Formula obtained from "Propagation Prediction Models for Wireless Communication Systems", IEEE 2002. 
    # @todo When the robot antennas will be defined on Morse, then get the gain Gt and Gr
    def __simulate_comm_freespaceloss(self):
        Gt = 2; Gr = 2; c = 299792458;
        result = self.__get_distance_and_lineofsight()
        wavelength = float(c/(self.__frequency*math.pow(10, 6)))
        loss = float(-10*math.log10((Gt*Gr*math.pow(wavelength, 2))/math.pow(4*math.pi*result[0], 2)))
        if loss < self.__pathloss_threshold: 
            logger.info("Communications Simulator: Robots '%s' and '%s' can communicate\
                    because PATH LOSS is: %i (<%i)"%(self.__r1.upper(), self.__r2.upper(), loss, self.__pathloss_threshold))
            return True
        else:  
            logger.info("Communications Simulator: Robots '%s' and '%s' CANNOT communicate\
                    because PATH LOSS is: %i (>=%i)"%(self.__r1.upper(), self.__r2.upper(), loss, self.__pathloss_threshold))
            return False

    ## @return A list with 2 arguments: distance between the 2 robots, line-of-sight (boolean) 
    def __get_distance_and_lineofsight(self):
        try:
                return self.__morse.rpc('communication', 'distance_and_view', self.__r1, self.__r2)
        except  pymorse.MorseServerError as mse:
            print('Oups! An error occurred!')
            print(mse)
