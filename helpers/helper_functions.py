import time
import logging


def wait(seconds, reason=""):
    print(f"等待{seconds}秒，{reason}")
    return time.sleep(seconds)


def loginfo(message=""):
    logging.info({message})

def logdebug(message=""):
    logging.debug({message})
