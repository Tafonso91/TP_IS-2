from utils.database import Database
import psycopg2

class QueryFunctions:
    def __init__(self):
        self.database = Database()

    def _execute_query(self, query, data):
        database = Database()
        try:
            result = database.selectUm(query, data)
            return result
        finally:
            database.disconnect()
    
 
    def fetch_players_by_country(pais):
        database = Database()
        dados_jogadores = []

        query = f""" WITH jogadores AS (
                SELECT  unnest(xpath('//Players/Player/Information/@Name', xml))::text as nome_jogador, 
                    unnest(xpath('//Players/Player/@countryRef', xml))::text as countryRef 
                    FROM imported_documents WHERE deleted_on IS NULL )

                SELECT nome_jogador FROM jogadores WHERE countryRef IN ( SELECT id_pais
                    FROM ( SELECT unnest(xpath('//Countries/Country/@Id', xml))::text as id_pais, unnest(xpath('//Countries/Country/@Name', xml))::text as nome_pais
                    FROM imported_documents WHERE deleted_on IS NULL ) countries WHERE nome_pais = '{pais}' ); """

        dados = database.selectTudo(query)
        database.disconnect()

        for jogador in dados:
            if jogador not in dados_jogadores:
                dados_jogadores.append(jogador)

        return dados_jogadores



    @staticmethod
    def lista_jogadores(nome_equipa):
        database = Database()
        query = """
        SELECT unnest(xpath('//Teams/Club[@Name="{}"]/Players/Player/Information/@Name', xml))::text AS player_name
        FROM imported_documents
        """.format(nome_equipa)


        result = database.selectTudo(query)
        jogadores = [jogador[0] for jogador in result]

        return jogadores


    @staticmethod
    def lista_estatisticas_jogador(nome_jogador, tipo_estatistica):
        database = Database()
        if tipo_estatistica == 'ataque':
            query = """
            SELECT unnest(xpath('//Teams/Club/Players/Player[Information/@Name="{}"]/Atack_Stats', xml))::text AS stats
            FROM imported_documents
            """.format(nome_jogador)
        elif tipo_estatistica == 'informação':
            query = """
            SELECT unnest(xpath('//Teams/Club/Players/Player[Information/@Name="{}"]/Information', xml))::text AS stats
            FROM imported_documents
            """.format(nome_jogador)
        elif tipo_estatistica == 'principal':
            query = """
            SELECT unnest(xpath('//Teams/Club/Players/Player[Information/@Name="{}"]/Main_Stats', xml))::text AS stats
            FROM imported_documents
            """.format(nome_jogador)
        elif tipo_estatistica == 'skill':
            query = """
            SELECT unnest(xpath('//Teams/Club/Players/Player[Information/@Name="{}"]/Skill_Stats', xml))::text AS stats
            FROM imported_documents
            """.format(nome_jogador)
        elif tipo_estatistica == 'movimento':
            query = """
            SELECT unnest(xpath('//Teams/Club/Players/Player[Information/@Name="{}"]/Movement_Stats', xml))::text AS stats
            FROM imported_documents
            """.format(nome_jogador)
        elif tipo_estatistica == 'força':
            query = """
            SELECT unnest(xpath('//Teams/Club/Players/Player[Information/@Name="{}"]/Power_Stats', xml))::text AS stats
            FROM imported_documents
            """.format(nome_jogador)
        elif tipo_estatistica == 'mental':
            query = """
            SELECT unnest(xpath('//Teams/Club/Players/Player[Information/@Name="{}"]/Mental_Stats', xml))::text AS stats
            FROM imported_documents
            """.format(nome_jogador)   
        elif tipo_estatistica == 'defesa':
            query = """
            SELECT unnest(xpath('//Teams/Club/Players/Player[Information/@Name="{}"]/Defense_Stats', xml))::text AS stats
            FROM imported_documents
            """.format(nome_jogador) 
        else:
            return "Tipo de estatística inválido. Escolha uma opção válida."

        result = database.selectTudo(query)
        estatisticas = [estatistica[0] for estatistica in result]

        return estatisticas
   

   





    
   