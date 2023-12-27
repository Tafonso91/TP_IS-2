import xml.etree.ElementTree as ET
from entities.country import Country

class Player:
    def __init__(self, id, name, height, price, salary,overall, potential, country_id, foot_id, ofensive_performance, defensive_performance, crossing, finishing, heading_accuracy, short_passing, volleys, dribbling, curve, fk_accuracy, long_pass, ball_control, acceleration, sprint, agility, reactions, balance, shot_power, jump, stamina, strength, long_shot, agression, interception, positioning, vision, penalty, composure, defense_awareness,stand_tackle, slide_tackle, diving,handling,kicking, gk_positioning, reflexes):
        self._id = id
        self._name = name
        self._height = height
        self._price = price
        self._salary = salary
        self._overall= overall
        self._potential= potential
        self._country_id = country_id
        self._foot_id = foot_id
        self._ofensive_performance = ofensive_performance
        self._defensive_performance = defensive_performance
        self._crossing = crossing
        self._finishing = finishing
        self._heading_accuracy = heading_accuracy
        self._short_passing = short_passing
        self._volleys= volleys
        self._dribbling = dribbling
        self._curve = curve
        self._fk_accuracy = fk_accuracy
        self._long_pass = long_pass
        self._ball_control = ball_control
        self._acceleration = acceleration
        self._sprint = sprint
        self._agility = agility
        self._reactions = reactions
        self._balance = balance
        self._shot_power = shot_power
        self._jump = jump
        self._stamina = stamina
        self._strength = strength
        self._long_shot = long_shot
        self._agression = agression
        self._interception = interception
        self._positioning = positioning
        self._vision = vision
        self._penalty = penalty
        self._composure = composure
        self._defense_awareness = defense_awareness
        self._stand_tackle= stand_tackle
        self._slide_tackle= slide_tackle
        self._diving = diving
        self._handling = handling
        self._kicking = kicking
        self._gk_positioning = gk_positioning
        self._reflexes= reflexes

    def to_xml(self):
        player_el = ET.Element("Player")
        player_el.set("Id", str(self._id))
        player_el.set("countryRef", str(self._country_id))

        info_el = ET.Element("Information")
        info_el.set("Name", self._name)
        info_el.set("Height", str(self._height))
        info_el.set("Price", self._price)
        info_el.set("Salary", self._salary)
        info_el.set("FootRef", str(self._foot_id))
        player_el.append(info_el)

        stats_el = ET.Element("Main_Stats")
        stats_el.set("Over", self._overall)
        stats_el.set("Potential", self._potential)
        stats_el.set("Offense", self._ofensive_performance.capitalize())
        stats_el.set("Defense", self._defensive_performance.capitalize())
        player_el.append(stats_el)

        atack_el = ET.Element("Atack_Stats")
        atack_el.set("Crossing", self._crossing)
        atack_el.set("Finishing", self._finishing)
        atack_el.set("Heading", self._heading_accuracy)
        atack_el.set("Short_Pass", self._short_passing)
        atack_el.set("Volleys", self._volleys)
        player_el.append(atack_el)

        skill_el = ET.Element("Skill_Stats")
        skill_el.set("Dribble", self._dribbling)
        skill_el.set("Curve", self._curve)
        skill_el.set("FK", self._fk_accuracy)
        skill_el.set("Long_Pass", self._long_pass)
        skill_el.set("Ball_control", self._ball_control)
        player_el.append(skill_el)

        movement_el = ET.Element("Movement_Stats")
        movement_el.set("Acceleration", self._acceleration)
        movement_el.set("Sprint", self._sprint)
        movement_el.set("Agility", self._agility)
        movement_el.set("Reactions", self._short_passing)
        movement_el.set("Balance", self._balance)
        player_el.append(movement_el)

        power_el = ET.Element("Power_Stats")
        power_el.set("Shot_power", self._shot_power)
        power_el.set("Jump", self._jump)
        power_el.set("Stamina", self._stamina)
        power_el.set("Strenght", self._strength)
        power_el.set("Long_shot", self._long_shot)
        player_el.append(power_el)

        mental_el = ET.Element("Mental_Stats")
        mental_el.set("Agression", self._agression)
        mental_el.set("Positioning", self._positioning)
        mental_el.set("Vision", self._vision)
        mental_el.set("Penalty", self._long_shot)
        mental_el.set("Composure", self._composure)
        player_el.append(mental_el)

        defense_el = ET.Element("Defense_Stats")
        defense_el.set("Interception", self._interception)
        defense_el.set("Def.Awareness", self._defense_awareness)
        defense_el.set("Stand_Tackle", self._stand_tackle)
        defense_el.set("Slide_Tackle", self._slide_tackle)
        player_el.append(defense_el)

        gk_el = ET.Element("GK_Stats")
        gk_el.set("Diving", self._diving)
        gk_el.set("Handling", self._defense_awareness)
        gk_el.set("GK_Kick", self._kicking)
        gk_el.set("GK_Positioning", self._gk_positioning)
        gk_el.set("Reflexes", self._reflexes)
        player_el.append(gk_el)

        return player_el

    def __str__(self):
        return f"{self._name} ({self._id})"

Player.counter = 0
