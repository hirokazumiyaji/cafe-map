#!/usr/bin/env python
# coding: utf-8
import csv
import logging
import os
import sys
import wsgiref.handlers
from StringIO import StringIO

from google.appengine.api import urlfetch

from django.utils import simplejson
from google.appengine.ext import db, webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from models.station import Stations
from models.store import Stores


#from models import Store

class MainHandler(webapp.RequestHandler):

    def get(self):
        data = {}
        path = os.path.join(os.path.dirname(__file__), 'views/index.html')
        self.response.out.write(template.render(path, data))


class SearchHandler(webapp.RequestHandler):

    def get(self):
        station = self.request.get('station')
        genre = self.request.get('genre')
        logging.info(station)
        logging.info(type(station))
        logging.info(genre)
        logging.info(type(genre))
        queryStores = ""

        if genre == u"all":
            logging.info("all")
            queryStores = u"SELECT * FROM Stores WHERE station = '%(reqstation)s'" % {
                'reqstation': station}
        else:
            queryStores = u"SELECT * FROM Stores WHERE station = '%(reqstation)s' AND genre = '%(reqgenre)s'" % {
                'reqstation': station, 'reqgenre': genre}

        logging.info("store query start")
        logging.info(queryStores)
        stores = db.GqlQuery(queryStores)
        logging.info("store query end")
        resultStores = stores.fetch(100)

        logging.info("station query start")
        queryStations = u"SELECT * FROM Stations WHERE name = '%(reqstation)s'" % {
            'reqstation': station}
        stations = db.GqlQuery(queryStations)
        logging.info(queryStations)
        logging.info("station query end")

        resultStations = stations.fetch(1)
        logging.info(resultStations)
        logging.info(resultStations[0].lat.encode('utf-8'))
        resStation = {'name': station, 'lat': resultStations[0].lat.encode(
            'utf-8'), 'lng': resultStations[0].lng.encode('utf-8')}
        logging.info("set reponse sStation")
#    logging.info(stores)
        logging.info(resStation)

        resStores = []
        for store in resultStores:
            resStores.append({"name": store.name, "genre": store.genre.encode(
                'utf-8'), "lat": store.lat.encode('utf-8'), "lng": store.lng.encode('utf-8')})
        data = {'stations': resStation, "stores": resStores}
        logging.info(data)
        self.response.content_tpe = "application/json"
        simplejson.dump(data, self.response.out, ensure_ascii=False)


class RegistHandler(webapp.RequestHandler):

    def get(self):
        data = {}
        path = os.path.join(os.path.dirname(__file__), 'views/regist.html')
        self.response.out.write(template.render(path, data))

    def post(self):
        logging.info("data store regist start")
        try:
            datatype = self.request.get('datatype')
            csvBuffer = csv.reader(StringIO(self.request.get('file')))
            logging.info(csvBuffer)
            logging.info("if start")
            logging.info(datatype)
            if datatype == "Stores":
                logging.info("store start")
                for row in csvBuffer:
                    logging.info(row)
#          logging.info("station=%(station)s, name=%(name)s, genre=%(genre)s, lat=%(lat)s, lng=%(lng)s" % {station: row[0], name: row[1], genre: row[2], lat: row[3], lng: row[4]})
                    store = Stores(
                        station=row[0].decode('utf-8'),
                        name=row[1].decode('utf-8'),
                        genre=unicode(row[2], 'cp932'),
                        lat=unicode(row[3], 'cp932'),
                        lng=unicode(row[4], 'cp932')
                    )
                    store.put()
                    logging.info(store)
                    logging.info("store put")
            else:
                for row in csvBuffer:
                    station = Stations(
                        name=row[0].decode('utf-8'),
                        lat=row[1].decode('utf-8'),
                        lng=unicode(row[2], 'cp932')
                    )
                    station.put()
        except Exception, e:
            logging.error(type(e))

        logging.info("data store regist end")
        self.redirect("/regist")

application = webapp.WSGIApplication([('/', MainHandler),
                                      ('/search', SearchHandler),
                                      ('/regist', RegistHandler)],
                                     debug=True)
logging.getLogger().setLevel(logging.DEBUG)


def main():
    run_wsgi_app(application)

if __name__ == '__main__':
    main()
