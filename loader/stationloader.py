#/usr/bin/env python
# -*- coding: utf-8 -*-

from google.appengine.ext import db
from google.appengine.tools import bulkloader
import sys, os
sys.path.append(os.pardir)
from models.station import Stations

class StationLoader(bulkloader.Loader):
  def __init__(self):
    bulkloader.Loader.__init__(self, 'Stations',
    [('name', lambda x: x.decode('utf-8')),
    ('lat', lambda x: x.decode('utf-8')),
    ('lng', lambda x: x.decode('utf-8')),
    ])

loaders = [StationLoader]