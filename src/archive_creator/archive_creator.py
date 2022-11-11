import os.path
from pathlib import Path
from typing import Optional, Union
from zipfile import ZipFile

from archive_creator.xml_generator import XMLGenerator
from config import DEFAULT_ZIP_DIR, DEFAULT_ZIP_COUNT, DEFAULT_XML_PER_ZIP_COUNT


class ArchiveCreator:
    OUTPUT_DIR = DEFAULT_ZIP_DIR
    ZIP_COUNT = DEFAULT_ZIP_COUNT
    XML_PER_ZIP_COUNT = DEFAULT_XML_PER_ZIP_COUNT

    """
    Создает 50 zip-архивов, в каждом 100 xml файлов со случайными данными следующей структуры:
        <root><var name=’id’ value=’<случайное уникальное строковое значение>’/><var name=’level’ value=’<случайное число от 1 до 100>’/><objects><object name=’<случайное строковое значение>’/><object name=’<случайное строковое значение>’/>…</objects></root>
    В тэге objects случайное число (от 1 до 10) вложенных тэгов object.
    """

    def __init__(self, output_dir: Optional[Union[str, Path]] = None, zip_count: Optional[int] = None,
                 xml_per_zip_count: Optional[int] = None):
        self._output_dir = output_dir or self.OUTPUT_DIR
        self._zip_count = zip_count or self.ZIP_COUNT
        self._xml_per_zip_count = xml_per_zip_count or self.XML_PER_ZIP_COUNT

    def execute(self):
        for zip_num in range(self._zip_count):
            zip_filename = self._generate_zip_filename(zip_num + 1)
            os.makedirs(os.path.dirname(zip_filename), exist_ok=True)
            with ZipFile(zip_filename, 'w') as zip_file:
                for xml_num in range(self._xml_per_zip_count):
                    xml = XMLGenerator().generate()
                    zip_file.writestr(self._generate_xml_filename(xml_num + 1), xml)

    def _generate_zip_filename(self, zip_num: int) -> str:
        return os.path.join(self._output_dir, f'zip_file_{zip_num}.zip')

    @staticmethod
    def _generate_xml_filename(xml_num: int) -> str:
        return f'xml_file_{xml_num}.xml'
