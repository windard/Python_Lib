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
