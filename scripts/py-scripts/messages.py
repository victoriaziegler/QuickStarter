from sre_constants import SUCCESS
from helpers import *


def inline_config_message():
    lines = [
        blank_line,
        f"{y}You have not added a config file. You can use the the prompt below to add microservices to your project. You can choose to use the full format to expedite the process, or you can go through the full step by step walkthrough.",
        blank_line,
        f"{y}At minimum, you must enter the names of your microservices at this point. Microservices must be separated by \"{p}|{y}\"{cl}.",
        blank_line,
        f"{spe}{u}{p}Example{cl}",
        blank_line,
        f"{sp5}{g} micro1 {p}|{g} micro2 {p}| {g}micro3 {p}|{g}",
        blank_line,
        f"{y}Everything beyond what is above is purely optional and you will be prompted about it later in the walkthrough. The only exception to that is if you would like to change the project or app name or would like to add additional apps to a microservice. See below for more on this. At this point, you can freely use spaces.",
        blank_line,
        f"{y}Additional information for each entry must be separated with \"{p}/{y}\" and must be entered in the correct order.",
        f"{y}The second argument is the port number that the microservice uses.",
        f"{spe}{u}{p}Example{cl}",
        blank_line,
        f"{sp5}{g} micro1{p}/{g}8080",
        blank_line,
        f"{y}Next, enter \"{g}y{y}\" if you want to add a poller to this microservice. If not, you can end the entry with a trailing slash or enter \"{g}n{y}\" if you want to add the last piece of the entry.",
        f"{spe}{u}{p}Example{cl}",
        blank_line,
        f"{sp5}{g} micro1{p}/{g}8080 {sp5} {r}no poller",
        f"{sp5}{g} micro1{p}/{g}8080{p}/ {sp5}{r}no poller",
        f"{sp5}{g} micro1{p}/{g}8080{p}/{g}n {sp4}{r}no poller",
        f"{sp5}{g} micro1{p}/{g}8080{p}/{g}y {sp4}{g}add poller",
        blank_line,
        f"{y}The last argument in the entry is not required, but you will not be asked about it again. By default, the project name will be {g}micro-name_project {y}and it will have one app called {cy}micro-name_rest.{y} If you would like to change either of these names or add apps, this is your only chance to do so.",
        blank_line,
        f"{y}The general format for this part of the entry is shown below.",
        blank_line,
        f"{sp5} {g}microservice{y} : {cy}app1{y}, {cy}app2{y},{cy} app3{y}...{cl}",
        blank_line,
        f"{y}The colon is important. It will determine what is an app and what is a microservice. You can leave either side of the colon blank and the program will infer meaning. ",
        blank_line,
        f"{sp5}{g}Acceptable {sp4} {g}name{y}: {sp3} {p}change project name to {g}name{cl}",
        f"{sp5}{g}Acceptable {sp4} {y}:{cy}name {sp3} {p}change app name to {cy}name{cl}",
        f"{sp5}{r}Unacceptable{sp3} {r}name{cl}",
        blank_line,
        f"{y}If an app name or list of app names is provided, the default app will be overwritten. If you would like to add apps but keep the default app as well, pass {cy}default{y} as one of the app names. ",
        blank_line,
        f"{y}A complete entry will look something like this.",
        blank_line,
        f"{spe}{g} micro1{p}/{g}8080{p}/{g}y{p}/{g}my_micro{p}:{cy}default{y}, {cy}app1{y}, {cy}app2{y} {p}|{g} next entry... ",
        blank_line,
        f"{y}Enter your microservices below.",
        blank_line,
    ]
    message_box("large", blbl, bblu, *lines)


def queue_message(micros):
    lines = [
        f"{y}To add queues to your project now, enter them below using the following format. You may use spaces freely, but characters {p}('{g}:{p}', '{g}@{p}', '{g},{p}', '{g}|{p}'){y} must be used correctly.",
        blank_line,
        f"{spe}{u}{p}Example{cl}",
        f"{spe}{g}cons1{p}: {g}prod1{p}@{cy}app{p},{g}prod2{p}@{cy}app {p}| {g}cons2{p}: {g}prod3{p}@{cy}app {p}| {g}cons3{y}...{cl}",
        blank_line,
        f"{sp4}{y}{u}Your Project{cl}"
    ]
    ending = [
        blank_line,
        f"{y}Press ENTER to skip this step.",
        blank_line,
    ]
    services = create_project_display(micros)
    [lines.append(service) for service in services]
    [lines.append(line) for line in ending]
    message_box("large", blbl, bblu, *lines)


def success_message():
    lines = [
        blank_line,
        f"{sp5}{sp5}{sp5}{sp3}{g}SUCCESS!{cl}",
        blank_line
    ]
    message_box("small", blg, bg, *lines)


def inline_config_format_error():
    lines = [
        blank_line,
        f"{r}{bl}Error!!!{cl}",
        blank_line,
        f"{y}Inline config improperly formatted.{cl}",
        blank_line,
        f"{y}A complete correct entry will look something like this. Refer to inline config instructions above.",
        blank_line,
        f"{spe}{g} micro1{p}/{g}8080{p}/{g}y{p}/{g}my_micro{p}:{cy}default{y}, {cy}app1{y}, {cy}app2{y} {p}|{g} next entry... ",
        blank_line,
        f"{y}Enter your microservices below.",
        blank_line,
    ]
    swapping_box("large", blr, br, *lines)


def port_number_error(current_input):
    lines = [
        blank_line,
        f"{r}{bl}Error!!!{cl}",
        blank_line,
        f"{y}Port number must be an integer",
        blank_line,
        f"{cy}{current_input} {y}is not a valid port number",
        blank_line,
    ]
    swapping_box("small", blr, br, *lines)


def duplicate_port_error(port, used_ports, port_list):
    used_line = f"{p}Ports {cy}{port_list}{p} have been assigned{cl}"
    if len(used_ports) == 1:
        used_line = f"{p}Port {cy}{port_list}{p} has been assigned{cl}"
    lines = [
        blank_line,
        f"{r}{bl}Error!!!{cl}",
        blank_line,
        f"{y}Port{cy} {port}{y} is unavailable",
        blank_line,
        used_line,
        blank_line
    ]
    swapping_box("small", blr, br, *lines)


def name_input_error(name, type):
    lines = [
        blank_line,
        f"{r}{bl}Error!!!{cl}",
        blank_line,
        f"{y}{type.title()} name cannot include spaces or any of the following characaters{cl}",
        blank_line,
        char_line,
        blank_line,
        f"{y}You entered {cy}{name}{cl}",
        blank_line,
    ]
    swapping_box("large", blr, br, *lines)


def project_name_error1(entry):
    lines = [
        blank_line,
        f"{r}{bl}Error!!!{cl}",
        blank_line,
        f"{y}Entry must contain a colon to specify if the name change is for the project or the default app.{cl}",
        blank_line,
        f"{sp5}{g}Acceptable {sp4} {g}name{p}: {sp3} {y}change project name to {g}name{cl}",
        f"{sp5}{g}Acceptable {sp4} {p}:{cy}name {sp3} {y}change app name to {cy}name{cl}",
        f"{sp5}{r}Unacceptable{sp3} {r}name{cl}",
        blank_line,
        f"{y}You entered {entry}{cl}",
        blank_line,
        f"{y}Re-enter the microservice below using the following format.{cl}",
        blank_line,
        f"{sp5} {g}microservice{p} : {cy}app1{p}, {cy}app2{p},{cy} app3{y}...{cl}"
    ]
    swapping_box("large", blr, br, *lines)


def project_name_error2(entry):
    lines = [
        blank_line,
        f"{r}{bl}Error!!!{cl}",
        blank_line,
        f"{y}Microservice name cannot include spaces or any of the following characaters{cl}",
        blank_line,
        char_line,
        blank_line,
        f"{y}You entered {entry}{cl}",
        blank_line,
        f"{y}Re-enter the microservice below using the following format.{cl}",
        blank_line,
        f"{sp5} {g}microservice{p} : {cy}app1{p}, {cy}app2{p},{cy} app3{y}...{cl}"
    ]
    swapping_box("large", blr, br, *lines)


def inline_queue_input_error(micros):
    lines = [
        blank_line,
        f"{r}{bl}Error!!!{cl} ",
        blank_line,
        f"{y}Queues entry improperly formatted.",
        blank_line,
        f"{y}Your entry should be in the following format.",
        blank_line,
        f"{sp5}{g}cons{p} : {g}prod{p}@{cy}app, {g}prod{p}@{cy}app {p}|{g} next entry..." ,
    ]
    ending = [
        blank_line,
        f"{y}Press ENTER to skip this step.",
        blank_line,
    ]
    services = create_project_display(micros)
    [lines.append(service) for service in services]
    [lines.append(line) for line in ending]
    swapping_box("large", blr, br, *lines)


def create_project_display(micros):
    services = [blank_line, f"{sp4}{y}{u}Your Project{cl}"]
    for micro in micros:
        line = f"{sp4}{g}{micro} {p}-->{cy}"
        for i, app in enumerate(micros[micro]["apps"]):
            if i == 0:
                line += f"{spe}{app}"
            else:
                line += f", {app}"
        services.append(line)
    return services


def create_queue_display(index, q_list):
    q_lines = [blank_line, f"{sp4}{u}{p}Sanitizing your queues{cl}"]
    for j, queue in enumerate(q_list):
        if j == index :
            q_line = f"{p}-->{cy}{queue.strip()}"
        elif j > index:
            q_line = f"{sp4}{r}{queue.strip()}"
        else:
            q_line = f"{sp4}{queue.strip()}"
        q_lines.append(q_line)
    return q_lines


def queue_no_consumer_error(current_entry, micros, q, q_list):
    lines = [
        blank_line,
        f"{r}{bl}Error!!!{cl}",
        blank_line,
        f"{y}Queue has no consumer{cl}",
        blank_line,
        f"{y}Your entry should be in the following format.",
        blank_line,
        f"{sp5}{g}cons{p} : {g}prod{p}@{cy}app, {g}prod{p}@{cy}app",
    ]
    ending = [
        blank_line,
        f"{y}Your current entry is {current_entry}{cl}",
        blank_line,
        f"{y}Re-enter your queue entry below",
        blank_line,
    ]
    services = create_project_display(micros)
    q_lines = create_queue_display(q, q_list)
    [lines.append(service) for service in services]
    [lines.append(entry) for entry in q_lines]
    [lines.append(line) for line in ending]
    swapping_box("large", blr, br, *lines)


def queue_no_producers_error(current_entry, micros, q, q_list):
    lines = [
        blank_line,
        f"{r}{bl}Error!!!{cl}",
        blank_line,
        f"{y}Queue has no producers{cl}",
        f"{y}Your current entry is {current_entry}{cl}",
        blank_line,
        f"{y}Your entry should be in the following format.",
        blank_line,
        f"{sp5}{g}cons{p} : {g}prod{p}@{cy}app, {g}prod{p}@{cy}app",
    ]
    ending = [
        blank_line,
        f"{y}Your current entry is {current_entry}{cl}",
        blank_line,
        f"{y}Re-enter your queue entry below",
        blank_line,
    ]
    services = create_project_display(micros)
    q_lines = create_queue_display(q, q_list)
    [lines.append(service) for service in services]
    [lines.append(entry) for entry in q_lines]
    [lines.append(line) for line in ending]
    swapping_box("large", blr, br, *lines)


def invalid_consumer_error(current_entry, micros, q, q_list):
    lines = [
        blank_line,
        f"{r}{bl}Error!!!{cl}",
        blank_line,
        f"{y}Consumer name cannot inlude spaces or any of the following characaters{cl}",
        blank_line,
        char_line,
        blank_line,
        blank_line,
        f"{y}Your entry should be in the following format.",
        blank_line,
        f"{sp5}{g}cons{p} : {g}prod{p}@{cy}app, {g}prod{p}@{cy}app",
    ]
    ending = [
        blank_line,
        f"{y}Your current entry is {current_entry}{cl}",
        blank_line,
        f"{y}Re-enter your queue entry below",
        blank_line,
    ]
    services = create_project_display(micros)
    q_lines = create_queue_display(q, q_list)
    [lines.append(service) for service in services]
    [lines.append(entry) for entry in q_lines]
    [lines.append(line) for line in ending]
    swapping_box("large", blr, br, *lines)


def queue_no_colon_error(current_entry, micros, q, q_list):
    lines = [
        blank_line,
        f"{r}{bl}Error!!!{cl}",
        blank_line,
        f"{y}Consumer and Producers List must be separated by a colon{cl} ",
        blank_line,
        f"{y}Your entry should be in the following format.",
        blank_line,
        f"{sp5}{g}cons{p} : {g}prod{p}@{cy}app, {g}prod{p}@{cy}app",
    ]
    ending = [
        blank_line,
        f"{y}Your current entry is {cy}{current_entry}{cl}",
        blank_line,
        f"{y}Re-enter your queue entry below",
        blank_line,
    ]
    services = create_project_display(micros)
    q_lines = create_queue_display(q, q_list)
    [lines.append(service) for service in services]
    [lines.append(entry) for entry in q_lines]
    [lines.append(line) for line in ending]
    swapping_box("large", blr, br, *lines)


def not_a_microservice_error(word, current_entry, micro_list, q, q_list, micros):
    lines = [
        blank_line,
        f"{r}{bl}Error!!!{cl}",
        blank_line,
        f"{r}{word}{y} is not a valid microservice{cl}",
    ]
    ending = [
        f"{y}Your current entry is {current_entry}{cl}",
        blank_line,
        f"{p}Microservice names{cl}",
        f"{g}{micro_list}{cl}",
        blank_line,
    ]
    services = create_project_display(micros)
    q_lines = create_queue_display(q, q_list)
    [lines.append(service) for service in services]
    [lines.append(entry) for entry in q_lines]
    [lines.append(line) for line in ending]
    swapping_box("large", blr, br, *lines)


def producer_path_error(micro, current_entry, apps, q, q_list, micros):
    lines = [
        blank_line,
        f"{r}{bl}Error!!!{cl}",
        blank_line,
        f"{y}Choose an app that will send data. Which app in {g}{micro}{y} will be the producer?",
    ]
    ending = [
        blank_line,
        f"{y}Your current entry is {current_entry}{y}. Enter one of the app names below to complete the queue.{cl}",
        blank_line,
        f"{p}App names{cl}",
        f"{cy}{apps}{cl}",
        blank_line,
    ]
    services = create_project_display(micros)
    q_lines = create_queue_display(q, q_list)
    [lines.append(service) for service in services]
    [lines.append(entry) for entry in q_lines]
    [lines.append(line) for line in ending]
    swapping_box("large", blr, br, *lines)


def no_producer_microservice_error(current_entry, micro_list, q, q_list, micros):
    lines = [
        blank_line,
        f"{r}{bl}Error!!!{cl}",
        blank_line,
        f"{y}Entry is missing microservice in the producer path.{cl}",
    ]
    ending = [
        blank_line,
        f"{y}Your current entry is {current_entry}.{y} enter one of the microservice names below to complete the queue.",
        blank_line,
        f"{p}Microservice names{cl}",
        f"{g}{micro_list}{cl}",
        blank_line,
    ]
    services = create_project_display(micros)
    q_lines = create_queue_display(q, q_list)
    [lines.append(service) for service in services]
    [lines.append(entry) for entry in q_lines]
    [lines.append(line) for line in ending]
    swapping_box("large", blr, br, *lines)


def producer_equals_consumer_error(current_entry, micro_list, q, q_list, micros):
    lines = [
        blank_line,
        f"{r}{bl}Error!!!{cl}",
        blank_line,
        f"{y}Producer cannot be it's own consumer{cl}",
    ]
    ending = [
        blank_line,
        f"{y}Your current entry is {current_entry}{cl}",
        blank_line,
        f"{p}Microservice names{cl}",
        f"{g}{micro_list}{cl}",
        blank_line,
    ]
    services = create_project_display(micros)
    q_lines = create_queue_display(q, q_list)
    [lines.append(service) for service in services]
    [lines.append(entry) for entry in q_lines]
    [lines.append(line) for line in ending]
    swapping_box("small", blr, br, *lines)


def format_error(consumer, prod, micros, q, q_list):
    lines = [
        blank_line,
        f"{r}{bl}Error!!!{cl}",
        blank_line,
        f"{y}Format Error"
    ]
    ending = [
        blank_line,
        f"{y}Your entry should be in the following format {cl}",
        blank_line,
        f"{g}{sp5}microservice{p} @{cy} app{cl}",
        blank_line,
        f"Your current entry is {g}{consumer}{p} : {cy}{prod}",
        blank_line
    ]
    services = create_project_display(micros)
    q_lines = create_queue_display(q, q_list)
    [lines.append(service) for service in services]
    [lines.append(entry) for entry in q_lines]
    [lines.append(line) for line in ending]
    swapping_box("large", blr, br, *lines)


def app_does_not_exist_error(app, service, apps, q, q_list, micros):
    current_entry = f"{g}{service}{p}@{cy}{app}"
    lines = [
        blank_line,
        f"{r}{bl}Error!!!{cl}",
        blank_line,
        f"{cy}{app}{y} is not and available app in {g}{service}{cl}",
        f"{y}Choose an app that will send data.{cl}",
        f"{y}Which app in {cy}{service}{y} will be the producer?",
    ]
    ending = [
        blank_line,
        f"{y}Your current entry is {current_entry}{cl}",
        blank_line,
        f"{p}App names{cl}",
        f"{cy}{apps}{cl}",
        blank_line,
    ]
    services = create_project_display(micros)
    q_lines = create_queue_display(q, q_list)
    [lines.append(service) for service in services]
    [lines.append(entry) for entry in q_lines]
    [lines.append(line) for line in ending]
    swapping_box("large", blr, br, *lines)

