import xml.etree.ElementTree as ET




class Jogador:

    def __init__(self,id, name: str,height, salary, price):
        
        self._id = id
        self._name = name
        self._height = height
        self._salary = salary
        self._price = price

        

    def to_xml(self):
        el = ET.Element("Player")
        el.set("Id", self._id)
        el.set("Name", self._name)
        el.set("Height", self._height)
        el.set("Salary", self._salary)
        el.set("Price", self._price)
        

        return el

   
    
    def __str__(self):
        return f"id:{self._id} nome:({self._name})"


