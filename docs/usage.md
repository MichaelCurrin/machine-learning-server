# Usage instructions

1. View the application's log files.

    ```bash
    $ cd path/to/machine-learning-server/mlserver
    $ cd var/log/app
    $ tail -F *.log
    ```

2. Start the server.

    * Either run as a main process (requires `daemon: False` in `app.local.conf`)
        ```bash
        $ cd path/to/machine-learning-server
        $ source ../virtualenv/bin/activate
        $ cd mlserver
        $ ./app.py
        ```
    * Or, run as a background process (requires `daemon: True` in `app.local.conf`) _TODO: This must be still be implemented on app.py and systemd._

        ```bash
        $ sudo systemctl start mlserver.service
        $ sudo systemctl stop mlserver.service
        ```

3. Test the application while it is running.

    * Test the prediction service in the browser at http://localhost:9000/form
    * Run tests covering the API endpoints. _TODO: Still to be implemented_

        ```bash
        $ cd mlserver/tests
        $ ./basic.sh
        $ ./prediction.sh
        ```
