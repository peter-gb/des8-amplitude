import os
import logging
from datetime import datetime

def logging_initialise():
    """This function initialises the logger, saving to a logs directory, with the timestamp as the file name. No input arguments needed.

    """
    # opted to hardcode logs and timestamp inside the function, rather than requiring arguments to be sent in
    
    # prepare the logging, make a directory and define how the logs will be generated.
    log_dir = 'logs'
    timestamp = datetime.now().strftime('%Y-%m-%d %H-%M-%S')
    os.makedirs(log_dir, exist_ok=True)
    log_filename = f'{log_dir}/{timestamp}.log'

    # configure the logging file and messages
    logging.basicConfig(
        filename = log_filename,
        format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level = logging.INFO
    )

    # create the logger and confirm that it is successfully set up
    return logging.getLogger()