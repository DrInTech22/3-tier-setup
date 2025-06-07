
# 3_tier_project

This is a repository to optimize deployment of 3_tier_applications to ensure consistency, reliability and scalability.

Each stage of this project will be saved in the git branches.

This 'main' branch represents the first stage which is containerization.

## dev environment
- node version (18.x.x) 
- npm install 
- npm start

## Prod environment
- node version (18.x.x)
- npm install 
- npm run build

## Project overview
The web tier of this application is written in react and designed to be served by nodejs 'serve' server. The app tier is written in nodejs and mysql is used for the database.

This project will optimize different facets of the project to enhance security, efficiency and granular configuration.


## Containerizing the application tier
- use a Dockerfile to create a docker image of the node.js application.
Hint: In the dockerfile, the steps should copy the dependencies file, install the dependencies and then copy the application files. After that, set the command to start the application using 'npm' or 'node'.
```sh
docker run  \
  --name web-tier \
  -p 80:80 \
  -v ./nginx.conf:/etc/nginx/conf.d/default.conf
  --network database
  web-tier:latest
```

## Containerizing the web tier
- use a Dockerfile to create a docker image of the frontend react application.
Hint: In the dockerfile,the steps should copy the dependencies file(package*.json), install the dependencies and copy the application files. After that, set the command to install 'serve' globally and then use it to run the application.


# Then run it
```sh
docker run -d \
  --name api \
  -e DB_PWD=dbpassword \
  -e DB_DATABASE=demo_db \
  -e DB_HOST=mysql-app \
  -e DB_USER=db_user  \
  -p 4000:4000 \
  web-tier:latest

docker run \
  --name app-tier \
  -e DB_PWD=rootpassword  \
  -e DB_DATABASE=demo_db \
  -e DB_HOST=mysql-app \
  -e DB_USER=root \
  -p 4000:4000 \
  --network database \
  app-tier:latest 
```
## Setting up the database
```sh
echo "DB_PWD=your_db_password
DB_DATABASE=your_db_name
DB_HOST=mysql-app
DB_USER=your_db_user
DB_ROOT_PWD=your_root_password
PHP_PORT=3306" > .env
```

```sh
docker run -d \
  --name mysql-app \
  -e MYSQL_ROOT_PASSWORD=${MYSQL_ROOT_PASSWORD} \
  -e MYSQL_USER=${MYSQL_USER} \
  -e MYSQL_PASSWORD=${MYSQL_PASSWORD} \
  -e MYSQL_DATABASE=${MYSQL_DATABASE} \
  -v ./init:/docker-entrypoint-initdb.d \
  -v database:/var/lib/mysql \
  mysql:8.0.39

docker run \
  --name mysql-app \
  -e MYSQL_ROOT_PASSWORD=rootpassword \
  -e MYSQL_USER=db_user  \
  -e MYSQL_PASSWORD=dbpassword \
  -e MYSQL_DATABASE=demo_db \
  -v ./init:/docker-entrypoint-initdb.d \
  -v database:/var/lib/mysql \
  mysql:8.0.39

docker run \
  --name mysql-app \
  -e MYSQL_ROOT_PASSWORD=rootpassword \
  -e MYSQL_USER=db_user  \
  -e MYSQL_PASSWORD=dbpassword \
  -e MYSQL_DATABASE=demo_db \
  -v ./init:/docker-entrypoint-initdb.d \
  --network database
  mysql:5.7
```
/var/lib/volumes
- Optionally set up phpmyadmin
```
docker run -d \
  --name php-app \
  -e PMA_HOST=mysql-app \
  -e PMA_PORT=3306 \
  -e MYSQL_ROOT_PASSWORD=your_root_password \
  -p 30002:80 \
  phpmyadmin/phpmyadmin:4.7
```


## Ensure you document your process
