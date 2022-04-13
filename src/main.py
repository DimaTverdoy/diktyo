import config
from manager import Manager

config = config.parse_from_yaml()
manager = Manager(conf=config)

manager.connect()
manager.exec()
manager.display_output()
manager.close()
