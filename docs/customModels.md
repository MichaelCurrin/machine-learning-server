# CUstom Models

## Colour Classification

The project includes an existing trained model for color classification and this exists in the [Built-in Color Classifier](/mlserver/models/builtinColorClassifier).

If you have your own trained model you would like to use, you can add it to the project as an unversioned file and then switch between the built-in and drop-in models by choosing the appropriate classifier form at [http://localhost:9000]().


### Steps

1. Copy your file to the custom [Drop-in Color Classifier](/mlserver/models/dropinColorClassifier) directory. If the file ends with `.local.pb`, it will not be tracked by git. Note that if running this inside a docker container, the target file to copy must already be on the docker container's file system for it to be accessible.

    Example:

       ```bash
       $ cp path/to/myColorClassifier.pb mlserver/models/dropinColorClassifier/modelGraph.local.pb
       ```

2. Update the drop-in model's [configuration file](/mlserver/models/dropColorClassifer/model.conf) if neccasary. The file is setup by default to point to a file named `modelGraph.local.pb` as above.

3. Start the server as per the [Usage Instructions](usage.md) and go to [http://localhost:9000/classify/dropinColors.html]() in the browser to test it.
