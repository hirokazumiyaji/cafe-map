# coding: utf-8
from __future__ import absolute_import, unicode_literals, print_function
from google.appengine.ext import db

from functional import cached_property


class Store(db.Model):
    station_id = db.IntegerProperty()
    name = db.StringProperty()
    genre = db.StringProperty()
    lat = db.FloatProperty()
    lng = db.FloatProperty()

    @classmethod
    def find(cls, station_id):
        return db.GqlQuery("SELECT * FROM Store WHERE station_id = :1", station_id)

    def to_dict(self):
        return {
            "name": self.name,
            "lat": self.lat,
            "lng": self.lng,
        }


class Station(db.Model):
    id = db.IntegerProperty()
    name = db.StringProperty()
    lat = db.FloatProperty()
    lng = db.FloatProperty()

    @property
    def stores(self):
        return list(Store.find(self.id))

    @classmethod
    def get(cls, name):
        return db.GqlQuery("SELECT * FROM Station WHERE name = :1", name).fetch(1)[0]

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
