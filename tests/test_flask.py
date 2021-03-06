# -*- coding: utf-8 -*-

"""Unittests for flask.
"""
__license__ = """
    This file is part of Janitoo.

    Janitoo is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Janitoo is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Janitoo. If not, see <http://www.gnu.org/licenses/>.

"""
__author__ = 'Sébastien GALLET aka bibi21000'
__email__ = 'bibi21000@gmail.com'
__copyright__ = "Copyright © 2013-2014-2015-2016 Sébastien GALLET aka bibi21000"

#~ from gevent import monkey
#~ monkey.patch_all()

import sys, os
import time, datetime
import unittest

from alembic import command as alcommand
from sqlalchemy import create_engine
from alembic import command as alcommand
from flask import Flask, request
from flask_bower import Bower
from flask_cache import Cache

from janitoo_nosetests_flask.flask import JNTTFlask, JNTTFlaskCommon

from janitoo.utils import json_dumps, json_loads
from janitoo.utils import HADD_SEP, HADD
from janitoo.utils import TOPIC_HEARTBEAT
from janitoo.utils import TOPIC_NODES, TOPIC_NODES_REPLY, TOPIC_NODES_REQUEST
from janitoo.utils import TOPIC_BROADCAST_REPLY, TOPIC_BROADCAST_REQUEST
from janitoo.utils import TOPIC_VALUES_USER, TOPIC_VALUES_CONFIG, TOPIC_VALUES_SYSTEM, TOPIC_VALUES_BASIC

from janitoo.options import JNTOptions
from janitoo_db.base import Base, create_db_engine
from janitoo_db.migrate import Config as alConfig, collect_configs, janitoo_config

from janitoo_flask_socketio import FlaskJanitooSocketio
from flask_socketio import SocketIO

class TestFlask(JNTTFlask):
    """Test flask
    """
    flask_conf = None

    def create_app(self):
        # SocketIO
        socketio = SocketIO()
        app = Flask("janitoo_flask_socketio")
        janitoo = FlaskJanitooSocketio(app, socketio)
        janitoo.init_app(app, socketio, {})
        return app

    def test_001_app_is_loaded(self):
        self.assertEqual(type(self.app.extensions['cache']), type(Cache()))
        self.assertEqual(type(self.app.extensions['bower']), type(Bower()))
        print(self.get_routes())
        self.assertEndpoint('bower.serve')
        self.assertEndpoint('static')
