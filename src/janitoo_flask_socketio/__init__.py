# -*- coding: utf-8 -*-

"""janitoo flask extension.

"""

___license__ = """
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

    Original copyright :
    Copyright (c) 2013 Roger Light <roger@atchoo.org>

    All rights reserved. This program and the accompanying materials
    are made available under the terms of the Eclipse Distribution License v1.0
    which accompanies this distribution.

    The Eclipse Distribution License is available at
    http://www.eclipse.org/org/documents/edl-v10.php.

    Contributors:
     - Roger Light - initial implementation

    This example shows how you can use the MQTT client in a class.

"""
__author__ = 'Sébastien GALLET aka bibi21000'
__email__ = 'bibi21000@gmail.com'
__copyright__ = "Copyright © 2013-2014-2015-2016 Sébastien GALLET aka bibi21000"

#~ from gevent import monkey
#~ monkey.patch_all()

import logging
logger = logging.getLogger(__name__)

from logging.config import fileConfig as logging_fileConfig
from flask import appcontext_pushed
from flask import current_app
from jinja2 import Markup
import signal, sys
import os, tempfile, errno
import threading

from pkg_resources import iter_entry_points

from janitoo_flask_socketio.listener import ListenerSocketio
from janitoo_flask import FlaskJanitoo

#~ print "================================================================================================= I'ts import !!!"

"""
A Flask extension to build a webapp for janitoo
"""

# Find the stack on which we want to store the database connection.
# Starting with Flask 0.9, the _app_ctx_stack is the correct one,
# before that we need to use the _request_ctx_stack.
try:
    from flask import _app_ctx_stack as stack
except ImportError:
    from flask import _request_ctx_stack as stack

class FlaskJanitooSocketio(FlaskJanitoo):

    def __init__(self, app=None, socketio=None, options=None, db=None):
        FlaskJanitoo.__init__(self, app=app, options=options, db=db)
        self._socketio = socketio
        if app is not None and socketio is not None and options is not None:
            self.init_app(app, socketio, options, db)

    def init_app(self, app, socketio, options, db=None):
        """
        """
        if socketio is not None:
            self._socketio = socketio
        FlaskJanitoo.init_app(self, app=app, options=options, db=db)

    def create_listener(self):
        """Create the listener on first call
        """
        self._listener = ListenerSocketio(self._socketio, self._app, self.options)
