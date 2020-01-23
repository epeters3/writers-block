# An AI Language Model Web Server

Includes an AI server and an HTTP API server that interact via Redis.

To deploy an AI server:

```shell
git clone https://github.com/epeters3/writers-block.git
cd writers-block
bash deploy-ai.sh
```

To deploy an HTTP API server:

```shell
git clone https://github.com/epeters3/writers-block.git
cd writers-block
bash deploy-api.sh
```

\*Make sure a Redis instance is configured and accessible inside the `writersblock.db` module.
