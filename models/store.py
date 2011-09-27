#!/usr/bin/env python
# -*- coding: utf-8 -*-

from google.appengine.ext import db

class Stores(db.Model):
	station = db.StringProperty()
	genre   = db.StringProperty()
	name    = db.StringProperty()
	lat     = db.StringProperty()
	lng     = db.StringProperty()
