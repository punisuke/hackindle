import logzero


def get_logger(name: str):
    logzero.logfile(f"./log/{name}.log")
    return logzero.logger
