import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='teste')

mensagem = raw_input();
channel.basic_publish(exchange='', routing_key='teste', body=mensagem)

print("Mensagem enviada: %r" % (mensagem))

connection.close()
