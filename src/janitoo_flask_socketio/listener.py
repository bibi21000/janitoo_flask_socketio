# -*- coding: utf-8 -*-

"""The listener.

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

import logging
logger = logging.getLogger(__name__)

import os

from flask import Flask, render_template, session, request

from janitoo_flask_socketio.network import NetworkSocketio
from janitoo_flask.listener import ListenerThread

##############################################################
#Check that we are in sync with the official command classes
#Must be implemented for non-regression
from janitoo.classes import COMMAND_DESC

COMMAND_DHCPD = 0x1000
COMMAND_CONTROLLER = 0x1050
COMMAND_DISCOVERY = 0x5000

assert(COMMAND_DESC[COMMAND_DISCOVERY] == 'COMMAND_DISCOVERY')
assert(COMMAND_DESC[COMMAND_CONTROLLER] == 'COMMAND_CONTROLLER')
assert(COMMAND_DESC[COMMAND_DHCPD] == 'COMMAND_DHCPD')
##############################################################

listener = None

class ListenerSocketio(ListenerThread):
    """ The listener Tread
    """

    def __init__(self, _socketio, _app, options):
        """The constructor"""
        self.socketio = _socketio
        ListenerThread.__init__(self, _app, options)
        self.extend_from_entry_points('janitoo_flask_socketio')

    def create_network(self):
        """Create the listener on first call
        """
        self.network = NetworkSocketio(
            self.socketio,
            self.app,
            self._stopevent,
            self.options,
            is_primary=False,
            is_secondary=True,
            do_heartbeat_dispatch=False
        )
