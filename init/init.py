#!/usr/bin/env python

import logging
import os

def create_log_dir(log_dir):
    """
    Create Log directory
    """
    try:
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
    except Exception as e:
        # TODO Change the exception type
        raise RuntimeError(
            "Failed to create log directory %s due to %s" % (log_dir, e))

def setup_logging(log_dir='./', log_file='run.log'):
    """
    Sets up Logging handlers and other environment.
    """
    create_log_dir(log_dir)

    log_file_name = os.path.join(log_dir, log_file)
    log_formatter = logging.Formatter(
        '%(asctime)s::%(levelname)s::%(threadName)s::'
        '%(module)s[%(lineno)04s]::%(message)s')
    root_logger = logging.getLogger()
    # if root_logger.handlers:
    #    return
    root_logger.setLevel(logging.DEBUG)
    file_handler = logging.FileHandler(log_file_name)
    file_handler.setFormatter(log_formatter)
    root_logger.addHandler(file_handler)
    return root_logger

setup_logging()
