# PirateGame

Know the pirate game we all love from school? Want a digital version?
Our A Level team are aiming to make a fully functioning prirate game!
Run on localHost while developing

---------------------------------------------------------------------
### Running using docker
The pirate game comes with the relevant docker file-systems to
facilitate debugging it within a docker environment. In order to do
this, one must have an instance of docker installed on your system.
This may be downloaded from the official website https://www.docker.com
or the packages ```docker``` and ```docker-compose``` may be installed
from the repos of your linux system.

Once docker is installed, you can use the files in this repo to setup
a docker container. To setup the relevant containers:
1. Navigate to the directory in which the piragegame is downloaded
2. Execute the following command to run the docker containers
```docker-compose up -d --build```
3. This will automatically create a custom pirate game image as well as 3 containers
In order for the game to function correctly, all 3 must be running
4. In order to use the pirategame the database must have some tables in it. Execute the 'database.py' file manually to create the tables in your database. Note: You only need to do this once per installation. Running it again will wipe all data from the database.

Some common commands can be used to manipulate the created container:
1. ```docker container ls``` - Lists the running containers so as to
determine the name of the created container
2. ```docker container restart <container_name>``` - Restart the game
3. ```docker container logs <container_name>``` - Show the historical
output of the the python program.
4. ```docker container attach <container_name>``` - Show all current
output of the program on the console

This will host the pirate game on the localhost under port 8000 under
a gunicord wsgi server

---------------------------------------------------------------------
### Editor Notes

Link colour = rgb(145, 145, 145)
Box shadows =  0 4px 8px 0 rgba(0,0,0,0.2)
Secondary header colour = #474e5d
Header colour = #ffd900
