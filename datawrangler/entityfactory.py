from typing import Generator, Tuple
import datawrangler.entities


def get_entity_names() -> Generator[str, None, None]:
    generator = (
        e
        for e in dir(datawrangler.entities)
        if (not e.startswith("__") and e != "namedtuple")
    )

    return generator


def create_entities(
    class_, rows: Generator[Tuple, None, None]
) -> Generator[Tuple, None, None]:
    for row in rows:
        field_count = len(class_._fields)
        instance = class_(*row[:field_count])
        yield instance
