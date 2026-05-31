### FOR FAST TEST
import os
import logging

LOG_DIR = '/var/log/hive'

log_files = [f for f in os.listdir(LOG_DIR) if 'ranger_audit' in f]

logging.basicConfig(level=logging.INFO, filename=argv[2]+"/app.log", filemode="a",
                    format="%(asctime)s %(levelname)-6s %(message)s")


########