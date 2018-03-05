# Installation instructions

Setup the the repo and the application's environment.

1. Install os-level dependencies:

    ```bash
    $ sudo apt-get update
    $ sudo apt-get install virtualenv build-essential imagemagick \
      python-dev libjpeg-dev zlib1g-dev libtiff5 libtiff5-dev
    ```

    _TODO: Refine above package list to minimum needed for PIL to install._

2. Clone the git repository:

    ```bash
    $ git clone https://michaelcurrin@bitbucket.org/michaelcurrin/machine-learning-server.git
    $ cd machine-learning-server
    ```

3. Install python dependencies:
    * Create a Python 2.7 virtual environment then install packages. You may ignore the `--python` flag if your default system is Python 2.X.
    * Note that a flag to access system site packages is _not_ necessary.

    ```bash
    $ git checkout develop
    $ virtualenv virtualenv --python=python2.7
    $ source virtualenv/bin/activate
    (virtualenv) $ pip install pip --upgrade
    (virtualenv) $ pip install -r requirements.txt
    ```

4. Create local conf files in etc dir.
    * app.local.conf 
 
        ```
        ### Local App configuration ###

        ### Site wide service settings
        [service]
        runAsDaemon: False
        ```
        
    * http.local.conf _FIXME: When nginx is implemented, we can leave host as default and the socket_host line can be removed here._

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
