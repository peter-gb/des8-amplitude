from modules.log_initialise import logging_initialise




# initialise logging
logger = logging_initialise()

# send a logging message to say we are up and running
logger.info("Logger succesfully initialised - let's go!")
