from flask import Flask, request, g, abort
from flask_restful import Resource, reqparse, fields, marshal
from jsonschema.exceptions import ValidationError

from .entity_type import entity_type_format
# from .entity_type_definition import entity_type_definition_format
from .filters import filter_type, single_table_query_filter
from model import tables, metadata


# This is a one level deep nested node. The relation is removed from this node. 
node_format_nested = {
    'eid': fields.String,
    'entity_type': fields.Nested(entity_type_format),
    'properties': fields.Raw,
    'definition_eid': fields.String,
}

relation_format = {
    'eid': fields.String,
    'label': fields.String,
    'properties': fields.Raw,
    'node_to_eid': fields.String,
    'relates_to': fields.Nested(node_format_nested),
}

node_format = {
    'eid': fields.String,
    'entity_type': fields.Nested(entity_type_format),
    # 'definition': fields.Nested(entity_type_definition_format),
    'properties': fields.Raw,
    'relates_to': fields.Nested(relation_format),
    'definition_eid': fields.String,
}

filter_args = reqparse.RequestParser(bundle_errors=True)
filter_args.add_argument('filters', type=filter_type, required=False, action='append', default=None, location='args')


class NodeRelation(Resource):
    def get(self):
        """ List all the entity types definitions matching the provided filter.
        """
        try:
            args = filter_args.parse_args()
            node_list = single_table_query_filter(
                g.db_session.query(tables.Node),
                args['filters']
            )
            node_list = node_list.all()
            return marshal(node_list, node_format), 200
        except ValueError as e:
            abort(400, str(e))
