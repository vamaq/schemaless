from flask import Flask, request, g, abort
from flask_restful import Resource, reqparse, fields, marshal
from jsonschema.exceptions import ValidationError

from .entity_type import entity_type_format
from .filters import filter_type, single_table_query_filter
from model import tables, metadata

from sqlalchemy.sql import func, and_


entity_type_definition_format = {
    'eid': fields.String,
    'version': fields.Integer,
    'properties': fields.Raw,
    'relations': fields.Raw,
    'entity_type': fields.Nested(entity_type_format)
}


etd_update_args = reqparse.RequestParser(bundle_errors=True)
etd_update_args.add_argument('properties', type=dict, required=False, action='append', default=[])
etd_update_args.add_argument('relations', type=dict, required=False, action='append', default=[])


etd_create_args = reqparse.RequestParser(bundle_errors=True)
etd_create_args.add_argument('entity_type_eid', type=str, required=True)
etd_create_args.add_argument('properties', type=dict, required=False, action='append', default=[])
etd_create_args.add_argument('relations', type=dict, required=False, action='append', default=[])

filter_args = reqparse.RequestParser(bundle_errors=True)
filter_args.add_argument('filters', type=filter_type, required=False, action='append', default=None, location='args')


class EntityTypeDefinitionEid(Resource):
    def get(self, eid):
        """ Gets one single entity type definition
        """
        etd = g.db_session.query(tables.EntityTypeDefinition).get(eid)
        if not etd:
            abort(404)
        return marshal(etd, entity_type_definition_format), 200

    def delete(self, eid):
        """ Deletes a entity type definition.
        """
        etd = g.db_session.query(tables.EntityTypeDefinition).get(eid)
        if not etd:
            abort(404)
        g.db_session.delete(etd)
        g.db_session.commit()
        return 200

    def put(self, eid):
        """ Updates an entity type definition
        """
        try:
            etd = g.db_session.query(tables.EntityTypeDefinition).get(eid)
            if not etd:
                abort(404, 'Definition not found')

            latest_etd = g.db_session.query(
                tables.EntityTypeDefinition
            ).filter(
                tables.EntityTypeDefinition.entity_type_eid == etd.entity_type_eid
            ).order_by(
                tables.EntityTypeDefinition.version.desc()
            ).first()

            if latest_etd != etd:
                abort(400, 'Not the latest version')

            data = etd_update_args.parse_args()
            new_etd = tables.EntityTypeDefinition(
                entity_type_eid=etd.entity_type_eid,
                version=etd.version + 1,
                properties=data['properties'] if 'properties' in data else etd.properties,
                relations=data['relations'] if 'relations' in data else etd.relations,
            )

            metadata.validate(new_etd)
            g.db_session.add(new_etd)
            g.db_session.commit()

            return marshal(new_etd, entity_type_definition_format), 200

        except ValidationError as e:
            abort(400, str(e))


class EntityTypeDefinition(Resource):
    def get(self):
        """ List all the entity types definitions matching the provided filter.
        """
        try:
            data = filter_args.parse_args()
            etd_list = single_table_query_filter(
                g.db_session.query(tables.EntityTypeDefinition),
                data['filters']
            ).all()
            return marshal(etd_list, entity_type_definition_format), 200
        except ValueError as e:
            abort(400, str(e))

    def post(self):
        """ Creates a new entity type definition.
        Checks if a etd exists for the same entity and raise an error (in that case an update should be made).
        """
        try:
            data = etd_create_args.parse_args()

            existing_etd = g.db_session.query(
                tables.EntityTypeDefinition
            ).filter(
                tables.EntityTypeDefinition.entity_type_eid == data['entity_type_eid']
            ).first()

            if existing_etd:
                abort(400, f'Already existing etd for entity definition {existing_etd.entity_type.type}')

            etd = tables.EntityTypeDefinition(
                version=1,
                entity_type_eid=data['entity_type_eid'],
                properties=data['properties'],
                relations=data['relations'],
            )
            metadata.validate(etd)
            g.db_session.add(etd)
            g.db_session.commit()
            return marshal(etd, entity_type_definition_format), 200

        except ValidationError as e:
            abort(400, str(e))


class EntityTypeDefinitionLatestEid(Resource):
    def get(self, eid):
        """ Gets one single entity type latest definition.
        """
        sub = g.db_session.query(
            tables.EntityTypeDefinition.entity_type_eid.label('entity_type_eid'),
            func.max(tables.EntityTypeDefinition.version).label('version')
        ).filter(
            tables.EntityTypeDefinition.entity_type_eid == eid
        ).group_by(
            tables.EntityTypeDefinition.entity_type_eid
        ).subquery()

        latest_definition = g.db_session.query(
            tables.EntityTypeDefinition
        ).join(
            sub,
            and_(
                sub.c.entity_type_eid == tables.EntityTypeDefinition.entity_type_eid,
                sub.c.version == tables.EntityTypeDefinition.version,
            ),
        ).first()

        if not latest_definition:
            abort(404)

        return marshal(latest_definition, entity_type_definition_format), 200
