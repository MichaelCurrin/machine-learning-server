# -*- coding: utf-8 -*-
"""
Classify application file.
"""
import time

import cherrypy

from lib import logger
from lib.plugins.colorClassifier import ColorClassifier
from lib.plugins.digitClassifier import DigitClassifier
from lib.config import AppConf


conf = AppConf()

# If there is no model graph file setup for the dropin color classifier,
# fail silently since it is optional when starting the server.
try:
    dropinColors = ColorClassifier(modelName='dropinColorClassifier')
except AssertionError:
    dropinColors = None

# Instantiate all the available classifier plugins at once when building the
# server app tree.
PLUGINS = {
    'builtinColors': ColorClassifier(modelName='builtinColorClassifier'),
    'dropinColors': dropinColors,
    'builtinDigits': DigitClassifier(modelName='builtinDigitClassifier')
}
CONFIGURED_PLUGINS = [k for k, v in PLUGINS.items() if v is not None]


@cherrypy.popargs('pluginName')
class Classify(object):
    """Handler for the /services/classify endpoint.

    Accepts a dynamic plugin name as /services/classify/{PLUGIN_NAME}
    and then does a prediction with the plugin if it is valid.
    """

    exposed = True

    def GET(self, pluginName=None, *args, **kwargs):
        """Return available plugin names or raise an error on a given name.

        @param pluginName: Optional str for name of plugin. If provided,
            raise an error, otherwise return available plugin names.

        @return: dict with list of available plugin names as the value.
        """
        if pluginName is None:
            return {
                'configured_plugin_names': CONFIGURED_PLUGINS
            }
        raise cherrypy.HTTPError(501, "Not implemented yet.")

    def POST(self, pluginName=None, *args, **kwargs):
        """Classify an image using given plugin name and return predictions.

        @param pluginName: Optional name of plugin to lookup. Raise an error
            if not supplied or not a valid name.

        @return predictions: list of strings for predicted labels, ordered as
            most likely first.
        """
        if pluginName is None:
            raise cherrypy.HTTPError(
                405,
                "POST method requires a plugin name."
            )

        try:
            plugin = PLUGINS[pluginName]
        except KeyError:
            raise cherrypy.HTTPError(
                400,
                "Expected plugin name as one of {names}, but got: '{actual}'."
                .format(
                    names=CONFIGURED_PLUGINS,
                    actual=pluginName
                )
            )

        if plugin is None:
            raise cherrypy.HTTPError(
                500,
                "That plugin has not been setup on the server. Ensure it has"
                " a valid graph file and that this is indicated in the"
                " model conf file."
            )

        startTime = time.time()
        predictions = plugin.process(**kwargs)
        maxResults = conf.getint('predictions', 'maxResults')
        predictions = predictions[:maxResults]

        duration = time.time() - startTime
        msg = "Completed request. Name: {name}. Duration: {duration:4.3f}s."\
            .format(
                name=pluginName,
                duration=duration
            )
        logger(msg, context="SERVICES.CLASSIFY.PREDICTION")

        cherrypy.response.status = 201

        return predictions
