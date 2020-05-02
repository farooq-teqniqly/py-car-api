import json
from typing import Tuple, Generator
from datawrangler.entityfactory import create_entities


def export(class_, rows: Generator[Tuple, None, None]) -> Generator[str, None, None]:

    for entity in create_entities(class_, rows):

        json_str = json.dumps(entity._asdict())
        yield json_str
