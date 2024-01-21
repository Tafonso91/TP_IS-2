import psycopg2
import pika
import xml.etree.ElementTree as ET
import requests

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
NOMINATIM_API_URL = 'https://nominatim.openstreetmap.org/search'

def obter_coordenadas_pais(nome_pais):
    # Consultar a API Nominatim para obter coordenadas do país
    params = {
        'q': nome_pais,
        'format': 'json',
    }

    try:
        response = requests.get(NOMINATIM_API_URL, params=params)
        response.raise_for_status() 

        result = response.json()

        if result:
            coordenadas = result[0]
            latitude = coordenadas['lat']
            longitude = coordenadas['lon']
            return latitude, longitude
        else:
            print(f"Coordenadas não encontradas para o país: {nome_pais}")
            return None

    except requests.RequestException as e:
        print(f"Erro ao consultar a API Nominatim: {e}")
        return None


def processar_mensagem(nome_arquivo):
    print(f"Processando mensagem para o arquivo: {nome_arquivo}")

    try:
        connection = psycopg2.connect(**db_params)
        print("Conexão ao PostgreSQL estabelecida com sucesso!")

        cursor = connection.cursor()
        xml_query = "SELECT xml FROM public.imported_documents WHERE file_name = %s"
        cursor.execute(xml_query, (nome_arquivo,))
        xml_data = cursor.fetchone()

        if xml_data:
            xml_data = xml_data[0]

            # Processar o XML
            root = ET.fromstring(xml_data)

            # Extrair nomes dos países
            countries = root.findall('.//Country')
            for country in countries:
                country_name = country.get('Name')
                print(f" Country Name: {country_name}")

                
                latitude, longitude = obter_coordenadas_pais(country_name)
                if latitude is not None and longitude is not None:
                    print(f" Coordenadas: Latitude {latitude}, Longitude {longitude}")
                    
                    
                    
                else:
                    print(f"Coordenadas não encontradas para o país: {country_name}")
                sendToApiGis(country_name, latitude, longitude)


        else:
            print(f"Arquivo {nome_arquivo} não encontrado na base de dados.")

    except psycopg2.Error as e:
        print(f"Erro ao conectar ou consultar o PostgreSQL: {e}")
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

def sendToApiGis(country_name, latitude, longitude):
    try:
        api_gis_url = 'http://api-gis:8080/update_country_coords'

        data = {
            'country_name': country_name,
            'latitude': latitude,
            'longitude': longitude
        }

        response = requests.patch(api_gis_url, json=data)

        if response.status_code == 200:
            print(f"Coordenadas atualizadas com sucesso para o país: {country_name}")
        else:
            print(f"Falha ao atualizar coordenadas para o país: {country_name}. Resposta da API GIS: {response.text}")

    except requests.RequestException as e:
        print(f"Erro ao enviar dados para a API GIS: {e}")

if __name__ == '__main__':
    consumir_fila_gis()
