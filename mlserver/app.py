#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Machine Learning Server application file.
"""
import os

import cherrypy

from lib import APP_DIR, updateHTTPConfig
from services import Services
from lib.config import AppConf


appConf = AppConf()


class Root(object):
    """Handler for the / endpoint.

    Does nothing alone but returns a not implemented yet error. Other
    endpoints are mounted to this one in a tree structure.
    """

    @cherrypy.expose
    def index(self):
        """
        Dispatcher for the index path, which raises a not implemented error.
        """
        raise cherrypy.HTTPError(501, "Not implemented yet.")


def setup():
    """Setup the main application and the web server tree.

    Steps:
        1. Set global Engine configuration.
        2. Mount the applications on the tree.
        3. Set additional configuration for services app.

    Note that HTTP configuration is set when importing from lib.
    """
    confDir = os.path.join(APP_DIR, 'etc')

    engineConfPath = os.path.join(confDir, 'engine.conf')

    rootApp = cherrypy.tree.mount(Root(), '/', config=engineConfPath)
    servicesApp = cherrypy.tree.mount(Services(), '/services')

    for s in ['services.conf', 'services.local.conf']:
        sPath = os.path.join(confDir, s)
        if os.access(sPath, os.R_OK):
            servicesApp.merge(sPath)


def run():
    """Start the Machine Learning Server."""
    setup()
    cherrypy.engine.start()
    cherrypy.engine.block()


if __name__ == '__main__':
    run()
