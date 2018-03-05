# -*- coding: utf-8 -*-
"""Classify application file."""
import time

import cherrypy

from lib import logger
from lib.plugins.colorClassifier import ColorClassifier
from lib.validators import ImageMarkValidator

# Instantiate all the available classifier plugins at once when building the
# server app tree.
PLUGINS = {'colors': ColorClassifier()}


@cherrypy.popargs('pluginName')
class Classify(object):
    """Handler for the /services/classify endpoint.

    Accepts a dynamic plugin name as /services/classify/{PLUGIN_NAME}
    and then does a prediction with the plugin if it is valid.
    """

    exposed = True

    def GET(self, *args, **kwargs):
        """Return a not implemented yet error."""
        raise cherrypy.HTTPError(501, 'Not implemented yet.')

    def POST(self, pluginName=None, *args, **kwargs):
        """Classify an image using given plugin name and return predictions."""
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
                    names=PLUGINS.keys(),
                    actual=pluginName
                )
            )

        # Remove the imageFile until this can be handled in the validator.
        # Add it back to the cleaned data.
        imageFile = kwargs.pop('imageFile', None)
        # TODO: Add probability output and a limit of items above a number
        # or above a probability threshold.
        data = ImageMarkValidator.to_python(kwargs)
        if imageFile:
            data['imageFile'] = imageFile.file

        startTime = time.time()
        predictions = plugin.process(**data)
        duration = time.time() - startTime
        msg = "Completed request. Name: {name}. Duration: {duration:4.3f}s."\
            .format(
                name=pluginName,
                duration=duration
            )
        logger(msg, context="SERVICES.CLASSIFY.PREDICTION")

        cherrypy.response.status = 201

        return predictions
