"""
Device management module

Example:
    config = config.parse_from_yaml()

    manager = Manager(conf=config)

    manager.connect()
    manager.exec()
    manager.display_output()
    manager.close()
"""
import os
import shutil

from loguru import logger
from netmiko import ConnectHandler, NetmikoTimeoutException, NetmikoAuthenticationException

from typing import NamedTuple, List
from netmiko.base_connection import BaseConnection

from config import Config
from device import Device

SAVE_OUTPUT = "output"


class Connection(NamedTuple):
    ssh: BaseConnection
    device: Device
    output: List[str]


class Manager:
    def __init__(self, conf: Config):
        self.devices: List[Device] = conf.devices
        self.commands: List[str] = conf.commands
        self.connections: List[Connection] = []
        self.conf = conf

    def connect(self):
        """ Connects to a host and adds the connection to self.connections """
        for device in self.devices:
            try:
                ssh = ConnectHandler(device_type=device.device_type, host=device.host,
                                     username=device.username, password=device.password, secret=device.secret,
                                     port=device.port)
                ssh.enable()
                self.connections.append(Connection(ssh=ssh, device=device, output=[]))

                logger.info(f"Connected to {device.host}")
            except NetmikoTimeoutException as error:
                logger.warning(f"Timeout exception connect to {device.host}. Error: {error}")
            except NetmikoAuthenticationException as error:
                logger.warning(f"Authentication exception connect to {device.host}. Error: {error}")

    def close(self):
        """ Breaks all connection and removes the connection from self.connections """
        for _ in range(len(self.connections)):
            connection = self.connections.pop(0)
            connection.ssh.exit_enable_mode()
            logger.info(f"Closed connection to {connection.device.host}")

    def exec(self):
        """ Runs all commands on all devices """
        for command in self.commands:
            self.__exec_command(command=command)

    def __exec_command(self, command: str):
        """ Runs one command on all devices """
        for connection in self.connections:
            connection.output.append(connection.ssh.find_prompt()
                                     + command + "\n" + connection.ssh.send_command(command))

    def display_output(self):
        """ Export output from all devices """
        for connection in self.connections:
            for output in connection.output:
                logger.info(output)

        if self.conf.export:
            self.save_output()

    def save_output(self):
        if os.path.exists(SAVE_OUTPUT):
            shutil.rmtree(SAVE_OUTPUT)
        os.mkdir(SAVE_OUTPUT)

        for connection in self.connections:
            with open(os.path.join(SAVE_OUTPUT, connection.device.host), "w") as file:
                for output in connection.output:
                    file.write(output + '\n')