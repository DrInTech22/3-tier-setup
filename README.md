
# 3_tier_project

This is a repository to optimize deployment of 3_tier_applications to ensure consistency, reliability and scalability.

Each stage of this project will be saved in the git branches.

This 'main' branch represents the first stage which is containerization.

## Project overview
The web tier of this application is written in react and designed to be served by nodejs 'serve' server. The app tier is written in nodejs and mysql is used for the database.

This project will optimize different facets of the project to enhance security, efficiency and granular configuration.


## Containerizing the application tier
- use a Dockerfile to create a docker image of the node.js application.
Hint: In the dockerfile, the steps should copy the dependencies file, install the dependencies and then copy the application files. After that, set the command to start the application using 'npm' or 'node'.


## Containerizing the web tier
- use a Dockerfile to create a docker image of the frontend react application.
Hint: In the dockerfile,the steps should copy the dependencies file(package*.json), install the dependencies and copy the application files. After that, set the command to install 'serve' globally and then use it to run the application.

## Ensure you document your process
