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


bowie = dict(name='David Bowie', location=["Beijing", "Shanghai"])
album = dict(artist=bowie, title="Hunky Dory", release_date=datetime.now())

schema = AlbumSchema()
result = schema.dump(album)
pprint(result, indent=2)

