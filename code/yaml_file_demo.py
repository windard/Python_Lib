# -*- coding: utf-8 -*-
import yaml


if __name__ == '__main__':
    data = {
        'name': 'ACME',
        'object': {'complex': True, 'description': 'complex object'},
        'shares': 100,
        'price': 542.23,
        'others': ["first thing", "second thing", "third thing"],
    }
    with open('yaml_test.yaml', 'w') as f:
        raw_yaml_data = yaml.safe_dump(data, f)

    with open('yaml_test.yaml', 'r') as f:
        print(yaml.safe_load(f))
