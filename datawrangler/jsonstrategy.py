import json
from typing import Tuple, Generator
from datawrangler.entityfactory import create_entities
from os import getenv
from os.path import join


def export(class_, rows: Generator[Tuple, None, None]):

    path = join(getenv("JSON_OUTPUT_FOLDER"), f"{class_.__name__}.json")
    print(f"Exporting {class_.__name__} to {path}...")

    with open(path, "a") as writer:
        writer.write("[")

        for entity in create_entities(class_, rows):
            writer.write(_serialize(entity))
            writer.write(",")

        writer.write("]")


def _serialize(entity):
    return json.dumps(entity._asdict())
