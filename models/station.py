#!/usr/bin/ env python
# -*- coding: utf-8 -*-

from google.appengine.ext import db

class Stations(db.Model):
  name = db.StringProperty()
  lat  = db.StringProperty()
  lng  = db.StringProperty()
