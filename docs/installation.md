# Installation instructions

Setup the the repo and the application's environment.

1. Install system dependencies:
    
    ```bash
    $ sudo apt-get update
    $ sudo apt-get install python-virtualenv
    ```

2. Clone the git repository:
   
    ```bash
    $ git clone https://michaelcurrin@bitbucket.org/michaelcurrin/machine-learning-server.git
    $ cd machine-learning-server
    ```

3. Install Python dependencies:
    
    ```bash
    $ git checkout develop
    $ venv virtualenv -p python3.6
    $ source virtualenv/bin/activate
    (venv) $ pip install --upgrade pip
    (venv) $ pip install -r requirements.txt
    ```

4. Optionally configure any existing models, by creating an unversioned file to override defaults. e.g.

   ```bash
   $ nano ml_server/models/builtinColorClassifier/model.local.conf
   # Local configuration file for builtin color classifier.
   [image]
    cropFactorW: 0.05
    cropFactorH: 0.05
    resizeW: 15
    resizeH: 15
   ```

5. Optionally, copy a user-trained color classifier file to the drop color classifier directory. If it ends with '.local.pb', it will not be tracked by git. e.g.

   ```bash
   $ cp path/to/myColorClassifier.pb mlserver/models/dropinColorClassifier/modelGraph.local.pb
   ```

4. If running on a production environment, the versioned [app.conf](/mlserver/etc/app.conf) and [http.conf](/mlserver/etc/http.conf) files are fine. But if running on a local development environment, then create _local_ configuration files in the [etc](/mlserver/etc) directory as below and paste in the text.
    
    * `nano mlserver/etc/app.local.conf`
        ```
        ### Local App configuration ###

        ### Site wide service settings
        [service]
        runAsDaemon: False
        ```

    * `nano mlserver/etc/http.local.conf` *FIXME: When nginx is implemented, we can leave host as default and the socket_host line can be removed here.*

        ```
        ### Local HTTP configuration ###
        [global]

        ### Address
        server.socket_host: '0.0.0.0'


        ### Threads
        server.thread_pool = 10


        ### Environment
        checker.on: True
        engine.autoreload.on: True
        request.show_mismatched_params: True
        request.show_tracebacks: True
        tools.log_headers.on: True
        ```

5. If running on a VM, configure port forwarding rules:
    1. Open the VirtualBox Manager UI:
    2. Right-click the icon for your VM.
    3. Go to Settings -> Network -> Advanced -> Port Forwarding
    4. Add a new Port Forwarding rule as: 

        ```
        Name: mlserver
        Protocol: TCP
        Host Port: 9000 
        Guest Port: 9000
        ```
