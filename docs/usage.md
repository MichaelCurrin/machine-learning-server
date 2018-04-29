# Usage instructions

1. View the application's log files (there will be none initially).

    ```bash
    $ cd path/to/machine-learning-server/mlserver
    $ cd var/log/app
    $ tail -F *.log
    ```

2. Start the server in another terminal window.

    ```bash
    $ cd path/to/machine-learning-server/mlserver
    $ source ../venv/bin/activate
    $ ./app.py
    ```

3. Test the application in the browser at [http://localhost:9000]().
