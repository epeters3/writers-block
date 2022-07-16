# An AI Language Model Web Server

Includes an AI server hosting a lightweight GPT-2 process and a web app server that serves up a simple UI for interacting with GPT-2. Both interact with each other via Redis. This allows for the AI server and web app server to be deployed on multiple nodes. Redis is used as a job queue for calls to GPT-2 and as a cache for results to queries already made to GPT-2.

Here is an example of GPT-2 continuing a prompt in the web app UI:

![Entering a one paragraph example story prompt and seeing GPT-2's result in the web app UI](./assets/ui-example.png)

## Running

Please ensure you have docker and docker-compose installed. Then, from the project's root directory, run:

```sh
docker-compose up --build
```

This will start up the api server, a redis queue, and the language model queue worker. By default, the UI corresponding to the HTTP API server should be accessible at `http://localhost:5000/`
