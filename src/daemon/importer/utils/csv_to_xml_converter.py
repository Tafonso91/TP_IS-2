import csv
import xml.dom.minidom as md
import xml.etree.ElementTree as ET


from utils.csv_reader import CSVReader
from entities.country import Country
from entities.team import Team
from entities.player import Player
from entities.foot import Foot






class CSVtoXMLConverter:

    def __init__(self, path):
        self._reader = CSVReader(path)

    def to_xml(self):

        # read countries
        countries = self._reader.read_entities(
            attr="Country",
            builder=lambda row: Country(row["Country"])
        )
          # read foots
        feet = self._reader.read_entities(
            attr="Strong Foot",
            builder=lambda row: Foot(row["Strong Foot"])
        )

        # read teams
        teams = self._reader.read_entities(
            attr="Club",
            builder=lambda row: Team(row["Club"])
        )

        # read players

        def after_creating_player(player, row):
            # add the player to the appropriate team
            teams[row["Club"]].add_player(player)

        self._reader.read_entities(
            attr="Name",
            builder=lambda row: Player(
                id=row["Id"],
                name=row["Name"],
                height=row["Height"],
                price=row["Price"],
                salary=row["Salary"],
                overall=row["Overall"],
                potential=row["Potential"],
                country_id=countries[row["Country"]].get_id(),
                foot_id=feet[row["Strong Foot"]].get_id(),
                ofensive_performance=row["Offensive performance"],
                defensive_performance=row["Deffensive performance"],
                crossing=row["Crossing"],
                finishing=row["Finishing"],
                heading_accuracy=row["Heading accuracy"],
                short_passing=row["Short passing"],
                volleys=row["Volleys"],
                dribbling=row["Dribbling"],
                curve=row["Curve"],
                fk_accuracy=row["FK Accuracy"],
                long_pass=row["Long passing"],
                ball_control=row["Ball control"],
                acceleration=row["Acceleration"],
                sprint=row["Sprint"],
                agility=row["Agility"],
                reactions=row["Reactions"],
                balance=row["Balance"],
                shot_power=row["Shot power"],
                jump=row["Jumping"],
                stamina=row["Stamina"],
                strength=row["Strength"],
                long_shot=row["Long shots"],
                agression=row["Aggression"],
                interception=row["Interceptions"],
                positioning=row["Positioning"],
                vision=row["Vision"],
                penalty=row["Penalty"],
                composure=row["Composure"],
                defense_awareness=row["Defensive awareness"],
                stand_tackle=row["Standing tackle"],
                slide_tackle=row["Sliding tackle"],
                diving=row["GK Diving"],
                handling=row["GK Handling"],
                kicking=row["GK Kicking"],
                gk_positioning=row["GK Positioning"],
                reflexes=row["GK Reflexes"],









                
                
            ),
            after_create=after_creating_player
        )

       
        root_el = ET.Element("Football")

        teams_el = ET.Element("Teams")
        for team in teams.values():
            teams_el.append(team.to_xml())

        countries_el = ET.Element("Countries")
        for country in countries.values():
            countries_el.append(country.to_xml())

        foot_el = ET.Element("Strong_Foot")
        for foot in feet.values():
            foot_el.append(foot.to_xml())

        root_el.append(teams_el)
        root_el.append(countries_el)
        root_el.append(foot_el)

        return root_el

    def to_xml_str(self):
        xml_str = ET.tostring(self.to_xml(), encoding='utf8', method='xml').decode()
        dom = md.parseString(xml_str)
        return dom.toprettyxml()
    
    
    
    

    

