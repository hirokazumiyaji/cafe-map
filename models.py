# coding: utf-8
from __future__ import absolute_import, unicode_literals, print_function
from google.appengine.ext import db

from utils import cached_property


class Station(db.Model):
    name = db.StringProperty()
    lat = db.StringProperty()
    lng = db.StringProperty()

    @cached_property
    def stores(self):
        return db.GqlQuery(
            "SELECT * FROM Store WHERE station = :1",
            self.name).fetch(None)

    @classmethod
    def get(cls, name):
        return db.GqlQuery(
            "SELECT * FROM Station WHERE name = :1",
            name).get()

    def to_json(self, genre=None):
        return {
            "station": {
                "name": self.name,
                "lat": self.lat,
                "lng": self.lng,
            },
            "stores": [
                store.to_json()
                for store in self.stores
                if genre and genre == store.genre
            ],
        }


class Store(db.Model):
    station = db.StringProperty()
    genre = db.StringProperty()
    name = db.StringProperty()
    lat = db.StringProperty()
    lng = db.StringProperty()

    def to_json(self):
        return {
            "name": self.name,
            "genre": self.genre,
            "lat": self.lat,
            "lng": self.lng,
        }
