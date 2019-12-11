import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='teste')


def callback(ch, method, properties, body):
    print("Recebido: %r " % (body))

channel.basic_consume(queue='teste', on_message_callback=callback, auto_ack=True)

print('Esperando mensagens...')
channel.start_consuming()