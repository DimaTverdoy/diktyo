import config
from manager import Manager

config = config.parse_from_yaml()

for device in config.devices:
    print(f"Device: {device.host}")

manager = Manager(conf=config)

manager.connect()
manager.exec()
manager.display_output()
manager.close()
