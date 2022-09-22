from wsgiref.util import application_uri
from helpers import *
from docker import *
from inputs import *


def setup_micro(micro, config):
    service = config["micros"][micro]
    project = f"{micro}_project"
    if service.get("project"):
        project = service["project"]
    run_commands(
        f"mkdir common",
        f"cp ~/quickstarter/dev-templates/json.py common/json.py",
        f"django-admin startproject {project} .",
        "python manage.py migrate",
        "cp ~/quickstarter/dev-templates/dj_api_require.txt requirements.txt",
        "rm -r db.sqlite3"
    )
    apps = service["apps"]
    app_list = []
    for app in apps:
      run_commands(f"python manage.py startapp {app}")
      with open(f"{app}/apps.py", "r") as f:
          contents = f.readlines()
      for line in contents:
          if "class" in line:
              app_config = line.split('(')[0].split()[1]
              app_list.append([app, app_config])
    microservice_docker_dev()
    return project, app_list


def setup_create_react_app():
    run_commands("mkdir frontend")
    os.chdir("frontend")
    run_commands(
        "npx create-react-app app",
        "cp ~/quickstarter/dev-templates/run.sh app/run.sh",
    )


def setup_poller():
    run_commands(
        "mkdir poll",
        "cp ~/quickstarter/dev-templates/poller.py poll/poller.py",
        "cp api/requirements.txt poll/requirements.txt"
    )
    poller_docker_dev()


def setup_queue():
    run_commands(
        "mkdir queue",
        "cp ../requirements.txt queue/requirements.txt",
        "cp ~/quickstarter/dev-templates/queue-consumer.py queue/consumer.py",
    )
    queue_docker_dev()


def clean_up():
    try:
        f = open("config.json")
        f.close()
        run_commands(
            "rm config.json",
            "rm requirements.txt",
        )
    except FileNotFoundError:
        try:
            f = open("config.yaml")
            f.close()
            run_commands(
                "rm config.json",
                "rm requirements.txt",
            )
        except FileNotFoundError:
            run_commands(
                "rm requirements.txt",
            )

