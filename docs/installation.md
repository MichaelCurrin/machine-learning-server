# Installation instructions

Setup the the repo and the application's environment.

Python 3.6 is recommended but Python 3.5 should be fine.

1. Install system dependencies:
    
    ```bash
    $ # Using Debian/Ubuntu package manager.
    $ sudo apt-get update
    $ sudo apt-get install python3-virtualenv
    $ # OR Install the Python3 pip using your system's package manager
    $ # then use it to install virtualenv.
    $ sudo pip3 install virtualenv
    ```

2. Clone the git repository:
   
    ```bash
    $ git clone https://github.com/MichaelCurrin/machine-learning-server.git
    $ cd machine-learning-server
    ```

3. Install Python dependencies:
    
    ```bash
    $ virtualenv venv -p python3.6
    $ source venv/bin/activate
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

5. If running on a virtual machine, configure port forwarding rules:
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
