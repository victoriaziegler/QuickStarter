import json
import yaml

from messages import *


def get_config_file():
    config_file = {}
    try:
        f = open("config.json")
        config_file = json.load(f)
        f.close()
    except FileNotFoundError:
        try:
            f = open("config.yaml")
            config_file = yaml.load(f)
            f.close()
        except FileNotFoundError:
            print(f"\n\n{p}   No config file has been added")
    return config_file


def sanitize_app_list(app_list, micro):
    apps = []
    for app in app_list:
        if app.lower().strip() == "default":
            apps.append(f"{micro}_rest")
        else:
            success =  False
            while not success:
                if validate_name(app):
                    success = True
                    apps.append(app.strip())
                else:
                    name_input_error(app,"app")
                    app = single_input(f"{y}Re-enter app name: {cl}","app")
    return apps


def sanitize_config(config):
    if config.get("main"):
        main = config["main"]
        if main.get("volume"):
            volume = main["volume"].strip()
            success = False
            while not success:
                if validate_name(volume):
                    success = True
                else:
                    name_input_error(volume, "volume")
                    volume = single_input(
                        f"{g}\nVolume Name: {w}", "volume"
                    ).strip()
            main["volume"] = volume
        if main.get("port"):
            port = main["port"]
            success = False
            while not success:
                try:
                    port = int(port)
                    success = True
                except ValueError:
                    port_number_error(port)
                    port = input(
                        f"{g}Enter a valid port number for the shared main port: "
                    )
            main["port"] = port
    if config.get("micros"):
        micros = config["micros"]
        used_ports = []
        key_clean_up = {}
        key_copys = []
        [key_copys.append(key) for key in micros.keys()]
        for key in key_copys:
            new_key = key
            success = False
            while not success:
                if validate_name(new_key):
                    success = True
                else:
                    name_input_error(new_key, "microservice")
                    new_key = single_input(f"{g}Microservice name: {cl}", "microservice")
            key_clean_up[new_key] = micros[key]
        config["micros"] = key_clean_up
        micros = config["micros"]
        for key in micros.keys():
            if micros[key].get("port"):
                port = micros[key]["port"]
                port = validate_ports(key, port, used_ports)
                micros[key]["port"] = port
            if micros[key].get("apps"):
                app_list = micros[key].get("apps")
                apps = sanitize_app_list(app_list, key)
                micros[key]["apps"] = apps
            else:
              micros[key]["apps"] = [f"{key}_rest"]
        config["used_ports"] = used_ports
    return config


def get_volume_and_main_port(config):
    if config.get("main"):
        main = config["main"]
        if main.get("volume"):
            volume_name = main["volume"].strip()
        else:
            volume_name = single_input(f"{g}\nVolume Name: {w}", "volume")
        if main.get("port"):
            main_port = main["port"]
        else:
            main_port = port_input(f"{g}\nAdd the main port that your backend microservices share: {w}")
    else:
        volume_name = single_input(f"{g}\nVolume Name: {w}", "volume")
        main_port = port_input(f"{g}\nAdd the main port that your backend microservices share: {w}")
    return volume_name, main_port


def single_input(prompt, name_type):
    success = False
    val = input(prompt)
    while not success:
        if validate_name(val):
            success = True
        else:
            name_input_error(val, name_type)
            val = input(prompt)
    return str(val).strip()


def name_input(prompt):
    val = input(prompt)
    return str(val).strip()


def validate_name(name):
    for character in name:
        if character in special_characters:
            return False
        if len(name.split()) > 1:
            return False
    return True


def port_input(prompt):
    invalid = True
    while invalid:
        input_val = input(prompt)
        try:
            val = int(input_val)
            invalid=False
        except ValueError:
            port_number_error(input_val)
    return val


def add_inquiry(prompt):
    val = input(prompt)
    if not val:
        return False
    val = val.lower().strip()
    if val[0] == "a" or val[0] == "y":
        return True
    else:
        return False


def list_to_string(array):
    copy = array.copy()
    if len(copy) > 1:
        last_index = len(copy) - 1
        last_item = copy[last_index]
        updated = f"& {last_item}"
        copy[last_index] = updated
        result = ", ".join(copy)
    else:
        result = "".join(copy)
    return result


def port_list_string(ports):
    ports_copy = []
    [ports_copy.append(str(num)) for num in ports]
    port_list = list_to_string(ports_copy)
    return port_list


def get_apps_list(ref, key):
    if key:
        if ref.get(key):
            apps = ref[key]["apps"].copy()
            apps_string = list_to_string(apps)
            return apps, apps_string
    return [],""


def confirm_poller(micros, f_micro):
    if micros.get("poller") == False or micros.get("poller") == True:
        poller = micros["poller"]
    else:
        poller = add_inquiry(f"{g}\nWould you like to add a poller to {f_micro} ? [y/n]: {w}")
    return poller


def add_microservice_port(micros, used_ports, f_micro):
    if not micros.get("port"):
        success = False
        while not success:
            micro_port = port_input(
                f"{g}\nAdd port that {f_micro} will use inside project: {w}"
            )
            if micro_port not in used_ports:
                success = True
                used_ports.append(micro_port)
            else:
                port_list = port_list_string(used_ports)
                duplicate_port_error(micro_port, used_ports, port_list)

    else:
        micro_port = micros["port"]
    return micro_port, used_ports


def validate_ports(name, port, used_ports):
    success = False
    while not success:
        try:
            port = int(port)
            if port not in used_ports:
                used_ports.append(port)
                success = True
            else:
                port_list = port_list_string(used_ports)
                duplicate_port_error(port, used_ports, port_list)
                port = input(
                    f"{g}Enter another port number for {y}\"{u}{name}{ru}\"{cl}: "
                )
        except ValueError:
            port_number_error(port)
            port = input(
                f"{g}Enter a valid port number for {y}\"{u}{name}{ru}\"{cl}: "
            )
    return port


def input_list(prompt):
    updated = []
    val = input(prompt)
    entry_validated = False
    while not entry_validated:
        if "|" not in val and len(val.split()) > 1:
            inline_config_format_error()
            val = input(prompt)
        else:
            entry_validated = True
    array = val.split("|")
    [updated.append(configuration.strip()) for configuration in array]
    config = {
        "micros": {}
    }
    con = config["micros"]
    used_ports = []
    for entry in updated:
        if "/" in entry:
            piece = entry.split("/")
            name = piece[0].strip()
            name_valid = False
            while not name_valid:
                if validate_name(name):
                    name_valid = True
                else:
                    name_input_error(name, "microservice")
                    name = single_input(f"{g}Re-enter microservice name: {cl}", "microservice")
            port = piece[1].strip()
            port = validate_ports(name, port, used_ports)
            f_name = f"{y}\"{u}{name}{ru}\"{g}"
            con[name] = {"port": port}
            try:
                if piece[2].lower().strip() == "y":
                    con[name]["poller"] = True
                else:
                    con[name]["poller"] = False
            except IndexError:
                con[name]["poller"] = None
            try:
                service = piece[3].split(":")
                if len(service) == 1 or not validate_name(service[0]):
                    success = False
                    while not success:
                        if len(service) > 1 and validate_name(service[0]):
                            success = True
                        elif len(service) == 1:
                            project_name_error1(service[0])
                            retry = name_input(
                                f"{g}Enter the project name and apps for the {f_name} microservice:{cl} "
                            )
                            service = retry.split(":")
                        elif not validate_name(service[0]):
                            project_name_error2(f"{g}{service[0]}{p}:{cy}{service[1]}")
                            retry = name_input(
                                f"{g}Enter the project name and apps for the {f_name} microservice:{cl} "
                            )
                            service = retry.split(":")
                if service[0]:
                    con[name]["project"] = service[0].strip()
                else:
                    con[name]["project"] = f"{name}_project"
                if service[1]:
                    app_list = service[1].split(",")
                    apps = sanitize_app_list(app_list, name)
                    con[name]["apps"] = apps
                else:
                    con[name]["apps"] = [f"{name}_rest"]
            except IndexError:
                con[name]["project"] = f"{name}_project"
                con[name]["apps"] = [f"{name}_rest"]
        else:
            con[entry] = {
                "port": None,
                "poller": None,
                "project": f"{entry}_project",
                "apps": [f"{entry}_rest"]
            }
    config["used_ports"] = used_ports
    return config


def queue_retry(ref, q, q_list):
    retry = ""
    while ":" not in retry:
        retry = input(f"{g}Add Queue:{cl} ")
        if ":" not in retry:
            queue_no_colon_error(retry, ref, q, q_list)
    return retry, retry.split(":")


def get_queue_info(config, micro_array):
    micros_ref = config["micros"]
    if not config.get("queues"):
        queue_message(micros_ref)
        config["queues"] = process_queue_info(micro_array, {}, micros_ref)
    else:
        temp = process_queue_info(micro_array, config["queues"], micros_ref)
        if temp:
            config["queues"] = temp
        else:
            config["queues"] = {}

    if config.get("queues") and config["queues"].get("consumers"):
        needs_rabbit = rabbit_list(config["queues"]["consumers"])
    else:
        needs_rabbit = []
    return config, needs_rabbit


def process_queue_info(microservices, input_config, ref):
    queue_config = {}
    if not input_config :
        queues_input= input(f"{g}Add Queues:{w} ").strip()
        entry_validated = False
        while not entry_validated:
            if "|" not in queues_input and len(queues_input.split()) > 1:
                inline_queue_input_error(ref)
                queues_input = input(f"{g}Add Queues:{w} ")
            else:
                entry_validated = True
        if not queues_input:
            return {}
        else:
            queues = queues_input.split("|")
            consumer_dict, producer_dict = sanitize_queue_entries(queues, microservices, ref)
    else:
        queues  = []
        for consumer in input_config:
            producers = []
            [producers.append(producer.strip()) for producer in input_config[consumer]]
            producers = ",".join(producers)
            queue = f"{consumer}:{producers}"
            queues.append(queue)
        consumer_dict, producer_dict = sanitize_queue_entries(queues, microservices, ref)
    queue_config["consumers"] = consumer_dict
    queue_config["producers"] = producer_dict
    return queue_config


def sanitize_queue_entries(queues, microservices, ref):
    consumer_dict = {}
    producer_dict = {}
    q_list = queues.copy()
    micro_list = list_to_string(microservices)
    for q, entry in enumerate(queues):
        success = False
        while not success:
            if ":" in entry:
                pieces = entry.split(":")
                pair = []
                [pair.append(piece.strip()) for piece in pieces]
                if not pair[0]:
                    queue_no_consumer_error(
                        f"{g}{pair[0]}{p}:{cy}{pair[1]}",
                        ref,
                        q,
                        q_list
                    )
                    entry, pair = queue_retry(ref, q, q_list)
                if not pair[1]:
                    queue_no_producers_error(
                        f"{g}{pair[0]}{p}:{cy}{pair[1]}",
                        ref,
                        q,
                        q_list
                    )
                    entry, pair = queue_retry(ref, q, q_list)
                if not validate_name(pair[0]):
                    invalid_consumer_error(
                        f"{g}{pair[0]}{p}:{cy}{pair[1]}",
                        ref,
                        q,
                        q_list
                    )
                    entry, pair = queue_retry(ref, q, q_list)
                if pair[0].strip() not in microservices:
                    not_a_microservice_error(
                        pair[0],
                        f"{g}{pair[0]}{p}:{cy}{pair[1]}",
                        micro_list,
                        q,
                        q_list,
                        ref
                    )
                    entry, pair = queue_retry(ref, q, q_list)

                if pair[0] and pair[1] and "," not in pair[0] and pair[0] in microservices:
                    valid = True
                if valid:
                    consumer = pair[0].strip()
                    producers = []
                    prods = pair[1].split(",")
                    for prod in prods:
                        prod = prod.split("@")
                        if len(prod) <= 1:
                                format_error(consumer,prod[0],ref,q,q_list)
                                correct_format = False
                                while not correct_format:
                                    prod_retry = input(f"{g}Re-enter Producer: {cl}").strip()
                                    prod_retry = prod_retry.split("@")
                                    if len(prod_retry) > 1 and prod_retry[0] and prod_retry[1]:
                                        prod_pair = []
                                        [prod_pair.append(piece.strip()) for piece in prod_retry]
                                        correct_format = True
                                    else:
                                        format_error(consumer,prod_retry[0],ref,q,q_list)
                        else:
                            prod_pair = []
                            [prod_pair.append(piece.strip()) for piece in prod]
                        valid_producer = False
                        while not valid_producer:
                            apps, apps_string = get_apps_list(ref, prod_pair[0])
                            if prod_pair[0] and prod_pair[1].lower() == "default":
                                prod_pair[1] = f"{prod_pair[0]}_rest"

                            if not prod_pair[0]:
                                no_producer_microservice_error(
                                    f"{g}{prod_pair[0]}{p}@{cy}{prod_pair[1]}",
                                    micro_list,
                                    q,
                                    q_list,
                                    ref
                                )
                                prod_pair[0] = input(
                                    f"{g}Which microservice will be the producer be in? {cl}"
                                ).strip()
                                apps, apps_string = get_apps_list(ref, prod_pair[0])

                            if prod_pair[0] == consumer:
                                producer_equals_consumer_error(
                                    f"{g}{prod_pair[0]}{p}@{cy}{prod_pair[1]}",
                                    micro_list,
                                    q,
                                    q_list,
                                    ref
                                )
                                prod_pair[0] = input(
                                    f"{g}Which microservice will be the producer be in? {cl}"
                                ).strip()
                                apps, apps_string = get_apps_list(ref, prod_pair[0])

                            if prod_pair[0] not in microservices:
                                not_a_microservice_error(
                                    prod_pair[0],
                                    f"{g}{prod_pair[0]}{p}@{cy}{prod_pair[1]}",
                                    micro_list,
                                    q,
                                    q_list,
                                    ref
                                )
                                prod_pair[0] = input(
                                    f"{g}Which microservice did you mean?{cl} "
                                ).strip()
                                apps, apps_string = get_apps_list(ref, prod_pair[0])

                            if not prod_pair[1]:
                                producer_path_error(
                                    prod_pair[0],
                                    f"{g}{prod_pair[0]}{p}@{cy}{prod_pair[1]}",
                                    apps_string,
                                    q,
                                    q_list,
                                    ref
                                )

                                prod_pair[1] = input(
                                    f"{g}Which app will be the producer?{cl} "
                                ).strip()

                            if prod_pair[1] not in apps:
                                app_does_not_exist_error(
                                    prod_pair[1],
                                    prod_pair[0],
                                    apps_string,
                                    q,
                                    q_list,
                                    ref
                                )
                                prod_pair[1] = input(
                                    f"{g}Which app will be the producer?{cl} "
                                ).strip()

                            if prod_pair[0] and prod_pair[1] and prod_pair[0] in microservices and prod_pair[0] != consumer and prod_pair[1] in apps:
                                valid_producer = True
                        if not producer_dict.get(prod_pair[0]):
                            producer_dict[prod_pair[0]] = {}
                            producer_dict[prod_pair[0]][prod_pair[1]] = [consumer]
                        elif not producer_dict[prod_pair[0]].get(prod_pair[1]):
                            producer_dict[prod_pair[0]][prod_pair[1]] = [consumer]
                        else:
                            producer_dict[prod_pair[0]][prod_pair[1]].append(consumer)

                        producers.append([prod_pair[0], prod_pair[1]])
                    if consumer_dict.get(consumer):
                        [consumer_dict[consumer].append(producer) for producer in producers]
                    else:
                        consumer_dict[consumer] = producers
                    success = True
                    updated_entry = f"{g}{consumer}:"
                    for j, group in enumerate(producers):
                        if j == 0:
                            updated_entry += f" {group[0]}@{group[1]}"
                        else:
                            updated_entry += f", {group[0]}@{group[1]}"
                    q_list[q] = updated_entry
            else:
                queue_no_colon_error(entry, ref, q, q_list)
                entry, pair = queue_retry(ref, q, q_list)
    success_message()
    return consumer_dict, producer_dict

