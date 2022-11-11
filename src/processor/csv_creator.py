import csv
import os
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Union


class CSVGenerator:
    FIELDS = []

    def __init__(self, output_filename: Union[str, Path]):
        self._filename = output_filename
        self._rows = []

    def handle_part(self, xml_content: str):
        xml_part = ET.fromstring(xml_content)
        self._parse(xml_part)

    def _parse(self, xml_part):
        raise NotImplementedError

    def save(self):
        os.makedirs(os.path.dirname(self._filename), exist_ok=True)
        with open(self._filename, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.FIELDS)
            writer.writeheader()
            for row in self._rows:
                writer.writerow(row)


class IDLevelGenerator(CSVGenerator):
    FIELDS = ['id', 'level']

    def _parse(self, xml_part):
        row = {}
        for element in xml_part:
            if element.tag == 'var':
                attrs = element.attrib
                row[attrs['name']] = attrs['value']
        self._rows.append(row)


class IDObjectGenerator(CSVGenerator):
    FIELDS = ['id', 'object']

    def _parse(self, xml_part):
        current_id = None
        for element in xml_part:
            attrs = element.attrib
            if element.tag == 'var' or attrs.get('name') == 'id':
                current_id = attrs['value']
                break
        for current_object in xml_part.findall('objects/object'):
            object_name = current_object.attrib['name']
            self._rows.append({'id': current_id, 'object': object_name})
