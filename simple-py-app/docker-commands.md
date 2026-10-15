## commands

## create docker network
docker network create postgress-network

## To run Postgres 
docker run -d \
-p 5432:5432 \
-e POSTGRES_USER=admin \
-e POSTGRES_PASSWORD=password \
-e POSTGRES_DB=mydb \
--name postgresdb \
--net postgress-network \
postgres

## start Adminer 
docker run -d \
-p 8080:8080 \
--net postgress-network \
--name adminer \
-e ADMINER_DEFAULT_SERVER=postgresdb \
adminer