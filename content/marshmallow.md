## marshmallow

数据转换库，一个将 python 简单数据格式如 dict，list 等转化为复杂对象的序列化和反序列化库。

### 序列化

Serializing，将一个对象转化为 dict 或者 string ，使用方法 `dump` 或者 `dumps`。

在 `dump` 的时候，如果有缺省值使用 `default`，如果需要字段更名使用 `dump_to`

序列化的时候，一般用于数据库对象的请求响应对外输出。

### 反序列化

Deserializing，将一个 dict 或者 string 转化为对象，使用方法 `load` 或者 `loads`。

在 `load` 的时候，如果有缺省值使用 `missing`，如果需要字段更名使用 `load_from`

反序列化的时候，可以使用 `validate` 进行参数校验，一般用于请求参数校验。

反序列化的时候，可以使用 `required` 表示参数必填，一般用于请求参数校验。

在构造对象时，使用 `post_load` 装饰构造函数，生成 orm 对象，否则默认转化结果还是 dict 。

### 通用参数
- only 只保留部分字段
- exclude 排除部分字段
- strict 参数无效时，是否报错
- error_messages 自定义错误信息
- many 转化为 list
- attribute 别名，这个就很神奇。在 `load` 中表示 `load_to`, 在 `dump` 中表示 `dump_from`
- load_only 或者 `dump_only` 字面意思

除了基本数据类型，如 Str, Int, Float, Dict, List 等，还有组合结构类型 Nested 和函数转化 Function 等。

### 实例

```

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


```


```
# coding=utf-8


from datetime import datetime
from marshmallow import Schema, fields, pprint
from fields import ConstChoice, ChoiceBase


class OpenApiAppScene(ChoiceBase):
    online = 1
    offline = 2

    __choices__ = ((online, u'1111'), (offline, u'22222'))


class ArtistSchema(Schema):
    name = fields.Str()
    location = fields.List(fields.Str())


class AlbumSchema(Schema):
    title = fields.Str()
    release_date = fields.Date(required=True)
    artist = fields.Nested(ArtistSchema())
    response = fields.Function(serialize=lambda x: "response data")
    request = fields.Function(serialize=lambda x: x.a, deserialize=lambda x: "request data")
    scene = ConstChoice(OpenApiAppScene, validate_only=True)
    group_type = fields.Int(load_from="real_group_type")
    real_app_type = fields.Int(dump_to="app_type")
    email_addr = fields.Str(attribute="email")


if __name__ == '__main__':
    bowie = dict(name='David Bowie', location=["Beijing", "Shanghai"])
    album = dict(artist=bowie, title="Hunky Dory", release_date=datetime.now(), request="...", scene=2,
                 group_type=1, real_group_type=2, real_app_type=1, email="windard@qq.com")

    schema = AlbumSchema() # type: Schema

    # 将一个 object 转换成 dict , 属于 serialize 在 pack response 中
    # 在转换成 dict 的时候，会去取值，如果没有，就会返回 missing_, 然后再返回值里也不展示
    # 如果想要一定展示出来，需要加上 default=None
    # dump 的时候改字段用 dump_to
    dump_result = schema.dump(album)
    pprint(dump_result, indent=2)
    print dump_result.data

    print '-'*80
    # 讲一个 dict 转换成 object, 属于 deserialize 在 request 里或者 转化里使用
    # 使用 load 的时候，原始数据中必须存在这个字段，如果原始字段不存在，则没有，如果没有 deserialize 函数，则返回原始值。
    # 如果没有原始值，则不会输入，否则可以加上 missing=None
    # load 的时候改字段用 load_from 或者 attribute
    load_result = schema.load(album)
    pprint(load_result, indent=2)
    print load_result.data

    # print schema.fields

```

### 参考文档

[渣翻marshmallow文档](https://www.jianshu.com/p/594865f0681b)
