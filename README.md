__Diktyo__
==

Description
----
The __Diktyo__ is tool to manage multiple network devices 
via ssh/telnet. Based on libraries [netmiko](https://github.com/ktbyers/netmiko)

Installation
----
```
git clone https://github.com/DimaTverdoy/diktyo
cd diktyo
pip install -r requirements.txt
```

Settings
----
All configuration happens in a configuration file `conf.yaml`
Example configuration:
```yaml
devices:
  - remote:
      device_type: linux
      host: 12.41.12.93
      username: ubuntu
      password: root
  - cisco:
      device_type: cisco_ios
      host: 192.168.1.1
      username: user
      password: userpass
      secret: enablepass
      port: 2022
commands:
    - ls
    - pwd
```

Help
----
```
$ python src/main.py -h
usage: main.py [-h] [-e] [-m]

Tool to manage multiple network devices via ssh/telnet

optional arguments:
  -h, --help         show this help message and exit
  -e, --export       Export output to ./output
  -m, --multithread  Launching each device in a new thread

```