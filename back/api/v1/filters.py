import json
from json.decoder import JSONDecodeError
from jsonschema import validate
from jsonschema.exceptions import ValidationError
from collections import namedtuple
from sqlalchemy.orm.relationships import RelationshipProperty
from sqlalchemy.orm.properties import ColumnProperty
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import inspect


filter_schema = {
    "$schema": "http://json-schema.org/draft-07/schema",
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "field": {
            "type": "string"
        },
        "operation": {
            "type": "string",
            "enum": [
                "eq",
            ]
        },
        "value" : {
            "type": "string",
        },            
    },
    "required": [
        "field",
        "operation",
    ],
}


Filter = namedtuple('Filter', 'operation field value')


def filter_type(filter: [dict,str]):
    """ Checks for a valid filter structure
    """
    try:
        if isinstance(filter, str):
            filter = json.loads(filter)        
        validate(instance=filter, schema=filter_schema)
        return filter
    except ValidationError as e:
        raise ValueError(e.message)
    except JSONDecodeError:
        raise ValueError('Argument can not be decoded')


def extract_filters(filters, table):
    """ Loop thru the filters list and inspect the model structure to return the set of values to join and filter.
    """
    new_filters = set()
    joins = set()

    for filter in filters:
        try:
            fields = filter["field"].split('.')
            while fields:
                current_field = fields.pop(0)

                if isinstance(getattr(table, current_field).property, RelationshipProperty):
                    # The field is a relation and should be included in the joins list
                    joins.add(current_field)

                elif isinstance(getattr(table, current_field).property, ColumnProperty):
                
                    if isinstance(getattr(table, current_field).property.columns[0].type, JSONB):
                        # The filter applies to a JSON attribute
                        # TODO: Code this
                        raise ValueError("Not implemented")
                    
                    if not fields: # This is the last element of the array where the condition should be applied.
                        new_filters.add(Filter(filter['operation'], current_field, filter["value"]))
                    else:
                        raise ValueError(f"Additional nested fields: {'.'.join(fields)}")
                    
        except AttributeError:
            raise ValueError(f"Field {filter['field']} not found in table")

    return joins, new_filters


def single_table_query_filter(query, filters): 
    """ Helper function that applies a filter based on the definition of the filter

    This is a generic filter implementation. Is... how to say it: maybe too flexible, maybe too ad hoc, time will tell.
    
    Restrictions: 
        This implementation only goes one relation level deep. Meaning it could only join to a direct ORM relation.
        The select part of the query should consist of only one table.

    Filter fields examples:
        relates_to.eid = relates_to -> join / eid -> filter 
        properties.names = properties -> json / names -> json prop
    """
    if filters:
        
        # Get the table the query is trying to retrieve. Should be only one.
        inspector = inspect(query)
        if not inspector.is_single_entity:
            raise ValueError('Query should be agains one single entity')
        table = inspector.column_descriptions[0]['entity']

        try:            
            joins, new_filters = extract_filters(filters, table)

            for join_field in joins:
                query = query.join(getattr(table, join_field))
            
            for filter in new_filters:
                    
                if filter.operation == "eq":
                    query = query.filter(getattr(table, filter.field) == filter.value)        
                else:
                    raise ValueError(f"Operation {filter.operation} not supported")

        except Exception as e:
            raise ValueError(f"Filter definition is invalid: {str(e)}")

    return query
