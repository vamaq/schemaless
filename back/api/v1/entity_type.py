from flask import Flask, request, g, abort
from flask_restful import Resource, reqparse, fields, marshal
from jsonschema.exceptions import ValidationError

from model import tables, metadata

entity_type_format = {
    'eid': fields.String,
    'type': fields.String,
}


entity_type_args = reqparse.RequestParser(bundle_errors=True)
entity_type_args.add_argument('type', type=str, required=True)


class EntityTypeEid(Resource):
    def get(self, eid):
        """ Gets one single entity type
        """
        entity_type = g.db_session.query(tables.EntityType).get(eid)
        if not entity_type:
            abort(404)
        return marshal(entity_type, entity_type_format), 200

    def delete(self, eid):
        """ Deletes a entity type.
        """
        entity_type = g.db_session.query(tables.EntityType).get(eid)
        if not entity_type:
            abort(404)
        g.db_session.delete(entity_type)
        g.db_session.commit()
        return 200

    def put(self, eid):
        """ Updates an entity type.
        """
        try:
            entity_type = g.db_session.query(tables.EntityType).get(eid)
            if not entity_type:
                abort(404)

            data = entity_type_args.parse_args()
            entity_type.type = data['type']
            metadata.validate(entity_type)
            g.db_session.commit()

            return marshal(entity_type, entity_type_format), 200

        except ValidationError as e:
            abort(400, str(e))


class EntityType(Resource):
    def get(self):
        """ List all the entity types
        """
        entity_type_list = g.db_session.query(tables.EntityType).all()
        return marshal(entity_type_list, entity_type_format), 200

    def post(self):
        """ Creates a new entity type
        """
        try:
            data = entity_type_args.parse_args()
            entity_type = tables.EntityType(type=data['type'])
            metadata.validate(entity_type)
            g.db_session.add(entity_type)
            g.db_session.commit()
            return marshal(entity_type, entity_type_format), 200

        except ValidationError as e:
            abort(400, str(e))
