import threading

from config import parse_from_yaml, Config
from manager import Manager

from loguru import logger


config = parse_from_yaml()
logger.info("Start program")

def run_multi(conf: Config):
    manager_multi = Manager(conf=conf)

    manager_multi.connect()
    manager_multi.exec()
    manager_multi.display_output()
    manager_multi.close()


if config.multi:
    threads = []
    for device in config.devices:
        conf_thread = config._asdict()
        conf_thread['devices'] = [device]
        conf_thread = Config(**conf_thread)

        thread = threading.Thread(target=run_multi, args=(conf_thread,))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()
else:
    manager = Manager(conf=config)

    manager.connect()
    manager.exec()
    manager.display_output()
    manager.close()
