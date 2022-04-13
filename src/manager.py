from loguru import logger
from netmiko import ConnectHandler, NetmikoTimeoutException, NetmikoAuthenticationException

from typing import NamedTuple, Optional, List, Dict
from netmiko.base_connection import BaseConnection

from config import Config
from device import Device

class Connection(NamedTuple):
    ssh: Optional[BaseConnection]
    device: Device
    output: Dict[str, str]

class Manager:
    def __init__(self, conf: Config):
        self.devices: List[Device] = conf.devices
        self.commands: List[str] = conf.commands
        self.connections: List[Connection] = []

    def connect(self):
        for device in self.devices:
            try:
                ssh = ConnectHandler(device_type=device.device_type, host=device.host,
                                     username=device.username, password=device.password, secret=device.secret,
                                     port=device.port)
                self.connections.append(Connection(ssh=ssh, device=device, output={}))
                ssh.enable()
                logger.info(f"Connected to {device.host}")
            except NetmikoTimeoutException as error:
                logger.error(f"Timeout exception connect to {device.host}. Error: {error}")
                exit(1)
            except NetmikoAuthenticationException as error:
                logger.error(f"Authentication exception connect to {device.host}. Error: {error}")
                exit(1)

    def close(self):
        for i in range(len(self.connections)):
            connection = self.connections.pop(i)
            connection.ssh.exit_enable_mode()
            logger.info(f"Closed connection to {connection.device.host}")

    def exec(self):
        for command in self.commands:
            self.__exec_command(command=command)

    def __exec_command(self, command: str):
        for connection in self.connections:
            connection.output[command] = connection.ssh.find_prompt() + command + "\n" + connection.ssh.send_command(command)

    def display_output(self):
        for connection in self.connections:
            for output in connection.output.values():
                logger.info(output)