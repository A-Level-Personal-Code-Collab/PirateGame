# PirateGame
Know the pirate game we all love from school? Want a digital version?
Our A Level team are aiming to make a fully functioning prirate game!
Run on localHost while developing
---------------------------------------------------------------------
### Running using docker
The pirate game comes with the relevant docker filesystems to
faciliate debugging it within a docker environment. In order to do
this, one must have an instance of docker installed on your system.
This may be downloaded from the official website https://www.docker.com
or the packages ```docker``` and ```docker-compose``` may be installed
from the repos of your linux system.

Once docker is installed, you can use the files in this repo to setup
a docker container. To setup a pirategame container:
1. Navigate to the directory in which the piragegame is downloaded
2. Execute the following command to run the docker container
```docker-compose up -d --build```
3. This will automatically create an image and container

Some common commands can be used to manipulate the created container
```docker container ls``` - Lists the running containers so as to
determine the name of the created container
```docker container restart <container_name>``` - Restart the game

This will host the pirate game on the localhost under port 8000 under
a gunicord wsgi server

---------------------------------------------------------------------
### Editor Notes

Link colour = rgb(145, 145, 145)
Box shadows =  0 4px 8px 0 rgba(0,0,0,0.2)
Secondary header colour = #474e5d
Header colour = #ffd900