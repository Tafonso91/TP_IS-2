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
            
    
    def lista_clubes(self):
        database = Database()
        list_clubes = []

        dados = database.selectTudo("SELECT unnest(xpath('//Teams/Club/@Name', xml)) as result FROM imported_documents")
        database.disconnect()

        for club in dados:
            if not club in list_clubes:
                list_clubes.append(club)

        return list_clubes
    
    def lista_todos_jogadores(self):
        database = Database()
        list_jogadores = []

        dados = database.selectTudo("SELECT unnest(xpath('//Player/Information/@Name', xml)) as result FROM imported_documents")
        database.disconnect()

        for jogador in dados:
            if not jogador in list_jogadores:
                list_jogadores.append(jogador)

        return list_jogadores

    

    def lista_paises(self):
        database = Database()
        list_paises = []

        dados = database.selectTudo("SELECT unnest(xpath('//Countries/Country/@Name', xml)) as result FROM imported_documents")
        database.disconnect()

        for pais in dados:
            if not pais in list_paises:
                list_paises.append(pais)

        return list_paises

    def lista_pe(self):
        database = Database()
        list_pe = []

        dados = database.selectTudo("SELECT unnest(xpath('//Strong_Foot/Foot/@Name', xml)) as result FROM imported_documents")
        database.disconnect()

        for pes in dados:
            if not pes in list_pe:
                list_pe.append(pes)

        return list_pe
    
    def lista_top_jogadores(self):
        database = Database()
        list_jogadores = []

        dados = database.selectTudo("SELECT (xpath('//Player/Main_Stats/@Over', xml))::text::integer[] as result, (xpath('//Player/Information/@Name', xml))::text[] as name FROM imported_documents")
        database.disconnect()

        for result, name in dados:
            for jogador_over, jogador_name in zip(result, name):
                list_jogadores.append((jogador_over, jogador_name))

        
        list_jogadores.sort(reverse=True)
        list_jogadores = list_jogadores[:10]

        return list_jogadores
    
    def lista_promessas_portugal(self):
        database = Database()
        list_promessas = []

        
        dados = database.selectTudo("""
            SELECT 
                (xpath('//Player[Main_Stats/@Potential > 84 and @countryRef=10]/Information/@Name', xml))::text[] as nome, 
                (xpath('//Player[Main_Stats/@Potential > 84 and @countryRef=10]/Main_Stats/@Potential', xml))::text::integer[] as potencial, 
                (xpath('//Player[Main_Stats/@Potential > 84 and @countryRef=10]/Main_Stats/@Over', xml))::text::integer[] as overall,
                (xpath('//Player[Main_Stats/@Potential > 84 and @countryRef=10]/Information/@Height', xml))::text::integer[] as height,
                (xpath('//Player[Main_Stats/@Potential > 84 and @countryRef=10]/Information/@Price', xml))::text[] as price,
                (xpath('//Player[Main_Stats/@Potential > 84 and @countryRef=10]/Information/@Salary', xml))::text[] as salary
            FROM imported_documents
        """)
        database.disconnect()

        for nome, potencial, overall, height, price, salary in dados:
            for jogador_nome, jogador_potencial, jogador_overall, jogador_height, jogador_price, jogador_salary in zip(nome, potencial, overall, height, price, salary):
                list_promessas.append({
                    "potencial": jogador_potencial,
                    "nome": jogador_nome,
                    "overall": jogador_overall,
                    "height": jogador_height,
                    "price": jogador_price,
                    "salary": jogador_salary
                })

        list_promessas.sort(key=lambda x: x["overall"], reverse=True)

        return list_promessas


    
    def fetch_players_by_country(self, pais):
        database = Database()
        dados_jogadores = []

        query = f""" WITH jogadores AS (
                SELECT  unnest(xpath('//Players/Player/Information/@Name', xml))::text as nome_jogador, 
                    unnest(xpath('//Players/Player/@countryRef', xml))::text as countryRef 
                    FROM imported_documents)

                SELECT nome_jogador FROM jogadores WHERE countryRef IN ( SELECT id_pais
                    FROM ( SELECT unnest(xpath('//Countries/Country/@Id', xml))::text as id_pais, unnest(xpath('//Countries/Country/@Name', xml))::text as nome_pais
                    FROM imported_documents) countries WHERE nome_pais = '{pais}' ); """

        dados = database.selectTudo(query)
        database.disconnect()

        for jogador in dados:
            if jogador not in dados_jogadores:
                dados_jogadores.append(jogador)

        return dados_jogadores

    def fetch_players_by_club(self, club_name):
        database = Database()
        players = []

        query = f"""
            SELECT unnest(xpath('//Club[@Name="{club_name}"]/Players/Player/Information/@Name', xml))::text as player_name
            FROM imported_documents
            WHERE xpath_exists('//Club[@Name="{club_name}"]', xml);
        """

        player_data = database.selectTudo(query)
        database.disconnect()

        for player in player_data:
            if player not in players:
                players.append(player)

        return players

    def fetch_stats_by_player(self, player_name):
        database = Database()
        player_stats = []

        query = f"""
            SELECT 
                unnest(xpath('//Player[Information/@Name="{player_name}"]/Main_Stats/@Over', xml))::text as overall,
                unnest(xpath('//Player[Information/@Name="{player_name}"]/Main_Stats/@Potential', xml))::text as potential,
                unnest(xpath('//Player[Information/@Name="{player_name}"]/Main_Stats/@Offense', xml))::text as offense,
                unnest(xpath('//Player[Information/@Name="{player_name}"]/Main_Stats/@Defense', xml))::text as defense,
                unnest(xpath('//Player[Information/@Name="{player_name}"]/Atack_Stats/@Finishing', xml))::text as finishing,
                unnest(xpath('//Player[Information/@Name="{player_name}"]/Skill_Stats/@Dribble', xml))::text as dribble,
                unnest(xpath('//Player[Information/@Name="{player_name}"]/Movement_Stats/@Sprint', xml))::text as sprint,
                unnest(xpath('//Player[Information/@Name="{player_name}"]/Defense_Stats/@Interception', xml))::text as interception,
                unnest(xpath('//Player[Information/@Name="{player_name}"]/Mental_Stats/@Penalty', xml))::text as penalty
            FROM imported_documents
            WHERE xpath_exists('//Player[Information/@Name="{player_name}"]/Main_Stats', xml);
        """

        stats_data = database.selectTudo(query)
        database.disconnect()

        for stats in stats_data:
            overall, potential, offense, defense, finishing, dribble, sprint, interception, penalty = stats
            player_stats.append({
                "overall": overall,
                "potential": potential,
                "offense": offense,
                "defense": defense,
                "finishing": finishing,
                "dribble": dribble,
                "sprint": sprint,
                "interception": interception,
                "penalty": penalty
            })

        return player_stats


       
        
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
   

   





    
   