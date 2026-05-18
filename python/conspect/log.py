### логирование в коде пример 

import logging


BASE_FORMAT_LOG = "[%(name)s][%(levelname)-6s] %(message)s"
FILE_FORMAT_LOG = "[%(asctime)s]" + BASE_FORMAT_LOG
# 
logging.basicConfig(level=logging.DEBUG,  format= FILE_FORMAT_LOG)

x = 3
y = 3

logging.info(f"The values of x and y are {x} and {y}.")
try:
    x/y
    logging.info(f"x/y successful with result: {x/y}.")
except ZeroDivisionError as err:
    logging.error("ZeroDivisionError",exc_info=True)
	

# [2026-05-17 17:16:52,027][root][INFO  ] The values of x and y are 3 and 3.
# [2026-05-17 17:16:52,027][root][INFO  ] x/y successful with result: 1.0.

x = 3
y = 0

logging.info(f"The values of x and y are {x} and {y}.")
try:
    x/y
    logging.info(f"x/y successful with result: {x/y}.")
except ZeroDivisionError as err:
    logging.error("ZeroDivisionError",exc_info=True)

# [2026-05-17 17:17:44,844][root][INFO  ] The values of x and y are 3 and 0.
# [2026-05-17 17:17:44,844][root][ERROR ] ZeroDivisionError
# Traceback (most recent call last):
#   File "/home/tooks/repo/study/python/conspect/log.py", line 30, in <module>
#     x/y
# ZeroDivisionError: division by zero