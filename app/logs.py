import logging
import coloredlogs

import os

if not os.path.exists("logs"):
    os.makedirs("logs")

fieldstyle = {'asctime': {'color': 'green'},
              'levelname': {'bold': True, 'color': 'white'},
              'filename': {'color': 'cyan'},
              'funcName': {'color': 'blue'},
              'lineno': {'color': 'white'}}

levelstyles = {'critical': {'bold': True, 'color': 'red'},
               'debug': {'color': 'green'},
               'error': {'color': 'red'},
               'info': {'color': 'magenta'},
               'warning': {'color': 'yellow'}}


def get_logger():
    mylogs = logging.getLogger(__name__)

    info = logging.FileHandler("logs/info.log",mode="a+", encoding="utf-8")
    info.setLevel(logging.INFO)

    cric_file = logging.FileHandler("logs/error.log",mode="a+", encoding="utf-8")
    cric_file.setLevel(logging.ERROR)

    cric_file.setFormatter(
        logging.Formatter("%(asctime)s [%(levelname)s] - [%(filename)s > %(funcName)s() > %(lineno)s] - %(message)s"))

    debug = logging.FileHandler("logs/debug.log", mode="a+", encoding="utf-8")
    debug.setLevel("DEBUG")

    mylogs.setLevel(logging.DEBUG)

    coloredlogs.install(level=logging.DEBUG,
                        logger=mylogs,
                        fmt='%(asctime)s [%(levelname)s] - %(message)s',
                        datefmt='%H:%M:%S',
                        field_styles=fieldstyle,
                        level_styles=levelstyles)

    mylogs.addHandler(info)
    mylogs.addHandler(cric_file)
    mylogs.addHandler(debug)
    return mylogs


logger = get_logger()