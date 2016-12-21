# coding=utf-8

import yaml

x = {'host': {'ip01': {'two': '192.168.1.254', 'one': '192.168.1.2'}, 'ip00': '192.168.1.1'}, 'soft': {'apache': 2.2, 'php': 5.3, 'mysql': 5.2}, 'name': 'Server'}
f = open("yaml_dump.yaml", "w")

yaml.dump(x, f)

f.close()