# -*- coding: utf-8 -*-
"""Configuration application file.

Usage for testing:
    $ python -m lib.config
"""
import os
from ConfigParser import SafeConfigParser

from . import APP_DIR


class AppConf(SafeConfigParser):
    """Container of app config data for the server application.

    Note that we determine the path to the config file relative from where this
    file lives. We expect a dir structure like this:

        app/
          |- lib/
          |    |- config.py
          |- etc/
          |    |- app.conf
          |    |- (app.local.conf)  # Optional local conf file
          ...  |- ...
    """

    CONF_NAMES = ('app.conf', 'app.local.conf')

    def __init__(self):
        """
        Read and parse the global and local configs.
        """
        SafeConfigParser.__init__(self)

        appDir = APP_DIR
        confDir = os.path.join(appDir, 'etc')

        # Create absolute paths to files for config parsing to work properly
        # when running as daemon. Only the first file needs to exist.
        confPaths = [os.path.join(confDir, x) for x in
                     self.__class__.CONF_NAMES]
        assert os.access(confPaths[0], os.R_OK), (
            'Cannot read config file: `{0}`.'.format(confPaths[0])
            )
        self.read(confPaths)

        # Set the value of the config object on app start. Any references to
        # `%(appDir)s` in app conf strings will be interpolated with this
        # value.
        self.set('DEFAULT', 'appDir', appDir)


class ModelConf(SafeConfigParser):
    """A class for creating Safe Config Parser instances configured for a
    specific model file.

    Note that we determine the path to the config file relative from where this
    file lives. We expect a dir structure like this:

        app/
          |- lib/
          |    |- config.py
          |- models/
          |    |- modelNameA
          |    |     | - model.conf
          |    |     | - (model.local.conf)  # Optional local conf file
          |    |- modelNameB
          |    |     ...
          |    ...
          ...
    """

    CONF_NAMES = ('model.conf', 'model.local.conf')

    def __init__(self, name):
        """
        Read and parse the global and local configs.

        @param name: The name of the model directory. e.g. 'themeClassifier'.
        """
        SafeConfigParser.__init__(self)

        # Make keys within a section case-sensitive, so that keys are not
        # forced to lowercase when added to a section. This is the solution
        # recommended in ConfigParser documentation, without need to subclass.
        self.optionxform = str

        # The model directory for this specific model.
        self.modelDir = os.path.join(APP_DIR, 'models', name)
        assert os.path.exists(self.modelDir), (
            'Cannot find directory: `{name}`. Full path: {path}'
            .format(
                name=name,
                path=self.modelDir
            )
        )
        # Create full paths to model conf files, for config parsing to work
        # properly. Only the first file needs to exist.
        confPaths = [os.path.join(self.modelDir, x) for x in
                     self.__class__.CONF_NAMES]
        assert os.access(confPaths[0], os.R_OK), (
            "Cannot read config file: `{0}`. Full path: {1}"
            .format(self.__class__.CONF_NAMES[0], confPaths[0])
        )
        self.read(confPaths)

    def getModelPath(self):
        """Get the path to the configured model file.

        @return: absolute path to model file if one is set, otherwise None.
        """
        modelFileName = self.get('inputFiles', 'modelFileName')

        if modelFileName:
            modelPath = os.path.join(self.modelDir, modelFileName)
            assert os.access(modelPath, os.R_OK), (
                "Unable to read path to model file: `{0}`.".format(modelPath)
            )
            return modelPath
        else:
            return None

    def getLabelsPath(self):
        """Get the path to the configured labels file.

        @return: absolute path to labels file if one is set, otherwise None.
        """
        labelsFileName = self.get('inputFiles', 'labelsFileName')

        if labelsFileName:
            labelsPath = os.path.join(self.modelDir, labelsFileName)
            assert os.access(labelsPath, os.R_OK), (
                "Unable to read path to labels file: `{0}`.".format(labelsPath)
            )
            return labelsPath
        else:
            return None

    def asDict(self):
        """Return data in the config object as dict object.

        Take all the stored sections, options and their values and convert to a
        nested dictionary and return it. Note that all values are kept as
        string format.

        @return: nested dictionary of all data in config object.
        """
        return {
            section: {k: v for k, v in self.items(section)}
            for section in self.sections()
        }


def test(modelName='colorClassifier'):
    """Check that this config file and its classes are performing as expected.

    Creates an instance of AppConf and prints the contents of the object.
    Creates an instance of ModelConf using a specific model name and prints
    the contents of the object.

    @param modelName: the name of the model, take from one of the dirs in
        app/models/{modelName}. Defaults tot themeClassifier if not set.
    """
    print("App Configuration test")
    print("========================")
    appConf = AppConf()

    for x in appConf.sections():
        print("[{0}]").format(x)
        for k, v in appConf.items(x):
            print("    {0:.<25} {1}").format(k, v)
        print()
    print()

    print("Model Configuration test")
    print("========================")
    modelConf = ModelConf(modelName)

    for x in modelConf.sections():
        print("[{0}]").format(x)
        for k, v in modelConf.items(x):
            print("    {0:.<25} {1}".format(k, v))
        print()

    print("CherryPy Configuration test")
    print("===========================")
    import cherrypy
    for k, v in cherrypy.config.items():
        print("    {0:.<25} {1}".format(k, v))


if __name__ == '__main__':
    test()
