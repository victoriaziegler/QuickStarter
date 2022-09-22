from helpers import *

def start_compose_file(volume, micros):
    compose_file = {
        "volumes": {
            volume: {
                "external": True
            }
        },
        "services": {
            "database": {
                "image": "postgres:14.2-bullseye",
                "volumes": [
                    f"{volume}:/var/lib/postgresql/data",
                    "./db:/docker-entrypoint-initdb.d"
                ],
                "environment": [
                    f"POSTGRES_MULTIPLE_DATABASES={micros}",
                    "POSTGRES_PASSWORD=test-databases"
                ],
                "ports": ["15432:5432"]
            }
        }
    }
    return compose_file


def react_docker_compose():
    temp_dict = {
        "image": "node:lts-bullseye",
        "command": "/bin/bash run.sh",
        "working_dir": "/app",
        "volumes": ["./frontend/app:/app"],
        "ports": ["3000:3000"],
        "environment": {
            "NODE_ENV": "development",
            "HOST": "0.0.0.0"
        }
    }
    return temp_dict


def micro_docker_compose(micro, ports):
    temp_dict = {
        "build": {
            "context": f"./{micro}/api",
            "dockerfile": "./Dockerfile.dev"
        },
        "ports":[f"{ports}"],
        "volumes": [f"./{micro}/api:/app"],
        "depends_on": ["database"],
        "environment": {
            "DATABASE_URL": f"postgres://{micro}:password@database:5432/{micro}",
            "WAIT_HOSTS": "database:5432",
            "WAIT_TIMEOUT": 240
        }
    }
    return temp_dict


def poll_docker_compose(micro, port, project, app_list):
    temp_dict = {
        "build": {
            "context": f"./{micro}/poll",
            "dockerfile": "./Dockerfile.dev"
        },
        "volumes": [
            f"./{micro}/poll:/app"
        ],
        "depends_on": ["database", f"{micro}-api"],
        "environment": {
            "DATABASE_URL": f"postgres://{micro}:password@database:5432/{micro}",
            "WAIT_HOSTS": f"database:5432,{micro}-api:{port}",
            "WAIT_TIMEOUT": 240
        }
    }
    temp_dict["volumes"].append(f"./{micro}/api/{project}:/app/{project}")
    [temp_dict["volumes"].append(f"./{micro}/api/{app[0]}:/app/{app[0]}") for app in app_list]
    return temp_dict


def queue_docker_compose(micro, project, app_list):
    temp_dict = {
        "build": {
            "context": f"./{micro}/queue",
            "dockerfile": "./Dockerfile.dev"
        },
        "volumes": [
            f"./{micro}/queue:/app",
        ],
        "depends_on": ["database", "rabbitmq"],
        "environment": {
            "DATABASE_URL": f"postgres://{micro}:password@database:5432/{micro}",
            "WAIT_HOSTS": f"database:5432, rabbitmq:5672",
            "WAIT_TIMEOUT": 240
        }
    }
    temp_dict["volumes"].append(f"./{micro}/api/{project}:/app/{project}")
    [temp_dict["volumes"].append(f"./{micro}/api/{app[0]}:/app/{app[0]}") for app in app_list]
    return temp_dict


def microservice_docker_dev():
    contents = add_lines_to_file(
        "FROM python:3.10-bullseye",
        "ENV PYTHONUNBUFFERED 1",
        "WORKDIR /app",
        "ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.9.0/wait /wait",
        "RUN chmod +x /wait",
        "COPY requirements.txt requirements.txt",
        "RUN pip install -r requirements.txt",
        "CMD /wait && python manage.py migrate && python manage.py runserver \"0.0.0.0:8000\""
    )
    with open("Dockerfile.dev", "w") as f:
        file = "".join(contents)
        f.write(file)


def poller_docker_dev():
    contents = add_lines_to_file(
        "FROM python:3.10-bullseye",
        "ENV PYTHONUNBUFFERED 1",
        "WORKDIR /app",
        "ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.9.0/wait /wait",
        "RUN chmod +x /wait",
        "COPY requirements.txt requirements.txt",
        "RUN pip install -r requirements.txt",
        "CMD /wait && python poller.py"
    )
    with open("poll/Dockerfile.dev", "w") as f:
        file = "".join(contents)
        f.write(file)


def queue_docker_dev():
    contents = add_lines_to_file(
        "FROM python:3",
        "ENV PYTHONUNBUFFERED 1",
        "WORKDIR /app",
        "COPY requirements.txt requirements.txt",
        "RUN pip install -r requirements.txt",
        "CMD python consumer.py"
    )
    with open("queue/Dockerfile.dev", "w") as f:
        file = "".join(contents)
        f.write(file)
