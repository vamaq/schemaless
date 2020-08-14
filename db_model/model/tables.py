import uuid as uuid_
import base64
from datetime import datetime
from typing import List, Tuple

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm.session import Session
from sqlalchemy.orm import backref

from model import Base


# pylint: disable=no-member

def uuid():
    """ Get an uid that is text just that
    """
    bytes_ = base64.b32encode(uuid_.uuid4().bytes)
    return bytes_[0:25].decode('utf-8')


class InvalidDefinition(Exception):
    """Invalid definition check """


class TimestampMixin():
    """ Introduce timestamps
    """
    created_date = sa.Column(sa.DateTime, nullable=False, default=datetime.utcnow)
    updated_date = sa.Column(sa.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)


class EntityType(TimestampMixin, Base):
    """ Identifies the type of node element.
    """
    __tablename__ = "entity_type"

    eid = sa.Column(sa.Unicode, primary_key=True, default=uuid)
    type = sa.Column(sa.Unicode, nullable=False, unique=True)

    nodes = sa.orm.relationship(
        "Node",
        secondary="entity_type_definition",
        viewonly=True,
        sync_backref=False,
        backref=backref(
            "entity_type",
            uselist=False,
            lazy='subquery',
            single_parent=True
        ),
    )


class EntityTypeDefinition(TimestampMixin, Base):
    """ Keepts the supported definition for each entity.
    """
    __tablename__ = "entity_type_definition"
    __table_args__ = (
        sa.UniqueConstraint('entity_type_eid', 'version', name='entity_type_definition_uq'),
    )

    eid = sa.Column(sa.Unicode, primary_key=True, default=uuid)
    version = sa.Column(sa.INTEGER, nullable=False)

    properties = sa.Column(postgresql.JSONB, nullable=False)
    relations = sa.Column(postgresql.JSONB, nullable=False)

    entity_type_eid = sa.Column(sa.Unicode, sa.ForeignKey('entity_type.eid'), nullable=False)
    entity_type = sa.orm.relationship(
        "EntityType",
        # single_parent=True,
        # cascade="all",
        backref=backref(
            "entity_type_definitions",
            uselist=True,
            # lazy='subquery',
            single_parent=True,
            cascade="all, delete-orphan",
        ),
    )


class Relation(TimestampMixin, Base):
    """ Associative entity between node
    """
    __tablename__ = "relation"
    __mapper_args__ = {'confirm_deleted_rows' : False}

    eid = sa.Column(sa.Unicode, primary_key=True, default=uuid)

    node_to_eid = sa.Column(sa.Unicode, sa.ForeignKey('node.eid'), primary_key=True)
    relates_to = sa.orm.relationship(
        "Node",
        primaryjoin="Relation.node_to_eid == Node.eid",
        backref=backref(
            "relates_from",
            uselist=True,
            cascade="all",
        ),
    )

    node_from_eid = sa.Column(sa.Unicode, sa.ForeignKey('node.eid'), primary_key=True)
    relates_from = sa.orm.relationship(
        "Node",
        primaryjoin="Relation.node_from_eid == Node.eid",
        backref=backref(
            "relates_to",
            uselist=True,
            cascade="all",
            lazy="subquery"
        ),
    )

    label = sa.Column(sa.Unicode, nullable=False) # The label describing the relation     
    properties = sa.Column(postgresql.JSONB, nullable=False, default={})


class Node(TimestampMixin, Base):
    """ Some Node just because.
    """
    __tablename__ = "node"

    eid = sa.Column(sa.Unicode, primary_key=True, default=uuid)
    properties = sa.Column(postgresql.JSONB, nullable=False, default={})

    definition_eid = sa.Column(
        sa.Unicode,
        sa.ForeignKey('entity_type_definition.eid'),
        nullable=False
    )
    definition = sa.orm.relationship(
        "EntityTypeDefinition",
        cascade="all",
        # lazy="subquery",
        backref=backref(
            "node_entities",
            # lazy='subquery',
            cascade="all, delete-orphan"
        ),
    )
    node_to = sa.orm.relationship(
        "Node",
        secondary=Relation.__table__,
        primaryjoin=eid == Relation.__table__.c.node_from_eid,
        secondaryjoin=Relation.__table__.c.node_to_eid == eid,
        backref=backref("node_from"), 
    )
