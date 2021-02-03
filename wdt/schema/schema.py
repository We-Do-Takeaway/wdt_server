from pathlib import PurePath
from ariadne import load_schema_from_path, make_executable_schema

from wdt.menu.schema import menu_schema


parent_dir = PurePath(__file__).parent


# Load all .graphql files
type_defs = load_schema_from_path(parent_dir)

schema = make_executable_schema(
    type_defs,
    *menu_schema,
)
