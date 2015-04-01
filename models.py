# coding: utf-8
from __future__ import absolute_import, unicode_literals, print_function
from google.appengine.ext import ndb

from functional import cached_property


class Store(ndb.Model):
    name = ndb.StringProperty()
    genre = ndb.StringProperty()
    lat = ndb.FloatProperty()
    lng = ndb.FloatProperty()

    def to_dict(self):
        return {
            "name": self.name,
            "lat": self.lat,
            "lng": self.lng,
        }


class Station(ndb.Model):
    name = ndb.StringProperty()
    lat = ndb.FloatProperty()
    lng = ndb.FloatProperty()
    stores = ndb.StructuredProperty(Store, repeated=True)

    @classmethod
    def get(cls, name):
        return cls.query(Station.name==name.encode('utf-8')).get()

    def to_dict(self, genre=None):
        return {
            "station": {
                "name": self.name,
                "lat": self.lat,
                "lng": self.lng,
            },
            "stores": [
                store.to_dict()
                for store in self.stores
                if genre and (genre == "all" or genre == store.genre)
            ],
        }
