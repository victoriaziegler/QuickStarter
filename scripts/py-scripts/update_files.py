from helpers import *


def update_settings(micro, config, project, app_list):
    with open(f"{project}/settings.py", "r") as f:
        contents = f.readlines()
    update_section(
        6,
        contents,
        "DATABASES = {\n",
        'DATABASES["default"] = dj_database_url.config()',
        "DATABASES = {} \n"
    )
    insert_at_next(
        contents,
        "MIDDLEWARE = [\n",
        "    'corsheaders.middleware.CorsMiddleware',\n"
    )
    [insert_at_next(
        contents,
        "INSTALLED_APPS = [\n",
        f"    '{app[0]}.apps.{app[1]}',\n",
    ) for app in reversed(app_list)]
    insert_at_next(
        contents,
        "INSTALLED_APPS = [\n",
        f"    'corsheaders',\n"
    )
    replace_line(
        contents,
        "ALLOWED_HOSTS = []\n",
        'DJWTO_ACCESS_TOKEN_LIFETIME = None\n',
        'DJWTO_MODE = "TWO-COOKIES"\n',
        'CORS_ALLOW_CREDENTIALS = True\n',
        'CORS_ALLOWED_ORIGINS = ["http://localhost:3000"]\n',
        'CSRF_TRUSTED_ORIGINS = ["http://localhost:3000"]\n',
        'ALLOWED_HOSTS = ["localhost"]\n'
    )
    insert_at_next(
        contents,
        "from pathlib import Path\n",
        "import dj_database_url\n"
    )
    contents.remove("    'django.middleware.csrf.CsrfViewMiddleware',\n")

    with open(f"{project}/settings.py", "w") as f:
        contents = "".join(contents)
        f.write(contents)


def create_poller_file(micro, project):
    with open("poll/poller.py", "r") as f:
        contents = f.readlines()
    replace_line(
        contents,
        "# Add this line\n",
        f"os.environ.setdefault(\"DJANGO_SETTINGS_MODULE\", \"{project}.settings\")\n",
    )
    replace_line(
        contents,
        "        print('Service poller polling for data')\n",
        f"        print('{micro.title()} poller polling for data')\n",
    )
    with open(f"poll/poller.py", "w") as f:
        contents = "".join(contents)
        f.write(contents)


def create_queue_cons_file(queue_dict, micro, project):
    with open("queue/consumer.py", "r") as f:
        contents = f.readlines()

    queues = queue_dict[micro]
    if len(queues) > 1:
        queue_names = []
        [queue_names.append(f"{micro}_{prod[0]}_{prod[1]}") for prod in queues]
        count = len(queue_names)
        for name in queue_names:
            insert_at_next(
                contents,
                "#insert callback\n",
                "\n",
                "    pass\n",
                f"def callback{count}(ch, method, properties, body):\n"
            )
            insert_at_next(
            contents,
            "#exchange declare\n",
            "        )\n",
            "            exchange_type=\"fanout\",\n",
            f"            exchange=\"{name}\",\n",
            "        channel.exchange_declare(\n"
            )
            insert_at_next(
                contents,
                "#insert queue declare\n",
                f"        channel.queue_declare(queue=\"{name}\")\n"
            )
            insert_at_next(
                contents,
                "#insert queue bind\n",
                f"        channel.queue_bind(exchange=\"{name}\", queue=\"{name}\")\n"
            )
            insert_at_next(
                contents,
                "#insert basic consume\n",
                "        )\n",
                "            auto_ack=True,\n",
                f"            on_message_callback=callback{count},\n",
                f"            queue=\"{name}\",\n",
                "        channel.basic_consume(\n",
            )
            count -= 1
    else:
        exchange = f"{micro}_{queues[0][0]}_{queues[0][1]}"
        insert_at_next(
            contents,
            "#insert callback\n",
            "\n",
            "    pass\n",
            f"def callback(ch, method, properties, body):\n"
        )
        insert_at_next(
            contents,
            "#exchange declare\n",
            f"        channel.queue_bind(exchange=\"{exchange}\", queue=queue_name)\n",
            "\n",
            "        queue_name = result.method.queue\n",
            "        result = channel.queue_declare(queue=\"\", exclusive=True)\n",
            "\n"
            ")\n",
            "            exchange_type=\"fanout\",\n",
            f"            exchange=\"{exchange}\",\n",
            "        channel.exchange_declare(\n"
        )
        insert_at_next(
            contents,
            "#insert basic consume\n",
            "        )\n",
            "            auto_ack=True,\n",
            f"            on_message_callback=callback,\n",
            f"            queue=queue_name,\n",
            "        channel.basic_consume(\n",
        )
    replace_line(
        contents,
        '# update this line\n',
        f"os.environ.setdefault(\"DJANGO_SETTINGS_MODULE\", \"{project}.settings\")\n",
    )
    contents.remove("#insert callback\n")
    contents.remove("#exchange declare\n")
    contents.remove("#insert queue bind\n")
    contents.remove("#insert queue declare\n")
    contents.remove("#insert basic consume\n")
    with open(f"queue/consumer.py", "w") as f:
        contents = "".join(contents)
        f.write(contents)


def update_producer_views_files(queue_dict, micro):
    prods = queue_dict[micro]
    for app in prods:
        consumers = prods[app]
        count = len(consumers)

        with open(f"api/{app}/views.py", "r") as f:
            contents  = f.readlines()
        print(contents)
        insert_at_next(
            contents,
            "from django.shortcuts import render\n",
            "\n",
            "import json\n",
            "import pika\n"
        )
        for consumer in consumers:
            queue = f"{consumer}_{micro}_{app}"
            if count > 1:
                label = str(count)
            else:
                label = ""
            insert_at_next(
                contents,
                "# Create your views here.\n",
                "\n",
                "\n",
                "    connection.close()\n",
                "    )\n",
                "        body=message,\n",
                f"        routing_key=\"{queue}\",\n",
                f"        exchange=\"{queue}\",\n",
                "    channel.basic_publish(\n",
                "\n",
                f"    message = \"\" #Add your data here\n",
                "\n",
                f"    channel.exchange_declare(exchange=\"{queue}\", exchange_type=\"fanout\")\n",
                "    channel = connection.channel()\n",
                "    connection = pika.BlockingConnection(parameters)\n",
                "    parameters = pika.ConnectionParameters(host=\"rabbitmq\")\n",
                f"def send_data{label}():\n"
            )
            count -= 1
        contents.remove("# Create your views here.\n")
        with open(f"api/{app}/views.py", "w") as f:
            contents = "".join(contents)
            f.write(contents)