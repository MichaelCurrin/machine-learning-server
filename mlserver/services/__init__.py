# -*- coding: utf-8 -*-
"""Services module."""
import cherrypy

from .classify import Classify


class Services(object):
    """Handler for the /services endpoint."""

    exposed = True

    def __init__(self):
       self.classify = Classify()

    def GET(self):
        raise cherrypy.HTTPError(404, 'Not found.')
