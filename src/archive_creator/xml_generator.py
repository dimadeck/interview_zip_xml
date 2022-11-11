from random import randint
from uuid import uuid4

from archive_creator.xml_element import XMLElement


class XMLGenerator:
    """
    Generating xml like:
        <root>
            <var name='id' value='rand_str'/>
            <var name='level' value='rand_int(1,100)'/>
            <objects>
                <object name='rand_str'/>
                <object name='rand_str'/>
            </objects>
        </root>
    """
    OBJECTS_COUNT = 10

    @classmethod
    def generate(cls):
        root = XMLElement('root')
        var_id = XMLElement(element_name='var', params=dict(name='id', value=cls._generate_random_string()))
        var_level = XMLElement(element_name='var', params=dict(name='level', value=cls._generate_random_int()))
        objects = XMLElement('objects')
        for i in range(randint(1, cls.OBJECTS_COUNT)):
            objects.add_child(XMLElement(element_name='object', params=dict(name=cls._generate_random_string())))
        root.add_child(var_id).add_child(var_level).add_child(objects)
        return root.document

    @staticmethod
    def _generate_random_string(string_length=8):
        return uuid4().hex[0:string_length]

    @staticmethod
    def _generate_random_int(min_range=0, max_range=100):
        return randint(min_range, max_range)
