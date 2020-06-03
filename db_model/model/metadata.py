from jsonschema import validate as json_validate
from jsonschema.exceptions import ValidationError
from. import tables

# If you are lost, read: https://json-schema.org/understanding-json-schema/index.html


properties_schema = {
    "$schema": "http://json-schema.org/draft-07/schema",
    "type": "array",
    "items": {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "name": {
                "type": "string"
            },
            "type": {
                "type": "string",
                "enum": [
                    "boolean",
                    "integer",
                    "float",
                    "string",
                    "date",
                ]
            }
        },
        "required": [
            "name",
            "type",
        ],
    }
}

relations_schema = {
    "$schema": "http://json-schema.org/draft-07/schema",
    "type": "array",
    "items": {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "label": {
                "type": "string"
            },
            "type": {
                "type": "string"
            },
            "properties": properties_schema,
        },
        "required": [
            "label",
            "type",
            "properties",
        ],
    }
}


def validate(object):
    """ Method to validate json fields on entities, data and relations
    """
    try:
        if isinstance(object, tables.EntityTypeDefinition):
            json_validate(instance=object.properties, schema=properties_schema)
            json_validate(instance=object.relations, schema=relations_schema)
            return True
        if isinstance(object, tables.EntityType):
            return True
        else:
            raise ValueError("Unknown model object")
    except ValidationError as e:
        raise ValueError(e.message)
