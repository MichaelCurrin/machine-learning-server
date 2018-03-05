# -*- coding: utf-8 -*-
"""Custom validators.

See `formencode.validators` documentation for validating and converting to or
from python.
"""
from formencode import Schema, validators


class ImageMarkValidator(Schema):
    """
    Validation for input of image and points co-ordinates for prediction.

    The co-ordinates can be numeric or string data
    types.
    """

    # Path to image on the server. Defaults to null string, but then
    # we raise an error elsewhere if the the imageFile object is also null.
    imagePath = validators.String()

    # TODO: Set range from 0 to 100.
    x = validators.Int()
    y = validators.Int()
