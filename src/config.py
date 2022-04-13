"""
Module for config

Example:
    config = config.parse_from_yaml()

    for device in config.devices:
        print(f"Device: {device.host}")
"""

import os

import yaml
from loguru import logger
from typing import NamedTuple, List

from yaml.scanner import ScannerError

from device import Device


class Config(NamedTuple):
    devices: List[Device]
    commands: List[str]


def parse_from_yaml(path="conf.yaml") -> Config:
    if not os.path.exists(path):
        logger.error(f"Config file {path} does not exist")
        exit(1)

    with open(path, 'r') as config_file:
        try:
            conf = yaml.safe_load(config_file)
        except ScannerError as error:
            logger.error(f"Error parse conf. Error: {error}")
            exit(1)

    if 'devices' not in conf:
        logger.error(f"Field devices not found in config")
        exit(1)

    if 'commands' not in conf:
        logger.error(f"Field commands not found in config")
        exit(1)

    config = Config(devices=[], commands=conf['commands'])

    for device in conf['devices']:
        name = list(device)[0]
        device = device[name]

        device.setdefault('port', 22)

        config.devices.append(Device(
            name=name,
            device_type=device['device_type'],
            host=device['host'],
            username=device['username'],
            password=device['password'],
            secret=device.get('secret'),
            port=device['port']
        ))

    return config
