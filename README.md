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

2. Run Main.py (in the shakeitUI repository)
   ```sh
   python main.py
   ```
   
To login to the application use the following credentials:

Username: ```admin@test.com```

Password: ```1234```
