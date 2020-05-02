import datawrangler.db as db
import datawrangler.entities
import datawrangler.jsonexporter as je
from os.path import dirname, realpath, join

if __name__ == "__main__":
    connection_info = ("127.0.0.1, 1433", "cars", "sa", "!!P@ssw0rd!!")
    connection = db.connect(*connection_info)
    output_dir = dirname(realpath(__file__))

    entities = [
        e
        for e in dir(datawrangler.entities)
        if (not e.startswith("__") and e != "namedtuple")
    ]

    for entity in entities:
        cursor = connection.cursor()
        cursor.execute(f"SELECT * FROM [dbo].[{entity}]")
        class_ = getattr(datawrangler.entities, entity)
        file_name = f"{class_.__name__}.json"
        file_full_name = join(output_dir, file_name)

        print(f"Exporting {class_.__name__} to {file_full_name}...")

        with open(file_full_name, "a") as writer:
            writer.write("[")

            for entity_json in je.export(class_, cursor):
                writer.write(entity_json)
                writer.write(",")

            writer.write("]")
