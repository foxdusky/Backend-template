# Backend Template


# [Project Structure](./project-structure.md)

# Deploy

Execute the command

~~~
git clone https://github.com/foxdusky/Cargo-Rates-API.git
~~~

OR

~~~
gh repo clone foxdusky/Cargo-Rates-API
~~~

create an env file in the root of the repository

.env EXAMPLE

~~~
COMPOSE_PROJECT_NAME='YOUR_COMPOSE_PROJECT_NAME'

# DEV OR PROD ENVIRONMENT
IS_DEV_ENV=1

SECRET_KEY='YOUR_SECRET_KEY'

POSTGRES_USER='YOUR_POSTGRES_USER'
POSTGRES_PASSWORD='YOUR_POSTGRES_PASSWORD'

#REPLACE @POSTGRES_USER:@POSTGRES_PASSWORD TO THE REAL ONE

DB_CON_STR=postgresql://@POSTGRES_USER:@POSTGRES_PASSWORD@db:5432/postgres

# Migration con str
#REPLACE @POSTGRES_USER:@POSTGRES_PASSWORD TO THE REAL ONE
#DB_CON_STR=postgresql://@POSTGRES_USER:@POSTGRES_PASSWORD@localhost:5432/postgres


# REPLACE THAT TO REAL PATHS IF THAT IS PROD ENVIRONMENT
SSL_KEY_FILE=./.env
SSL_CERT_FILE=./.env


~~~

run using docker

~~~
docker-compose up -d --build
~~~
