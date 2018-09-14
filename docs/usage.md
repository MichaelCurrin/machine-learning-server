# Usage instructions

1. Start the server in a terminal window.

    ```bash
    $ cd path/to/machine-learning-server/mlserver
    $ source ../venv/bin/activate
    $ ./app.py
    ```

2. View the application's log files.

    ```bash
    $ cd path/to/machine-learning-server/mlserver
    $ cd var/log/app
    $ tail -F *.log
    ```

3. Test the application is running at [http://localhost:9000](http://localhost:9000).

4. Use the project's sample images to do predictions.

    - See [digits](/sampleImages/digits/) directory.
    - See [photos](/sampleImages/photos/) directory.
    - Or use the [download URL](https://github.com/MichaelCurrin/machine-learning-server/raw/master/mlserver/sampleImages/digits_and_photos.zip) for the [digits_and_photos.zip](/sampleImages/digits_and_photos.zip) file.
