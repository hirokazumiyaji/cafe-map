#/usr/bin/env python
# -*- coding: utf-8 -*-

from google.appengine.ext import db
from google.appengine.tools import bulkloader
import sys, os
sys.path.append(os.pardir)
from models.store import Stores

class StoreLoader(bulkloader.Loader):
  def __init__(self, arg):
    bulkloader.Loader.__init__(self, 'Stores',
    [('station', lambda x: x.decode('utf-8')),
    ('genre', lambda x: x.decode('utf-8')),
    ('name', lambda x: x.decode('utf-8')),
    ('lat', lambda x: x.decode('utf-8')),
    ('lng', lambda x: x.decode('utf-8')),
    ])

loaders = [StoreLoader]