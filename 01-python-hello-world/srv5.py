# -*- Mode: Python; python-indent-offset: 4 -*-
#
# Time-stamp: <2018-05-26 15:33:59 alex>
#
# --------------------------------------------------------------------
# lab-prometheus - basic python instrumentation for prometheus
# 
# Copyright (C) 2016-2017  Alexandre Chauvin Hameau <ach@meta-x.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# --------------------------------------------------------------------

"""
lab-prometheus - basic python instrumentation for prometheus
add call number & time on function

virtualenv lab01
source lab01/bin/activate
pip install -r requirements.txt
python ./srv5.py

get some ws on /now counting the even and odd epoch values
get the ws with a client on /metrics and check ws_srv_is_now_even counter
"""

import datetime

from flask import Flask, make_response, jsonify, Response

from prometheus_client import (generate_latest,
                               CONTENT_TYPE_LATEST,
                               Counter,
                               Summary)

app = Flask(__name__)

COUNTER_NOW_EVEN = Counter('ws_srv_is_now_even',
                           'count even now aligned on second',
                           ['even'])

COUNT_FCT_NOW = Summary('ws_srv_func_now', 'stats of function now')


@app.route('/now')
@COUNT_FCT_NOW.time()
def ws_now():
    """Now service to get date time on the server."""
    now = datetime.datetime.now()

    # business counter
    if int(now.timestamp()) % 2 == 0:
        COUNTER_NOW_EVEN.labels(even='yes').inc()
    else:
        COUNTER_NOW_EVEN.labels(even='no').inc()

    return make_response(jsonify({
        'epoch': now.timestamp(),
        'ctime': now.ctime(),
        'date': str(now)
    }), 200)


@app.route('/metrics')
def metrics():
    """Flask endpoint to gather the metrics, will be called by Prometheus."""
    return Response(generate_latest(),
                    mimetype=CONTENT_TYPE_LATEST)


if __name__ == '__main__':
    app.secret_key = "lab-01-prometheus/05"
    app.debug = True

    app.run(host='0.0.0.0')
