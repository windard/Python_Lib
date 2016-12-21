# coding=utf-8

import yaml

with open('yaml_test.yaml', 'r') as f:
	x = yaml.load(f) 
	print x

x = yaml.load(file('yaml_test.yaml'))

print x['name']
print x['spouse']

print x['children'][0]
print x['children'][1]['age']