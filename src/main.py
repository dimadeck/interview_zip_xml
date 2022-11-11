from archive_creator.archive_creator import ArchiveCreator
from processor.archive_reader import ArchiveReader


def launch():
    creator = ArchiveCreator()
    creator.execute()
    reader = ArchiveReader()
    reader.execute()


if __name__ == '__main__':
    launch()
