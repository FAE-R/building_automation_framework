import logging

# Function to configure a custom logger.
def logger_conf(name):
    logger = logging.getLogger(name)

    c_handler = logging.StreamHandler()  
    f_handler = logging.FileHandler(name + '.log')  
    
    c_handler.setLevel(logging.WARNING)  
    f_handler.setLevel(logging.ERROR)  

    c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')  
    f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')  
    c_handler.setFormatter(c_format)  
    f_handler.setFormatter(f_format)  

    logger.addHandler(c_handler)
    logger.addHandler(f_handler)
    
    return logger
