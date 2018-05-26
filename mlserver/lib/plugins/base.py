# -*- coding: utf-8 -*-
"""Base plugin file."""
import json
import os
import time
from io import BytesIO

import numpy as np
import tensorflow as tf

from lib import logger
from lib.config import AppConf, ModelConf
from lib.imageTransformer import ImageTransformer


conf = AppConf()


class PluginBase(object):
    """Abstract class as a base for plugins."""

    def __init__(self, modelName):
        """Instantiate a configured instance of the plugin.

        @param modelName: the name of the plugin's model, as a string.
            This is used to setup a ModelConf instance, which holds
            the prediction parameters and model metadata.
        """
        self.conf = ModelConf(modelName)
        self.context = "LIB.PLUGINS.{pluginName}".format(
            pluginName=self.__class__.__name__.upper()
        )

    def getConf(self):
        """Retrieve the ModelConf instance of the plugin.

        @return: conf object as SafeConfigParser instance. with configured
            data for the plugin and model.
        """
        return self.conf

    def getDescription(self):
        """Retrieve the description of the plugin.

        @return: description of plugin, as a string.
        """
        return self.conf.get('model', 'description')

    def getName(self):
        """Retrieve the name of the plugin.

        @return: name of plugin, as a string.
        """
        return self.conf.get('model', 'name')

    def getContext(self):
        """Retrieve the context of the plugin to be used for logging.

        @return: logging context of the plugin, as a string.
        """
        return self.context

    def _loadGraph(self, modelPath):
        """Prepare the plugin's graph definition so we can use its tensors.

        The time taken for this method to compelte is sent to the error log.

        This is a private method which be called internally on model
        initialisation. It unpersists a TensorFlow graph from the proto-buf
        file, so that we can use it in a TensorFlow session to do predictions.

        According to the `tf.import_graph_def` docs, it expects a `GraphDef`
        proto containing operations to be imported in the default graph, so
        they be extracted as a `tf.Tensor` and `tf.Operation` objects.

        @param modelPath: path to the model graph file, as a string.

        @return graph: a tf.Graph instance which contains the graph definition
            for the required model.
        """
        startTime = time.time()

        # Create a new graph then set it as the default.
        graph = tf.Graph()
        with graph.as_default():
            with tf.gfile.FastGFile(modelPath, 'rb') as fIn:
                # Create an empty graph-def then load the proto-buf file into
                # the graph-def.
                graphDef = tf.GraphDef()
                graphDef.ParseFromString(fIn.read())

                # Import the graph-def to the default TensorFlow graph.
                # Name is a prefix for the tensor and should be left empty.
                tf.import_graph_def(graphDef, name='')

        duration = time.time() - startTime
        msg = "Loaded model. Duration: {0:4.3f}s.".format(duration)
        logger(msg, context=self.getContext())

        return graph

    def _loadLabels(self, labelsPath):
        """Load human-readable labels from model's text labels file.

        The order of the text file's rows is important, since indexes of
        the list items read in correspond to the node IDs returned
        when the plugin makes a prediction.

        @param labelPath: path to the labels text file. The labels file is
            expected as a CSV text file, without headers. The rows should be
            in the following format:
                label1
                label2
                ...

        @return labels: List of tuples representing rows in the input labels
            CSV file.
        """
        # Remove the newline characters from row end.
        return [row.rstrip() for row in tf.gfile.GFile(labelsPath)]

    def _doPrediction(self):
        """All plugins require a prediction method - but it must be implemented
        in the child class.

        This method should only be called in the instance internally, using
        the process method.
        """
        raise ValueError("Method not implemented yet.")

    def process(self):
        """All plugins require a process method - but it must be implemented in
        the child class.
        """
        raise ValueError("Method not implemented yet.")


class ImagePluginBase(PluginBase):
    """
    Abstract class as a base for plugins which make predictions based on
    image input.
    """

    def __init__(self, modelName, getArray=False, greyscale=False):
        """Initialise an instance of the ImagePluginBase class.

        @param modelName: the name of the plugin's model, as a string.
            This is used to setup a ModelConf instance, which holds
            the prediction parameters and model metadata.
        @param getArray: Default False. Boolean flag to set the image type
            required during process, so that we get an image format
            from image transformer which is appropriate for the
            prediction algorithm. If True, use an array (some suitable for
            some models which need pixel color or brightness data as an
            array), otherwise use a string of bytes.
        @param greyscale: Default False. If True, do preprocessing using
            a greyscale image, otherwise process as color (RGB). Note
            that the LA greyscale mode has an alpha channel which can be
            ignored, leaving a single channel of pixel brightness.
        """
        super().__init__(modelName)
        self.getArray = getArray
        self.greyscale = greyscale

    def _preProcessImg(self, imageInput, x=None, y=None):
        """Apply image transformation to pre-process the image for predictions.

        Crop the image if a cropping ratio has been configured AND if a (X, Y)
        co-ordinate point is given. Resizes the image if target resize pixels
        have been configured. We catch the error of converting empty strings
        to float or integers by replacing with None values.

        The (X,Y) point is optional to allow child plugins to do a prediction.
        on an uncropped image. But if a mark point to crop around is a
        requirement for a plugin, then that should be enforced by validation
        at the controller level.

        @param imageInput: the image as a path string, or as string array of
            bytes (io.BytesIO instance).
        @param x: Optional X co-ordinate of a point to crop around. Defaults
            to None so that cropping can be skipped.
        @param y:  Optional Y co-ordinate of a point to crop around. Defaults
            to None so that cropping can be skipped.
        @param getArray: Default False. If True, return outputImage as
            numpy array instead of bytes string.

        @return outputImage: image with pre-processing steps applied, converted
            to string of bytes by default. Return as a numpy array if
            `getArray` is True. In both cases, the image object used
            in the transformations is closed before returning.
        """
        try:
            cropFactorW = self.conf.getfloat('image', 'cropFactorW')
            cropFactorH = self.conf.getfloat('image', 'cropFactorH')
        except ValueError:
            cropFactorW = cropFactorH = None
        try:
            resizeW = self.conf.getint('image', 'resizeW')
            resizeH = self.conf.getint('image', 'resizeH')
        except ValueError:
            resizeW = resizeH = None

        t = ImageTransformer()
        t.setImage(imageInput, 'LA' if self.greyscale else 'RGB')

        # Crop image if target ratio is configured and co-ordinate point is
        # set. The point is allowed to be at (0, 0).
        if cropFactorW and cropFactorH and x is not None \
                and y is not None:
            t.specialCrop(
                x,
                y,
                cropFactorW,
                cropFactorH,
                minWidth=resizeW,
                minHeight=resizeH
            )

        # Resize image to target dimensions, if configured.
        if resizeW and resizeH:
            t.specialResize(resizeW, resizeH)

        image = t.getImage()

        if self.getArray:
            # Get image pixel data then convert to array.
            arr = np.array(image.getdata())

            if self.greyscale:
                # Ignore alpha layer and keep luminosity.
                arr = arr[:,0]
                channels = 1
            else:
                channels = 3

            arr = np.asarray(arr, dtype='int32')

            # Flatten the array.
            outputImage = arr.reshape(1, image.width*image.height*channels)
        else:
            with BytesIO() as imgBytesArr:
                # Write image out to a bytes array file object in memory.
                image.save(imgBytesArr, format='jpeg')
                # Convert file object to a string of bytes.
                outputImage = imgBytesArr.getvalue()

        image.close()

        return outputImage

    def _doPrediction(self, imageData):
        """Use image input for trained model and return list of predicted
        node IDs which map to categories.

        If a prediction needs to be done without a model, this method
        should be overwritten in the child class.

        We create a session on each prediction and close it after the with
        block. This is recommended in the TensforFlow Session docs. Also, we
        need to use this logic when running dsAPI.service as a daemon,
        otherwise the prediction causes the app to freeze.

        @param imageData: image to be used for prediction, as string of
            bytes or as numpy array..

        @return predictions: list of prediction items in descending order,
            with each dict item having a 'label' and 'score' value. Exclude
            scores at or below the threshold of 5%.
        """
        inputTensor = self.getConf().get('tensors', 'input')
        outputTensor = self.getConf().get('tensors', 'output')

        params = {inputTensor: imageData}

        with tf.Session(graph=self.graph) as session:
            softmaxTensor = session.graph.get_tensor_by_name(outputTensor)
            predictions = session.run(softmaxTensor, params)

        # Get node IDs and sort from highest to lowest probability.
        sortedResults = reversed(predictions[0].argsort())

        return [
            {
                'label': self.labels[nodeID],
                'score': "{:3.2%}".format(predictions[0][nodeID])
            } for nodeID in sortedResults if predictions[0][nodeID] > 0.05
        ]

    def process(self, imagePath=None, imageFile=None, x=None, y=None):
        """Do category prediction on the configured plugin instance using
        input image and co-ordinate point.

        Expects an image and mark co-ordinates, then does a prediction
        for categories and returns as a list, ordered from highest to lowest
        probability.

        @param imagePath: Default None. path to local image on server, as
            a string.
        @param imageFile: Default None. Multi-party cherrpy request body.
            This is expected to have a file attribute with image data.
        @param x: Default None. The X co-ordinate of the mark on the image, as
            a percentage value from 0 to 100. As an integer.
        @param y: Default None. The Y co-ordinate of the mark on the image, as
            a percentage value from 0 to 100. As an integer.

        @return predictions: list of categories prediction values, as strings.
        """
        start = time.time()

        if imagePath:
            image = imagePath
            filename = os.path.basename(image)
        elif imageFile:
            image = imageFile.file
            filename = imageFile.filename
        else:
            raise ValueError("Expected value for either`imagePath` or"
                             " `imageFile` parameters.")

        preProcessedImg = self._preProcessImg(image, x, y)
        predictions = self._doPrediction(preProcessedImg)

        msg = "Completed prediction. Duration: {duration:4.3f}s."\
            " Filename: {filename}. Results: {results}.".format(
                duration=time.time() - start,
                filename=filename,
                results=json.dumps(predictions)
            )
        logger(msg=msg, context=self.getContext())

        return predictions


def testPlugin(pluginClass, modelName):
    """Test to create an instance of any child plugin and print its attributes.

    This is so that a plugin can be run independently of the other plugins
    where possible and without the API service running. This should succeed
    on any child plugin and cannot be run on the base plugin file (since
    they do not have attributes to initialise with).

    Usage: python -m lib.plugins.NAME_OF_PLUGIN
      e.g. python -m lib.plugins.colorClassifier

    Note that this command must be done as an IMPORT of the plugin name as a
    module with the app dir as the current directory, since an execution of
    the py file directly (even with app dir as working directory) will
    prevent local package imports from working.

    @param pluginClass: A child plugin object as a class (not as an instance).
    @param modelName: The name of a directory in the models directory.

    @return: None
    """
    import json

    print("Getting attributes of a `{0}` class instance.".format(
        pluginClass.__name__))

    plugin = pluginClass(modelName)

    print("Name: \n {0}\n".format(plugin.getName()))
    print("Description: \n  {0}\n".format(plugin.getDescription()))
    metadata = plugin.getConf().asDict()
    print("Metadata: \n  {0}\n".format(json.dumps(metadata, indent=4)))


def testImagePrediction(args, pluginClass, modelName):
    """Test to do prediction for an image plugin, using a file path and
    mark co-ordinates.

    This is to be used for internal testing when running the script directly.
    and can be called from image plugin files other than base.

    If help flag is supplied or there are not at least 3 arguments, a basic
    test is done to print out the plugin's attributes.

    @param args: List of command-line arguments.
    @param pluginClass: A child plugin object as a class (not as an instance).
    @param modelName: The name of a directory in the models directory.
    """
    import json
    import os

    if not args or set(args) & set(('-h', '--help')):
        print("Usage: python -m lib.plugins.nameOfPlugin [IMAGE_PATH]"
            " [X] [Y] [-p|--pretty] [-h|--help]\n")
        # Show plugin data without doing a prediction.
        testPlugin(pluginClass, modelName)
    else:
        # Expand possible '~' for user's home dir in image path.
        imgPath = args[0]
        imgPath = os.path.expanduser(imgPath)

        if len(args) == 3:
            x = int(args[1])
            y = int(args[2])
        else:
            x = 50
            y = 50
        # Do integer conversion here, but this is handled with validator at
        # the controller level.
        data = {
            'imagePath': imgPath,
            'x': x,
            'y': y,
        }

        plugin = pluginClass(modelName)
        predictions = plugin.process(**data)
        maxResults = conf.getint('predictions', 'maxResults')
        predictions = predictions[:maxResults]
        print(json.dumps(predictions, indent=4))
