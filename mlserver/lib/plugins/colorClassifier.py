# -*- coding: utf-8 -*-
"""Color Classifier plugin file.

Usage for testing:
    python -m lib.plugins.colorClassifier --help
"""
import os
import sys

from .base import ImagePluginBase, testImagePrediction


class ColorClassifier(ImagePluginBase):
    """Color Classifier plugin class.

    This can be used for the standard or the drop-in color classifier services.
    """

    def __init__(self, modelName):
        """Initialise by setting up metadata, paths and loading the model.

        @param modelName: The name of the directory within the models,
            directory. The model graph file is read relative to this.
        """
        # Send values to initialisation method of parent class and setup
        # the model conf object.
        super().__init__(
            modelName,
            getArray=True
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
    testImagePrediction(
        args,
        pluginClass=ColorClassifier,
        modelName='colorClassifier'
    )


if __name__ == '__main__':
    main(sys.argv[1:])
