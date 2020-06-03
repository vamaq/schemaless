import sqlalchemy
from sqlalchemy.orm import sessionmaker

from config import config
from model.tables import Node, Relation, EntityType, EntityTypeDefinition

# pylint: disable=no-member

engine = sqlalchemy.create_engine(config['SQLALCHEMY_URL'])
session = sessionmaker(bind=engine)()

#### Deletes all the tables

session.query(Relation).delete()
session.query(Node).delete()
session.query(EntityTypeDefinition).delete()
session.query(EntityType).delete()

session.commit()
