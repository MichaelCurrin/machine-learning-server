# -*- coding: utf-8 -*-
"""Color Classifier plugin file.

Usage for testing:
    python -m lib.plugins.colorClassifier --help
"""
import os
import sys

from base import ImagePluginBase, testImagePrediction


class ColorClassifier(ImagePluginBase):
    """Color Classifier plugin class."""

    def __init__(self):
        """Initialise by setting up metadata, paths and loading the model.
        """
        name = 'Color Classifier'
        description = 'Image predictor plugin for suggesting colors for'\
            ' an image at an (x,y) co-ordinate point.'
        modelName = 'colorClassifier'
        # Override default value so we use an image array on the prediction.
        getArray = True

        # Send values to initialisation method of parent class and setup
        # the model conf object.
        super(ColorClassifier, self).__init__(
            name,
            description,
            modelName,
            getArray=getArray
        )
        # Set Tensorflow verbosity level.
        os.environ['TF_CPP_MIN_LOG_LEVEL'] = self.getConf().get('logging',
                                                                'TFLogLevel')
        # Get full paths to input files then load them.
        labelsPath = self.getConf().getLabelsPath()
        modelsPath = self.getConf().getModelPath()
        self.labels = self._loadGuidAndDescriptionLabels(labelsPath)
        self.graph = self._loadGraph(modelsPath)


def main(args):
    """Do test with the ColorClassifier plugin, as either basic test or a
    prediction, depending on the arguments.
    """
    testImagePrediction(args, pluginClass=ColorClassifier)


if __name__ == '__main__':
    main(sys.argv[1:])
