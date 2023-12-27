import xml.etree.ElementTree as ET





class Foot:

    def __init__(self, name):
        Foot.counter += 1
        self._id_foot = Foot.counter
        self._name = name

    def to_xml(self):
        el = ET.Element("Foot")
        el.set("Id", str(self._id_foot))
        el.set("Name", self._name)
        return el

    def get_id(self):
        return self._id_foot

    def __str__(self):
        return f"Name: {self._name}, Id:{self._id_foot}"


Foot.counter = 0

