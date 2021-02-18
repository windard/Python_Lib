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
- many 可以将转化为在 nested 中传入 object list
- `load_only` 或者 `dump_only` 都是字面意思
- attribute 别名，这个就很神奇。在 `load` 中表示 `load_to`, 在 `dump` 中表示 `dump_from`
- 在 python3 中，marshmallow 统一去除了 `load_from` 和 `dump_to` 字段，用 `data_key` 来表述
- 在 python3 中，missing 和 default 的作用时间发生了改变，传入`missing={}` load 的结果就是`{}` 而不是会继续 `deserialize`
- 且不说在 python3 中默认有多的参数就会报错，需要设置 `unknown=EXCLUDE` 这种问题
- 还有 webargs 在 python3 中 location 只能从一个地方去取，不能从 fields 中定义这种问题
- 真的是想做好开源产品么？为什么觉得越改问题越多呢？真想把版本直接回滚到从前
- missing 的问题，很严重，改变执行时机的问题，举两个具体的例子，nested 的 missing={}. 不会去继续解析参数的 missing，Datetime 的 missing，不会去继续解析参数,而是直接返回 Datetime 类型，如此重重，不兼容的地方太多了。
- 又发现 marshmallow 的一个坑，`fields.URL` 的 URL 域名不支持下划线(underscore), 就是`ww_w.baidu.com` 是不允许的，但是实际上 URL 现在已经可以使用下划线了。不过 DNS name 已经明确不支持下划线了，就不要再浪费时间在这上面。

除了基本数据类型，如 Str, Int, Float, Dict, List 等，还有组合结构类型 Nested 和函数转化 Function 等。

在 Function 中，deserialize 函数的参数是当前字段的值，serialize 的参数却是整个结构体的值。

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
