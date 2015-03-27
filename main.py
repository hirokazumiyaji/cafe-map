#!/usr/bin/env python
# coding: utf-8
from __future__ import absolute_import, unicode_literals, print_function
import csv
import logging
import os
import sys
import wsgiref.handlers
from cStringIO import StringIO

from google.appengine.api import urlfetch

from django.utils import simplejson
from google.appengine.ext import db, webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from models import Station, Store

ROOT_DIR = os.path.dirname(__file__)


class MainHandler(webapp.RequestHandler):

    def get(self):
        data = {}
        path = os.path.join(root_dir, "views/index.html")
        self.response.out.write(template.render(path, data))


class SearchHandler(webapp.RequestHandler):

    def get(self):
        station_name = self.request.get("station")
        genre = self.request.get("genre")

        station = Station.get(station_name)

        self.response.content_type = "application/json"
        simplejson.dump(
            station.to_json(genre),
            self.response.out,
            ensure_ascii=False)


class RegistHandler(webapp.RequestHandler):

    def get(self):
        path = os.path.join(root_dir, "views/regist.html")
        self.response.out.write(template.render(path, {}))

    def post(self):
        try:
            datatype = self.request.get("datatype")
            csvBuffer = csv.reader(StringIO(self.request.get("file")))
            if datatype == "Stores":
                for row in csvBuffer:
                    store = Store(
                        station=row[0].decode("utf-8"),
                        name=row[1].decode("utf-8"),
                        genre=unicode(row[2], "cp932"),
                        lat=unicode(row[3], "cp932"),
                        lng=unicode(row[4], "cp932")
                    )
                    store.put()
            else:
                for row in csvBuffer:
                    station = Station(
                        name=row[0].decode("utf-8"),
                        lat=row[1].decode("utf-8"),
                        lng=unicode(row[2], "cp932")
                    )
                    station.put()
        except Exception, e:
          pass

        self.redirect("/regist")


application = webapp.WSGIApplication([("/", MainHandler),
                                      ("/search", SearchHandler),
                                      ("/regist", RegistHandler)],
                                     debug=True)


logging.getLogger().setLevel(logging.DEBUG)


def main():
    run_wsgi_app(application)


if __name__ == "__main__":
    main()
