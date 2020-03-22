# coding=utf-8


from datetime import datetime
from marshmallow import Schema, fields, pprint


class ArtistSchema(Schema):
	name = fields.Str()
	location = fields.List(fields.Str())


class AlbumSchema(Schema):
	title = fields.Str()
	release_date = fields.Date()
	artist = fields.Nested(ArtistSchema())
	response = fields.Function(serialize=lambda x: "response data")
	request = fields.Function(serialize=lambda x:x.a, deserialize=lambda x: "request data")


bowie = dict(name='David Bowie', location=["Beijing", "Shanghai"])
album = dict(artist=bowie, title="Hunky Dory", release_date=datetime.now(), request="...")

schema = AlbumSchema()

# 将一个 object 转换成 dict , 属于 serialize 在 pack response 中
# 在转换成 dict 的时候，会去取值，如果没有，就会返回 missing_, 然后再返回值里也不展示
dump_result = schema.dump(album)
pprint(dump_result, indent=2)
print dump_result.data

# 讲一个 dict 转换成 object, 属于 deserialize 在 request 里或者 转化里使用
# 使用 load 的时候，原始数据中必须存在这个字段，如果原始字段不存在，则没有，如果没有 deserialize 函数，则返回原始值。
load_result = schema.load(album)
pprint(load_result, indent=2)
print load_result.data

# print schema.fields
