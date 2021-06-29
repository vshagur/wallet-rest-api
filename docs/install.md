## Install

#### Install Docker

You need to install Docker. Follow the instructions: [Install Docker](https://docs.docker.com/engine/installation/)

#### Install docker-compose

Follow the instructions - [Install Docker Compose](https://docs.docker.com/compose/install/#install-compose).

#### Configure Docker Management as a Non-Root User.

```
$ sudo groupadd docker
$ sudo gpasswd -a ${USER} docker
$ sudo service docker restart
$ sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose
```
[More details.](https://docs.docker.com/engine/install/linux-postinstall/#manage-docker-as-a-non-root-user)

#### Clone a project from the repository. 

```
$ git clone https://github.com/vshagur/wallet-rest-api.git
$ cd wallet-rest-api/
```
#### Build and initialize the project

Using Makefile: 
```
$ make init
```
Make sure the build was successful and run your tests.

```
$ make test
```

#### Start up.

```
$ make run
```
