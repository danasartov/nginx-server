# Nginx-server
This is a project created by Dana Sartov.

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

### Rate limiting
The nginx server on port 8080 has a rate limit.
It's configured in the nginx.conf file, under html section.
The rate is set to 5 requests per second, and can be modified to x requests p/s by modifing "rate={x}r/s".
The limit is per IP, if the rate limit is exceeded it returns a 429 status code.

## Manual execution
In the Test\test.py file change HOST to "localhost".

run on terminal:
```bash
docker compose up --build

To view the pages in a browser, go to:
- https://localhost:8080
- https://localhost:8081
