from flask import Flask, Blueprint
from flask_restful import Api, Resource

from api.v1.entity_type import EntityType, EntityTypeEid
from api.v1.entity_type_definition import EntityTypeDefinition, EntityTypeDefinitionEid


def get_api_v1():
    """ Returns the api blueprint
    """
    api_bp = Blueprint('api_v1', __name__, url_prefix='/api/v1')
    api = Api(api_bp)

    api.add_resource(EntityTypeEid, '/entity-type/<eid>')
    api.add_resource(EntityType, '/entity-type/')

    api.add_resource(EntityTypeDefinitionEid, '/entity-type-definition/<eid>')
    api.add_resource(EntityTypeDefinition, '/entity-type-definition/')

    return api_bp
