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


Filter = namedtuple('Filter', 'operation table field value')
Join = namedtuple('Join', 'table field')


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
    The expected filter metadata structure should match the one specified at filter_schema.    
    """
    new_filters = set()
    joins = set()

    for filter in filters:
        try:
            fields = filter["field"].split('.')
            last_table = table # Latest Joined Table.
            while fields:
                current_field = fields.pop(0)

                if isinstance(getattr(last_table, current_field).property, RelationshipProperty):
                    # The field is a relation and should be included in the joins list.
                    joins.add(Join(last_table, current_field))

                    # Get the table this field belongs to.
                    last_table = getattr(last_table, current_field).property.mapper.class_

                elif isinstance(getattr(last_table, current_field).property, ColumnProperty):
                
                    if isinstance(getattr(last_table, current_field).property.columns[0].type, JSONB):
                        # The filter applies to a JSON attribute
                        # TODO: Code this
                        raise ValueError("Not implemented")
                    
                    if not fields: # This is the last element of the array where the condition should be applied.
                        new_filters.add(
                            Filter(
                                filter['operation'],
                                last_table,
                                current_field,
                                filter["value"]
                        ))
                    else:
                        raise ValueError(f"Additional nested fields: {'.'.join(fields)}")
                    
        except AttributeError:
            raise ValueError(f"Field {filter['field']} not found in table")

    return joins, new_filters


def single_table_query_filter(query, filters): 
    """ Helper function that applies a filter based on the definition of the filter

    This is a generic filter implementation. Is... how to say it: maybe too flexible, maybe too ad hoc, time will tell.
    
    Restrictions: 
        The select part of the query should consist of only one table.

    Filter fields examples:
        Nodes.relates_to.eid = relates_to -> join + eid -> filter 
        Nodes.properties.names = properties -> json + names -> json prop
        Nodes.definition.entity_type.eid -> definition -> join + entity_type -> join + eid -> filter
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
                query = query.join(getattr(join_field.table, join_field.field))
            
            for filter in new_filters:
                    
                if filter.operation == "eq":
                    query = query.filter(getattr(filter.table, filter.field) == filter.value)        
                else:
                    raise ValueError(f"Operation {filter.operation} not supported")

        except Exception as e:
            raise ValueError(f"Filter definition is invalid: {str(e)}")

    return query
