# -*- coding: utf-8 -*-
"""Custom validators.

See `formencode.validators` documentation for validating and converting to or
from python.
"""
from formencode import Schema, validators


class ImageMarkValidator(Schema):
    """Validation for input of image and points co-ordinates for prediction.

    The co-ordinates can be numeric or string data types.
    """

    # Path to image on the server.
    imagePath = validators.String(if_missing=None)

    x = validators.Int(min=0, max=100)
    y = validators.Int(min=0, max=100)
