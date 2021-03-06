#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
janitoo-flask
--------------

"""
from os import name as os_name
from setuptools import setup, find_packages
from platform import system as platform_system
import glob
import os
import sys
from _version import janitoo_version

def data_files_config(res, rsrc, src, pattern):
    for root, dirs, fils in os.walk(src):
        if src == root:
            sub = []
            for fil in fils:
                sub.append(os.path.join(root,fil))
            res.append((rsrc, sub))
            for dire in dirs:
                    data_files_config(res, os.path.join(rsrc, dire), os.path.join(root, dire), pattern)

data_files = []
data_files_config(data_files, 'docs','src/docs/','*')

setup(
    name='janitoo_flask_socketio',
    version=janitoo_version,
    url='http://github.com/bibi21000/janitoo_flask/',
    author='Sébastien GALLET aka bibi2100 <bibi21000@gmail.com>',
    author_email='bibi21000@gmail.com',
    license = """
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
    """,
    description="The flask extension with socketio support to build web apps for janitoo",
    long_description=__doc__,
    packages = find_packages('src', exclude=["scripts", "docs", "config"]),
    zip_safe=False,
    keywords = "flask,web",
    include_package_data=True,
    package_dir = { '': 'src' },
    platforms='any',
    install_requires=[
        'janitoo_db',
        'janitoo_flask',
        'Flask-SocketIO',
    ],
    dependency_links = [
      'https://github.com/bibi21000/janitoo_db/archive/master.zip#egg=janitoo_db',
      'https://github.com/bibi21000/janitoo_flask/archive/master.zip#egg=janitoo_flask',
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
)
