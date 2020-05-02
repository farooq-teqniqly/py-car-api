import importlib
from os import getenv
from typing import Generator

from dotenv import load_dotenv

import datawrangler.db as db
import datawrangler.entities
import datawrangler.entityfactory as ef

if __name__ == "__main__":
    load_dotenv()

    connection_info = (
        getenv("SERVER"),
        getenv("DB"),
        getenv("USER"),
        getenv("PASSWORD"),
    )

    importlib.invalidate_caches()
    export_strategy = importlib.import_module(getenv("EXPORT_STRATEGY"))

    connection = db.connect(*connection_info)
    entity_names: Generator[str, None, None] = ef.get_entity_names()

    for entity_name in entity_names:
        class_ = getattr(datawrangler.entities, entity_name)

        entity_rows: Generator[tuple, None, None] = db.get_entities(
            connection, entity_name
        )

        export_strategy.export(class_, entity_rows)
