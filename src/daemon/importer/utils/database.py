import psycopg2

class Database:
    def __init__(self, host="db-xml"):
        self.connection = None
        self.cursor = None
        self.user = "is"
        self.password = "is"
        self.host = host
        self.port = "5432"
        self.database = "is"

    def connect(self):
        if self.connection is None:
            try:
                self.connection = psycopg2.connect(
                    user=self.user,
                    password=self.password,
                    host=self.host,
                    port=self.port,
                    database=self.database
                )
                self.cursor = self.connection.cursor()
                print("\nConexão estabalecida com sucesso.")
            except psycopg2.Error as error:
                print(f"\nError: {error}")

    def disconnect(self):
        if self.connection:
            try:
                self.cursor.close()
                self.connection.close()
                print("\nDisconectado com sucesso.")
            except psycopg2.Error as e:
                print(f"\nErro: {e}")

    def insert(self, sql_query, data):
        self.connect()
        try:
            self.cursor.execute(sql_query, data)
            self.connection.commit()
            print("\nA query foi bem executada.")
        except psycopg2.Error as error:
            print(f"\nError: {error}")

    def selectTudo(self, query, data=None):
        self.connect()
        with self.cursor as cursor:
            if data is None:
                cursor.execute(query)
            else:
                cursor.execute(query, data)
            result = [row for row in cursor.fetchall()]
        return result

    def selectUm(self, query, data):
        self.connect()
        with self.cursor as cursor:
            cursor.execute(query, data)
            result = cursor.fetchone()
        return result
    
    def soft_delete(self, file_name):
        self.connect()
        try:
            query = "UPDATE imported_documents SET delete = now() WHERE file_name = %s"
            self.cursor.execute(query, (file_name,))
            self.connection.commit()
            print("\nThe record was successfully soft deleted.")
        except psycopg2.Error as error:
            print(f"\nError: {error}")
        self.disconnect()