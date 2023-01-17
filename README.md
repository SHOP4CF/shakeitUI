# ShakeitUI

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#about-the-project">About The Project<a/></li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
        <li><a href="#running">Running</a></li>
      </ul>
    </li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->
## About The Project
<p align="middle">
  <img src="https://user-images.githubusercontent.com/113982478/212876926-aca6b8bf-9550-4c45-84e0-7fec7657ed7c.png" width="33%" />
  <img src="https://user-images.githubusercontent.com/113982478/212877103-0c37d9a8-5b25-4cdb-b522-336b29d5dbcb.png" width="33%" /> 
  <img src="https://user-images.githubusercontent.com/113982478/212877160-96573ae7-e39c-4950-890c-1eb67b306f43.png" width="33%" />
</p>

This project contains the UI for the [shakeit component](https://github.com/SHOP4CF/shakeit). It uses KeyRock for authentication of users.

<!-- GETTING STARTED -->
## Getting Started
To get a local copy up and running follow these steps.

### Prerequisites

* Docker ([Installing docker desktop on windows](https://docs.docker.com/desktop/install/windows-install/#install-docker-desktop-on-windows))
* npm
  ```sh
  npm install -g npm
  ```
* node.js
* pyqt5
  ```sh
  pip install pyqt5
  ```
* requests
  ```sh
  pip install requests
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

4.  Configure the server to listen HTTPS requestsb by generating certificates OpenSSL and configuring config.js:

    ```console
    ./generate_openssl_keys.sh
    ```

    ```javascript
    config.https = {
        enabled: true, //default: 'false'
        cert_file: 'certs/idm-2018-cert.pem',
        key_file: 'certs/idm-2018-key.pem',
        port: 443
    };
    ```

5.  Navigate to ```extras/docker``` directory and copy the Dockerfile into the root. Then replace the whole RUN statement on line 69-86 by the following COPY statement:
    ```DockerFile
    COPY . /opt/fiware-idm
    ```

6. Navigate to ```extras/docker``` directory and copy the docker-compose.yml file into the root. Remove the mailer (line 27-29 and 61-74) and add the following two lines under enviroment for the keyrock service.
    ```docker-compose
          - IDM_HTTPS_ENABLED=true
          - IDM_HTTPS_PORT=443
    ```

7. Now that KeyRock is ready clone this repository.
   ```sh
   git clone https://github.com/SHOP4CF/shakeitUI.git
   ```
   
You should now have 2 repositories set up: "fiware-idm" and "shakeitUI".

### Running

1. Start KeyRock container using the dockercompose file (in the fiware-idm repository)
   ```sh
   sudo docker-compose up
   ```
   Go to localhost:3000 to see the KeyRock site running.
   
2. The first time the code is run an application should be generated in KeyRock. To do this run the file ```generateApplication.py``` (in shakeitUI repository). This should modify ```applicationInfo.json```. This step only needs to be done before the first time ```Main.py``` is run, and this step can therefore be skipped the subsequent times.
    ```sh
   python generateApplication.py
   ```

3. Run ```Main.py``` (in the shakeitUI repository)
   ```sh
   python main.py
   ```
   
To login to the application use the following credentials:

Username: ```admin@test.com```

Password: ```1234```
