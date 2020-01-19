# coding=utf-8

from pprint import pprint
from marshmallow import Schema, fields, pprint, post_load


class User(object):
    """docstring for User"""
    def __init__(self, created_at, email, name):
        self.created_at = created_at
        self.email = email
        self.name = name


class UserSchema(Schema):
    created_at = fields.Date()
    email = fields.Str()
    name = fields.Str()
    age = fields.Int()

    # @post_load
    # def make_user(self, data):
        # return User(**data)

user_data = {
    'created_at': '2014-08-11T05:26:03.869245',
    # 'email': u'ken@yahoo.com',
    'name': u'Ken',
    'age': '20-'
}
schema = UserSchema()
result = schema.load(user_data)
pprint(result.data)
print(type(result.data))
print(result)
print(type(result))
# {'name': 'Ken',
#  'email': 'ken@yahoo.com',
#  'created_at': datetime.datetime(2014, 8, 11, 5, 26, 3, 869245)},


print result.data['name']
result.data['name'] = 'windard'
print result
print result.data.name

result.data['email'] = result.data.get('email', None)
print type(result.data['age'])

