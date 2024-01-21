import psycopg2

class Database:
    def __init__(self, host="db-rel"):
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
                print("\nConexão estabelecida com sucesso.")
            except psycopg2.Error as error:
                print(f"\nError: {error}")

    def disconnect(self):
        if self.connection:
            try:
                self.cursor.close()
                self.connection.close()
                print("\nDesconectado com sucesso.")
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
    
    def update(self, sql_query, data=None):
        self.connect() 
        try:
           
            if data:
                self.cursor.execute(sql_query, data)
            else:
                self.cursor.execute(sql_query)
            self.connection.commit()
            print("\nA query de atualização foi bem executada.")
        except psycopg2.Error as error:
            print(f"\nError: {error}")
        
    
    def selectJogadoresComCoordenadas(self):
        try:
            self.connect()  
            query = """
                SELECT
                    p.id,
                    p.name,
                    p.country_id,
                    c.geom
                FROM
                    player p
                INNER JOIN
                    country c ON p.country_id = c.id
            """
            return self.selectTudo(query)
        except psycopg2.Error as error:
            print(f"\nError: {error}")
        finally:
            self.disconnect()
        