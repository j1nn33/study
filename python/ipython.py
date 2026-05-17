### FOR FAST TEST

import logging


BASE_FORMAT_LOG = "[%(name)s][%(levelname)-6s] %(message)s"
FILE_FORMAT_LOG = "[%(asctime)s]" + BASE_FORMAT_LOG

logging.basicConfig(level=logging.DEBUG,  format= FILE_FORMAT_LOG)
logging.info('Start of program')
# запись сообщений в файл
# logging.basicConfig(filename="sample.log", level=logging.INFO)
def logging_in_func (n):
    total = 1
    logging.info  ('Start logging in functoin the argument is %s' %(n))
    logging.debug ('Output DEBUG message from function var in func is' + str(total))
    logging.info  ('end logging in functoin')
    return 
   
logging_in_func(3)
logging.info ('End of program')


