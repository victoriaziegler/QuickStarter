import pika
import json

def send_data(data, encoder, exchange, type):
    parameters = pika.ConnectionParameters(host="rabbitmq")
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.exchange_declare(exchange=exchange, exchange_type=type)

    message = json.dumps(data, cls=encoder)
    channel.basic_publish(
        exchange=exchange,
        routing_key="",
        body=message,
    )
    connection.close()