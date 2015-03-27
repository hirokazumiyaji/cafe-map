#/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

from google.appengine.ext import db
from google.appengine.tools import bulkloader
from models.store import Stores

sys.path.append(os.pardir)


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
