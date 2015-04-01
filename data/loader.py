# coding: utf-8
from __future__ import absolute_import, unicode_literals, print_function
import json
import os
import sys

import requests


if __name__ == "__main__":
    stations = json.loads(
        open(os.path.join(os.path.dirname(__file__), "./station.json")).read())
    stores = json.loads(
        open(os.path.join(os.path.dirname(__file__), "./store.json")).read())

    headers = {
        "Content-Type": "application/json; charset=utf-8",
    }
    data = json.dumps({"stations": stations, "stores": stores},
                      ensure_ascii=False)
    r = requests.post(
        '{}/store'.format(sys.argv[1]),
        json={"stations": stations, "stores": stores},
        headers=headers)
    print(r)
