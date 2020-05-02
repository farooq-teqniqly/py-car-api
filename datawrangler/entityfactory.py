from typing import Generator, Tuple


def create_entities(
    class_, rows: Generator[Tuple, None, None]
) -> Generator[Tuple, None, None]:
    for row in rows:
        field_count = len(class_._fields)
        instance = class_(*row[:field_count])
        yield instance
