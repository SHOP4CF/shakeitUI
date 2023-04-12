# ShakeitUI

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#about-the-project">About the Project<a/></li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
        <li><a href="#running">Running</a></li>
      </ul>
    </li>
    <li>
      <a href="usage-notes">Usage Notes</a>
      <ul>
        <li><a href="#overview-of-class-relations">Overview of Class Relations</a></li>
        <li><a href="#using-qtdesigner">Using QtDesigner</a></li>
      </ul>
    </li>
  </ol>
</details>


<!-- ABOUT THE PROJECT -->
## About the Project
<p align="middle">
  <img src="https://user-images.githubusercontent.com/113982478/218409653-ab1c46cc-d6f0-4066-910a-ad5d91cfc9d2.png" width="32%" />
  <img src="https://user-images.githubusercontent.com/113982478/226293911-ef513eab-1340-4048-8342-c3b3aff39422.png" width="32%" /> 
  <img src="https://user-images.githubusercontent.com/113982478/218114114-edf41504-54c4-4b60-b389-5789b919fc4a.png" width="32%" />
</p>

This project contains the UI for the [shakeit component](https://github.com/SHOP4CF/shakeit). It uses KeyRock for authentication of users.

<!-- GETTING STARTED -->
## Getting Started
To get a local copy up and running follow these steps.

### Prerequisites

* **Docker**
  * Windows: [Installing docker desktop on windows](https://docs.docker.com/desktop/install/windows-install/#install-docker-desktop-on-windows)
* **npm and node.js**
  * Windows:
    ```sh
    npm install -g npm
    ```
  * Linux:
    ```sh
    sudo apt install nodejs npm
    ```
* **pyqt5**
  * Windows:
    ```sh
    pip install pyqt5
    ```
  * Linux: 
    ```sh
    sudo apt install python3-pyqt5
    ```
* **Python requests**
  * Windows:
    ```sh
    pip install requests
    ```
  * Linux:
    ```sh
    sudo apt-get install python3-requests
    ```


### Installation
Before installation of this project KeyRock should be set up. To do so follow the steps below.

1.  Clone KeyRock Proxy repository:

    ```console
    git clone https://github.com/ging/fiware-idm.git
    ```

2.  Duplicate config.template in config.js:

    ```console
    cp config.js.template config.js
    ```

3.  Configure data base access credentials:

    ```javascript
    config.database = {
        host: 'localhost', // default: 'localhost'
        password: 'idm', // default: 'idm'
        username: 'root', // default: 'root'
        database: 'idm', // default: 'idm'
        dialect: 'mysql' // default: 'mysql'
    };
    ```

4.  Configure the server to listen HTTPS requests by generating certificates OpenSSL. You may be asked to enter information that will be incorporated into your certificate request (mostly happens for linux users). If this happens make sure to fill out at least one of the fields, if you dont the request wont go through.

    ```console
    ./generate_openssl_keys.sh
    ```
    
    and configuring config.js:
    
    ```javascript
    config.https = {
        enabled: true, //default: 'false'
        cert_file: 'certs/idm-2018-cert.pem',
        key_file: 'certs/idm-2018-key.pem',
        port: 443
    };
    ```

5.  Navigate to ```extras/docker``` directory and copy the Dockerfile into the root. Then replace the whole RUN statement on line 69-86 with the following COPY statement:
    ```DockerFile
    COPY . /opt/fiware-idm
    ```

6. Navigate to ```extras/docker``` directory and copy the docker-compose.yml file into the root. Remove the mailer (line 27-29 and 61-74) and add the following two lines under enviroment for the keyrock service. After this keyrock is ready.
    ```docker-compose
          - IDM_HTTPS_ENABLED=true
          - IDM_HTTPS_PORT=443
    ```

7. Lastly clone this repository.
   ```sh
   git clone https://github.com/SHOP4CF/shakeitUI.git
   ```
   
You should now have 2 repositories set up: "fiware-idm" and "shakeitUI".

### Running

1. Start KeyRock container using the dockercompose file (in the fiware-idm)
   ```sh
   docker-compose up
   ```
   Go to localhost:3000 to see the KeyRock site running.
   
2. The first time the code is run an application should be generated in KeyRock. To do this run the file ```generateApplication.py``` (in shakeitUI). This should modify ```applicationInfo.json```. This step only needs to be done before the first time ```Main.py``` is run, and this step can therefore be skipped the subsequent times.
    ```sh
   python generateApplication.py
   ```

3. Run ```Main.py``` (in the shakeitUI)
   ```sh
   python Main.py
   ```
   
To login to the application use the following credentials:

Username: ```admin@test.com```

Password: ```1234```

<!-- USAGE NOTES -->
## Usage Notes

### Overview of Class Relations
<p align="middle">
  <img src="https://user-images.githubusercontent.com/113982478/231374396-71187e20-5bb7-4fa6-848f-6c62a3a662dc.png"/>
</p>

UI files are excluded from this diagram. The UI files is only used by the matching python file, fx: Interation.py -> InteractionUI.py

### Using QtDesigner
The projects visual component is designed and set up using QtDesigner. If it is desired to make changes to the visual of the UI, it is recommended to use QtDesigner. QtDesigner comes with most installtions of pyqt5.

If you are using Linux and QtDesigner is not installed it can be installed by using the following command.
```sh
sudo apt install qttools5-dev-tools 
```

The file ```MainUI.ui``` in this project is a qt file, and can be opened in QtDesigner. Use QtDesigner to open the file and make changes to it. Before changes from this file can be seen in the code a python file should be genereated based on the changed ```MainUI.ui```. Run the following command in the directory where ```MainUI.ui``` is located to do so:

```sh
python -m PyQt5.uic.pyuic -x MainUI.ui -o MainUI.py
```

This command overwrites the old ```MainUI.py```, so as a general rule changes should **not** be made to ```MainUI.py```. Instead visual changes should be made by QtDesigner and functunality should be in ```Main.py```.


This rule also counts for the other ```.ui``` files. The same command also works for them:

```sh
python -m PyQt5.uic.pyuic -x InteractionUI.ui -o InteractionUI.py
```

```sh
python -m PyQt5.uic.pyuic -x ExitDialogUI.ui -o ExitDialogUI.py
```

```sh
python -m PyQt5.uic.pyuic -x TimesUpDialogUI.ui -o TimesUpDialogUI.py
```
