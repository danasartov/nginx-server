# F5-project
This is a project created for the Devops internship at F5.
It was created by Dana Sartov for the F5 recruiting team.

## How It Works
This repo contains 3 folders: Nginx, Test and Github Action workflow.

### Nginx folder
The Nginx folder contains all the prerequisites for a simple application on ubuntu, with 1 nginx container running 2 application:

- Application 1 runs on port 8080 and serves a simple HTML page with the writing "Hi! nice to meet you".

- Application 2 runs on port 8081 and returns a 503 error.

### Test folder
The test folder contains test image that runs a python script to test both applications on the Nginx.
It sends HTTP requests to both servers, Verifies the status codes and content of application 1, and exits with non zero code if tests fail.

### Github Action
The Github action "docker-compose-ci.yml" runs the docker-compose.yaml at the root of the repo that builds the Nginx and Test images and runs them.
Then, the test.py script runs and tests the Nginx applications, if some test failes then an artifact containing a file name "fail" is created, and if all tests pass then an artifact containing a file name "succeeded" is created.
