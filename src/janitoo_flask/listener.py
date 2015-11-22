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
__copyright__ = "Copyright © 2013-2014-2015 Sébastien GALLET aka bibi21000"

from gevent import monkey
monkey.patch_all()

import logging
logger = logging.getLogger('janitoo.flask')

import os, sys
import time
import threading
from pkg_resources import iter_entry_points

from flask import Flask, render_template, session, request, current_app

from janitoo.mqtt import MQTTClient
from janitoo.options import JNTOptions
from janitoo.server import JNTControllerManager
from janitoo.utils import HADD, HADD_SEP, CADD, json_dumps, json_loads
from janitoo.dhcp import HeartbeatMessage, check_heartbeats, CacheManager
from janitoo_flask.network import NetworkFlask

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

class ListenerThread(threading.Thread, JNTControllerManager):
    """ The listener Tread
    """

    def __init__(self, _socketio, _app, options):
        """The constructor"""
        threading.Thread.__init__(self)
        self._stopevent = threading.Event( )
        self.socketio = _socketio
        self.app = _app
        self.section="webapp"
        self.mqttc = None
        self.options = JNTOptions(options)
        JNTControllerManager.__init__(self)
        self.hadds = {}
        self.network = NetworkFlask(self.socketio, self.app, self._stopevent, self.options, is_primary=False, is_secondary=True, do_heartbeat_dispatch=False)
        self.loop_sleep = 0.25
        loop_sleep = self.options.get_option('system','loop_sleep', self.loop_sleep)
        if loop_sleep is not None:
            self.loop_sleep = loop_sleep
        else:
            logger.debug("[%s] - Can't retrieve value of loop_sleep. Use default value instead (%s)", self.__class__.__name__, self.loop_sleep)
        self.extend_from_entry_points('janitoo_flask')

    def boot(self):
        """configure the HADD address
        """
        default_hadd = HADD%(9998,0)
        hadd = self.options.get_option('webapp','hadd', default_hadd)
        if default_hadd is None:
            logger.debug("[%s] - Can't retrieve value of hadd. Use default value instead (%s)", self.__class__.__name__, default_hadd)
        self.hadds = { 0 : hadd,
                     }

    def run(self):
        """The running method
        """
        logger.info("Start listener")
        self.boot()
        self.network.boot(self.hadds)
        JNTControllerManager.start_controller(self, self.section, self.options, cmd_classes=[COMMAND_DHCPD], hadd=self.hadds[0], name="Webapp Server",
            product_name="Webapp Server", product_type="Webapp Server")
        self._stopevent.wait(1.0)
        JNTControllerManager.start_controller_timer(self)
        while not self._stopevent.isSet():
            self._stopevent.wait(self.loop_sleep)
        self.network.stop()

    def stop(self):
        """Stop the tread
        """
        JNTControllerManager.stop_controller_timer(self)
        self._stopevent.set( )
        logger.info("Stop listener")
        JNTControllerManager.stop_controller(self)

    def extend_from_entry_points(self, group):
        """"Extend the listener with methods found in entrypoints
        """
        for entrypoint in iter_entry_points(group = '%s.listener'%group):
            logger.info('Extend listener with %s', entrypoint.module_name )
            extend = entrypoint.load()
            extend( self )

def start_listener(app_, socketio_, options):
    """Start the listener
    """
    global listener
    if listener is None:
        listener = ListenerThread(socketio_, app_, options)
        listener.start()
    return listener

def stop_listener():
    """Stop the listener
    """
    global listener
    if listener is not None:
        listener.stop()
        listener = None