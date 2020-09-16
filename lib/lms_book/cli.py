from typing import List
from argparse import ArgumentParser
from lms_book import LMSBookCommand, create_part, create_chapter, publish, pull, sync


def main():
    pass


def parse_command(command: LMSBookCommand, argv: List[str]):
    if command == LMSBookCommand.create:
        if argv[0].lower() == "part":
            create_part(*argv[1:])
        elif argv[0].lower() == "chapter":
            create_chapter(*argv[1:])
        else:
            raise ValueError("Create {} not supported. Can only create part or chapter at the moment.".format(argv[0]))
    if command == LMSBookCommand.pull:
        pull(*argv)
    if command == LMSBookCommand.publish:
        publish(*argv)
    if command == LMSBookCommand.sync:
        sync()


def parse_commands(argv=None):
    try:
        command = LMSBookCommand.from_str(argv[1])
    except KeyError:
        if argv in ["-i", "--interactive"]:
            interactive()
            exit(0)
        else:
            raise KeyError(
                "Valid commands are create, pull, publish, and sync. Or you can run it interactively with -i option."
            )
    parse_command(command, argv[2:])
    parser = ArgumentParser()
    parser.add_argument()
    pass

