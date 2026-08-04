# CSE644 Docker Assignment

## Student Information

- Name: Rod Raemon Alvero
- Course: Advanced Cloud Computing and Cloud Management
- Course Number: CSE644
- Docker Hub Username: rodraemonalvero
- GitHub Username: rodraemonalvero

## Project Overview

This repository demonstrates practical Docker skills, including Docker
installation, Docker Hub authentication, image pulling, container execution,
interactive container access, custom image creation, a Python web application,
HAProxy reverse proxying, persistent volumes, Docker networking, Docker Hub
publishing, and GitHub version control.


## Repository Structure

custom-nginx/
- Dockerfile and customized HTML page for the Nginx container.

python-web/
- Flask web application, Dockerfile, and requirements for the Python web server.

haproxy-nginx/
- Docker Compose project demonstrating HAProxy forwarding requests to an Nginx backend.

networking-demo/
- Files demonstrating Docker bridge, isolated, and host networking.

volume-demo/
- Demonstration of Docker volumes and persistent storage.

screenshots/
- All screenshots captured during the assignment.

## Part 1: Docker Installation

Include commands and screenshot.

## Part 2: Docker Hub Authentication

Include the safe login evidence. Never include the token.

## Part 3: Pull, Run, and Exec

Include the Ubuntu commands and screenshots.

## Part 4: Customized Nginx Image

Explain how to build and run it.

## Part 5: Python Web Server

Explain how to build and run it on port 8888.

## Part 6: HAProxy and Nginx

Explain how docker compose runs both services.

## Part 7: Persistent Volume

Explain how data survived container deletion.

## Part 8: Docker Networking

Explain bridge, isolated, and host networking tests.

## Docker Hub Images

- Customized Nginx:
  https://hub.docker.com/r/rodraemonalvero/cse644-custom-nginx

- Python Web Server:
  https://hub.docker.com/r/rodraemonalvero/cse644-python-web

- HAProxy:
  https://hub.docker.com/r/rodraemonalvero/cse644-haproxy

- HAProxy Backend Nginx:
  https://hub.docker.com/r/rodraemonalvero/cse644-haproxy-nginx

## Security

No passwords, access tokens, API keys, private keys, or environment files
containing secrets are included in this repository.

## Conclusion

This assignment demonstrated the complete Docker workflow from local
installation through image development, container execution, networking,
persistent storage, reverse proxying, Docker Hub publication, and GitHub
version control.