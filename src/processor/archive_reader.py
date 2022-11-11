import os
import zipfile
from pathlib import Path
from typing import Optional, Union

from config import DEFAULT_ZIP_DIR, DEFAULT_CSV_DIR, DEFAULT_ID_LEVEL_CSV_FILENAME, DEFAULT_ID_OBJECT_CSV_FILENAME
from processor.csv_creator import IDLevelGenerator, IDObjectGenerator


class ArchiveReader:
    INPUT_DIR = DEFAULT_ZIP_DIR
    OUTPUT_DIR = DEFAULT_CSV_DIR
    ID_LEVEL_FILENAME = os.path.join(DEFAULT_CSV_DIR, DEFAULT_ID_LEVEL_CSV_FILENAME)
    ID_OBJECT_FILENAME = os.path.join(DEFAULT_CSV_DIR, DEFAULT_ID_OBJECT_CSV_FILENAME)
    """
    Обрабатывает директорию с полученными zip архивами, разбирает вложенные xml файлы и формирует 2 csv файла:
        Первый: id, level - по одной строке на каждый xml файл
        Второй: id, object_name - по отдельной строке для каждого тэга object (получится от 1 до 10 строк на каждый xml файл)
    """

    def __init__(self, input_dir: Optional[Union[str, Path]] = None,
                 id_level_filename: Optional[Union[str, Path]] = None,
                 id_object_filename: Optional[Union[str, Path]] = None):
        self._input_dir = input_dir or self.INPUT_DIR
        self._id_level_generator = IDLevelGenerator(id_level_filename or self.ID_LEVEL_FILENAME)
        self._id_object_generator = IDObjectGenerator(id_object_filename or self.ID_OBJECT_FILENAME)

    def execute(self):
        for filename in os.listdir(self._input_dir):
            zip_filename = os.path.join(self._input_dir, filename)
            if not self._check_zip(zip_filename):
                continue
            self._handle_zip(zip_filename)
        self._id_level_generator.save()
        self._id_object_generator.save()

    @staticmethod
    def _check_zip(zip_filename: str) -> bool:
        return zipfile.is_zipfile(zip_filename)

    def _handle_zip(self, zip_filename: str):
        with zipfile.ZipFile(zip_filename) as zip_file:
            for file in zip_file.filelist:
                with zip_file.open(file.filename) as xml_file:
                    xml_content = xml_file.read().decode('utf-8')
                    self._handle_xml(xml_content)

    def _handle_xml(self, xml_content: str):
        self._id_level_generator.handle_part(xml_content)
        self._id_object_generator.handle_part(xml_content)
