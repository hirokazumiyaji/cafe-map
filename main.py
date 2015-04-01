#!/usr/bin/env python
# coding: utf-8
from __future__ import absolute_import, unicode_literals, print_function
from itertools import groupby
import os

try:
    import json
except ImportError:
    from django.utils import simplejson as json

import webapp2
import jinja2

from models import Station, Store

template = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class RootHandler(webapp2.RequestHandler):

    def get(self):
        self.response.write(template.get_template("views/index.html").render({}))


class SearchHandler(webapp2.RequestHandler):

    def get(self):
        station_name = self.request.get("station")
        genre = self.request.get("genre")

        station = Station.get(station_name)

        self.response.headers[b"Content-Type"] = b"application/json; charset=utf-8"
        data = json.dumps(station.to_dict(genre), ensure_ascii=False)
        self.response.write(data)


class StoreHandler(webapp2.RequestHandler):

    def post(self):
        import urllib
        data = urllib.unquote(self.request.body)
        data = json.loads(data)
        stations = data["stations"]
        stores = data["stores"]

        stores_by_station = {}
        for k, v in groupby(stores, lambda x: x["station_id"]):
            stores_by_station[k] = list(v)

        for station in stations:
            _stores = stores_by_station[station["id"]]
            s = Station(name=station["name"].encode("utf-8"),
                        lat=station["lat"],
                        lng=station["lng"],
                        stores=[
                            Store(name=x["name"].encode("utf-8"),
                                  genre=x["genre"].encode("utf-8"),
                                  lat=x["lat"],
                                  lng=x["lng"])
                            for x in _stores
                        ])
            s.put()

        self.response.headers[b"Content-Type"] = b"application/json; charset=utf-8"
        self.response.write(json.dumps({"status": "success"}, ensure_ascii=False))


app = webapp2.WSGIApplication(
    [
        ("/", RootHandler),
        ("/search", SearchHandler),
        ("/store", StoreHandler),
    ],
    debug=True)
