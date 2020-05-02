import json
from typing import Tuple, Generator


def export(class_, rows: Generator[Tuple, None, None]) -> Generator[str, None, None]:

    for row in rows:

        field_count = len(class_._fields)
        instance = class_(*row[:field_count])
        json_str = json.dumps(instance._asdict())
        yield json_str
