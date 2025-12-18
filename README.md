# Project with Python, Pact and Pact Broker via Docker

This project uses **Python** for development, **Pact** for contract testing, and runs the **Pact Broker** using a Docker container.

## About the project

This repository aims to demonstrate the implementation of contract tests using [Pact](https://docs.pact.io/) in a Python project. The generated contracts are published to a Pact Broker, facilitating integration between consumer and provider API development teams.

## Tecnologies Used

- [Python](https://www.python.org/)
- [Pact PY](https://github.com/pact-foundation/pact-python)
- [Pact Broker](https://docs.pact.io/pact_broker)
- [Docker](https://www.docker.com/)

## Requirements

- [Python](https://www.python.org/) >=3.11.x
- [pip](https://pypi.org/project/pip/)
- [Docker](https://www.docker.com/) installed and running on your machine

## Instalation Guide

```bash

### Cloning the repository
git clone https://github.com/your-user/repo-here.git

### Run through the venv (virtual environment), for this, you need to create and activate it first
python3 -m venv {$name}
source {$name}/bin/activate 

### Copy the all folders and files in the main project and past into your recent created env-folder, and then install the dependencies:
cd {your-venv-folder}
pip install -r requirements.txt

### Then you must download the pact cli compatible version throught the command below:
curl -fsSL https://raw.githubusercontent.com/pact-foundation/pact-cli/main/install.sh | sh

### Runnign the contract tests
pytest ./tests
```

The contract files (pacts) will be generated in the `pacts` directory.

## Up the Pact files using Docker

```dockerfile
docker-compose up -d
```

- The pact broker will be available in your browser at [http://localhost:9292](http://localhost:9292)

- After running the tests, you publish PACT files to the broker:

```dockerfile
pact-broker publish ./pacts \
  --broker-base-url http://localhost:9292 \
  --consumer-app-version {{version-here}}
```

## References

- [Pact PY Oficial Documentation](https://docs.pact.io/implementation_guides/python/readme)
- [Pact Broker Oficial Documentation](https://docs.pact.io/pact_broker)
