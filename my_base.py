#!/usr/bin/env python3
"""Python utility template"""

import os
import sys
import logging
import datetime
import argparse
import configparser
from logging.handlers import RotatingFileHandler
from logging import Formatter


CONFIG_FILE = "config_file"
logger = logging.getLogger("my_app")


# --------------------------------------------------
def prog_log_init(params):
    """Init logging"""

    if "logger_level" in params.keys():
        logger_level = params["logger_level"]
    else:
        logger_level = "error"

    logger_file = params["logger_file"]
    logger_count = params["logger_count"]
    logger_size = params["logger_size"]

    if logger_level == "debug":
        logging.basicConfig(level=logging.DEBUG)
    elif logger_level == "info":
        logging.basicConfig(level=logging.INFO)
    elif logger_level == "error":
        logging.basicConfig(level=logging.ERROR)
    else:
        logging.basicConfig(level=logging.INFO)

    formatter = logging.Formatter("%(asctime)s - %(levelname)s : %(message)s")

    # log to file if log file is specified and disable console logging
    if logger_file:
        log_hdl = logging.handlers.RotatingFileHandler(
            filename=logger_file,
            mode="a",
            delay=False,
            maxBytes=int(logger_size),
            backupCount=int(logger_count),
        )
        log_hdl.setFormatter(formatter)
        logger.addHandler(log_hdl)

        # Disable terminal output
        sys.stdout = open(os.devnull, "wt")
        sys.stderr = open(os.devnull, "wt")
    else:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)

    return logger


# --------------------------------------------------
def parse_config_file():
    """Read and parse config file"""

    config_params = {}

    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)

    # Parse module_1 config
    config_params["config_1"] = config["module_1"]["config_1"]

    # Parse module_2 config
    config_params["config_2"] = config["module_2"]["config_2"]
    if config["module_2"]["var_default_value"]:
        config_params["var_default_value"] = int(config["module_2"]["var_default_value"])

    # Parse logging related config
    config_params["logger_file"] = config["logging"]["log_file"]
    config_params["logger_count"] = config["logging"]["log_file_count"]
    config_params["logger_size"] = config["logging"]["log_file_size"]

    return config_params


# --------------------------------------------------
def get_args():
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        description="arg-xxx Description",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument("arg_xxx_name", metavar="str", nargs="+", help="About arg-xxx")

    #    parser.add_argument('-s',
    #            '--sorted',
    #            action='store_true',
    #            help='Sort args-xxx')

    parser.add_argument(
        "-l",
        "--log_level",
        help="Log level [debug|info|error] (default info)",
        type=str,
        required=False,
    )

    parser.add_argument(
        "-o",
        "--log_output",
        help="Log output file (default console)",
        type=str,
        required=False,
    )

    args = parser.parse_args()
    if args.log_level and args.log_level not in ["debug", "info", "error"]:
        parser.print_help()
        sys.exit(1)

    return parser.parse_args()


# --------------------------------------------------
def base_init():
    """Init Module"""

    global logger

    # Read and parse config file
    prog_params = parse_config_file()

    # Parse arguments
    args = get_args()
    arg_xxx = args.arg_xxx_name

    #    if arg_xxx.sorted:
    #        arg_xxx.sort()

    # Override default config with command line args
    if args.log_output:
        prog_params["logger_file"] = args.log_output

    if args.log_level:
        prog_params["logger_level"] = args.log_level

    # Initialize logging
    logger = prog_log_init(prog_params)


# --------------------------------------------------
def prog_test():
    """Basic Test"""

    logger.debug("This is debug\n")
    logger.error("This is error\n")


# --------------------------------------------------
if __name__ == "__main__":
    base_init()
    prog_test()
