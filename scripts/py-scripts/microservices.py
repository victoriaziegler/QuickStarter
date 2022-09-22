import os
import yaml

from setup import *
from update_files import *


config = get_config_file()

if config:
    config = sanitize_config(config)

volume_name, main_port = get_volume_and_main_port(config)

if not config.get("micros"):
    inline_config_message()
    temp = input_list(f"{g}\nList your Microservices: {w}")
    config["micros"] = temp["micros"]
    config["used_ports"] = temp["used_ports"]

microservices = config["micros"].keys()
micro_list = ",".join(microservices)
micro_array = micro_list.split(",")
f_vol = f"{y}\"{u}{volume_name}{ru}\"{g}"
add_lines(f"\n{g}Adding volume {f_vol} to project{w}\n")
run_commands(f"docker volume create {volume_name}")

config, needs_rabbit = get_queue_info(config, micro_array)

compose_file = start_compose_file(volume_name, micro_list)
services = compose_file["services"]

if needs_rabbit:
    services["rabbitmq"] = { "image": "rabbitmq:3"}

used_ports = config["used_ports"]
for microservice in microservices:
    f_micro = f"{y}\"{u}{microservice}{ru}\"{g}"
    run_commands(f"mkdir {microservice}")
    os.chdir(f"{microservice}")
    run_commands("cp ~/quickstarter/dev-templates/python-gitignore.txt .gitignore", "mkdir api")
    os.chdir("api")

    project, app_list = setup_micro(microservice, config)

    micros = config["micros"][microservice]
    micro_port, used_ports = add_microservice_port(micros, used_ports, f_micro)
    ports = f"{micro_port}:{main_port}"
    poller = confirm_poller(micros, f_micro)
    update_settings(microservice, config, project, app_list)

    services[f"{microservice}-api"] = micro_docker_compose(microservice, ports)
    os.chdir("../")

    if poller:
        setup_poller()
        create_poller_file(microservice, project)
        services[f"{microservice}-poller"] = poll_docker_compose(microservice, main_port, project, app_list)
    if config.get("queues") and microservice in config["queues"]["consumers"].keys():
        setup_queue()
        create_queue_cons_file(config["queues"]["consumers"], microservice, project)
        services[f"{microservice}-queue"] = queue_docker_compose(microservice, project, app_list)
    if config.get("queues") and microservice in config["queues"]["producers"].keys():
        update_producer_views_files(config["queues"]["producers"], microservice)
    os.chdir("../")

setup_create_react_app()
services["react"] = react_docker_compose()
os.chdir("../")
clean_up()
with open("compose.yaml", 'w') as file:
    documents = yaml.dump(compose_file, file)
os.system("mv compose.yaml docker-compose.yml")




