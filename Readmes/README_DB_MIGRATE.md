# This is the readme to configure this project with rdb of choice


## We will use example of mysql db with admniner for visualisation


## Prerequisites:
1. Install Docker and docker compose for windows or mac


## Steps to run the docker image:

1. Inside the same directory as [docker-compose.yaml](https://github.com/RahulKeluskar/Abbiocco/blob/master/docker-compose.yaml), run the command:
```bash
docker-compose up -d
```
The above command initialises the mysql db and connects it with the adminer visualisation tool for the db.
2. User ``` docker ps ``` to check if the containers are up
3. The next step is to point the db url from the flask application. There are 2 ways to do it:
    1. export the environment variable  DATABASE_URL=mysql+mysqlconnector://root:rootpassword@localhost:3306/abiocco
    2. Hard code the value in [config.py](https://github.com/RahulKeluskar/Abbiocco/blob/master/config.py#L6)
4. Run the following commands in your virtual environment
*Note: Please remove the migrations directory before running these commands.*
```bash
flask db init
flask db migrate
flask db upgrade
``` 
5. We can got to localhost:8080 to see the db contents. Username is root and password is rootpassword. We can change these in the docker compose file.
