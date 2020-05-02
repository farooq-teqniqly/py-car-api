from collections import namedtuple

Equipment = namedtuple("Equipment", ["id", "trim_id", "name", "year"])

Generation = namedtuple(
    "Generation", ["id", "model_id", "name", "year_start", "year_end"]
)

Make = namedtuple("Make", ["id", "name"])

MakeModel = namedtuple("MakeModel", ["model_id", "make_id", "name"])

Option = namedtuple("Option", ["id", "name", "parent_id"])

OptionValue = namedtuple("OptionValue", ["id", "option_id", "equipment_id", "is_base"])

Series = namedtuple("Series", ["id", "mode_id", "generation_id", "name"])

Specification = namedtuple("Specification", ["id", "name", "parent_id"])

SpecificationValue = namedtuple(
    "SpecificationValue", ["id", "trim_id", "specification_id", "value", "unit"]
)

Trim = namedtuple(
    "Trim",
    [
        "id",
        "series_id",
        "model_id",
        "name",
        "year_production_start",
        "year_production_end",
    ],
)
