# coding=utf-8


import json
import pickle


def pickle_test():
    data = {
        'name': 'json',
        'profile': 'better'
    }
    pickle_data = pickle.dumps(data)
    print pickle_data
    print pickle.loads(pickle_data)


def json_test():
    data = {
        'name': 'pickle',
        'profile': 'worser'
    }
    json_data = json.dumps(data)
    print json_data
    print json.loads(json_data)


if __name__ == '__main__':
    pickle_test()
    json_test()
