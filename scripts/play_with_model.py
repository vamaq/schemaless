# pylint: disable=no-member

import sqlalchemy
from sqlalchemy.orm import sessionmaker

from config import config
from model.tables import Node, Relation, EntityType, EntityTypeDefinition
from model.metadata import validate

from sqlalchemy.orm import configure_mappers
configure_mappers()

# If you need additional debug info uncomment 
kwargs = {
    # echo: "debug",
}

engine = sqlalchemy.create_engine(config["SQLALCHEMY_URL"], **kwargs)
session = sessionmaker(bind=engine)()

# To have contron on when are we hitting the DB
sqlalchemy.event.listen(engine, "before_cursor_execute", lambda *a, **k: print('------------'))

# Run validations in entity type definitions

etd = session.query(EntityTypeDefinition).all()
for e in etd:
    validate(e)

# Some queries

etd = session.query(EntityTypeDefinition).all()
etd[0].entity_type
nodes = etd[0].entity_type.nodes
nodes[0].relates_to[0].relates_to.properties

# Basic filter

session.query(
    Node.properties["title"]
).filter(
    Node.properties["title"].cast(sqlalchemy.Unicode) == '"On the Origin of Species"'
).all()

session.query(
    Node.properties["title"]
).join(
    EntityTypeDefinition
).join(
    EntityType
).filter(
    EntityType.type == 'book'
).all()

# Using properties for join and entity for filter

nodes = session.query(
    Node
).join(
    Node.entity_type,
).filter(
    EntityType.type == 'book'
).all()

# Query: Sorted by price property at the relation.

session.query(
    Node.properties, Relation.properties
).join(
    Node.definition,
    EntityTypeDefinition.entity_type,
    Node.relates_from,
).filter(
    EntityType.type == 'book'
).order_by(
    Relation.properties["price"].desc()
).all()

# Query: get the latest definition version 

session.query(
    EntityTypeDefinition
).filter(
    EntityType.eid == 'EID'
).order_by(
    EntityTypeDefinition.version.desc()
).first()