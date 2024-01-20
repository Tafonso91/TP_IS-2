import psycopg2
import pika


# Configurações do PostgreSQL
db_params = {
    'dbname': 'is',
    'user': 'is',
    'password': 'is',
    'host': 'db-xml',
    'port': '5432',
}

# Configurações do RabbitMQ
rabbitmq_params = {
    'host': 'broker',
    'port': 5672,
    'virtual_host': 'is',
    'credentials': pika.PlainCredentials('is', 'is'),
}

QUEUE_NAME = 'queue'

def processar_mensagem(nome_arquivo):
    # TODO: Lógica para processar a mensagem do GIS
    print(f"Processando mensagem para o arquivo: {nome_arquivo}")

    # Exemplo: Inserir dados na base de dados PostgreSQL
    try:
        connection = psycopg2.connect(**db_params)
        cursor = connection.cursor()

        # TODO: Adicione a lógica para manipular os dados no PostgreSQL

        connection.commit()
    except psycopg2.Error as e:
        print(f"Erro ao conectar ao PostgreSQL: {e}")
    finally:
        cursor.close()
        connection.close()

def callback(ch, method, properties, body):
    # Mensagem recebida da fila
    nome_arquivo = body.decode('utf-8')
    print(f"Recebendo mensagem do GIS para o arquivo: {nome_arquivo}")

    # Processar a mensagem
    processar_mensagem(nome_arquivo)

    # Confirmar a mensagem foi processada com sucesso
    ch.basic_ack(delivery_tag=method.delivery_tag)

def consumir_fila_gis():
    connection_params = pika.ConnectionParameters(
        host=rabbitmq_params['host'],
        port=rabbitmq_params['port'],
        virtual_host=rabbitmq_params['virtual_host'],
        credentials=pika.PlainCredentials(
            'is', 'is' 
        ),
    )

    connection = pika.BlockingConnection(connection_params)
    channel = connection.channel()

    try:
        # Consumir a fila existente
        channel.basic_consume(queue=QUEUE_NAME, on_message_callback=callback)

        print(f"Aguardando mensagens do GIS. Pressione CTRL+C para sair.")
        channel.start_consuming()
    except KeyboardInterrupt:
        print("Encerrando a consumação da fila.")
        connection.close()

if __name__ == '__main__':
    consumir_fila_gis()
