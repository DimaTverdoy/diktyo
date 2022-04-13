"""
Module for config

Example:
    config = config.parse_from_yaml()

    for device in config.devices:
        print(f"Device: {device.host}")
"""
import argparse
import os

import yaml
from loguru import logger
from typing import NamedTuple, List

from yaml.scanner import ScannerError

from device import Device


class Config(NamedTuple):
    devices: List[Device]
    commands: List[str]
    export: bool
    multi: bool


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Tool to manage multiple network devices via ssh/telnet")

    parser.add_argument("-e", "--export", dest="export", action='store_true',
                        default=False, help="Export output to ./output")
    parser.add_argument("-m", "--multithread", dest="multi", action='store_true',
                        default=False, help="Launching each device in a new thread")

    return parser.parse_args()


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

    args = parse_args()
    config = Config(devices=[], commands=conf['commands'], export=args.export, multi=args.multi)

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
