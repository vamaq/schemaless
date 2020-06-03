import sqlalchemy
from sqlalchemy.orm import sessionmaker

from config import config
from model.tables import Node, Relation, EntityType, EntityTypeDefinition

# pylint: disable=no-member

engine = sqlalchemy.create_engine(config['SQLALCHEMY_URL'])
session = sessionmaker(bind=engine)()

#### Add definitions

book_store = EntityType(type='book store')
book = EntityType(type='book')
subject = EntityType(type='subject')
people = EntityType(type='people')

book_store_v0 = EntityTypeDefinition(
    entity_type=book_store, 
    version=0,
    properties=[
        {
            'name': 'name',
            'type': 'string'
        },
        {
            'name': 'address',
            'type': 'string'
        },
    ],
    relations=[
        {
            'label': 'managed by',
            'type': 'people',
            'properties': []
        },
    ]
)

book_store_v1 = EntityTypeDefinition(
    entity_type=book_store,
    version=1,
    properties=[
        {
            'name': 'name',
            'type': 'string'
        },
        {
            'name': 'address',
            'type': 'string'
        },
        {
            'name': 'telephone_number',
            'type': 'string'
        },
    ],
    relations=[
        {
            'label': 'managed by',
            'type': 'people',
            'properties': []
        },
        {
            'label': 'has',
            'type': 'book',
            'properties': [
                {
                    'name': 'quantity',
                    'type': 'integer'
                },
                {
                    'name': 'quantity',
                    'type': 'float'
                }
            ]
        },
    ]
)

book_v1 = EntityTypeDefinition(
    entity_type=book,
    version=1,
    properties=[
        {
            'name': 'title',
            'type': 'string'
        },
        {
            'name': 'publishing_date',
            'type': 'date'
        },
    ],
    relations=[
        {
            'label': 'author',
            'type': 'people',
            'properties': []
        },
        {
            'label': 'subject',
            'type': 'subject',
            'properties': []
        },
    ]
)

subject_v1 = EntityTypeDefinition(
    entity_type=subject,
    version=1,
    properties=[
        {
            'name': 'title',
            'type': 'string'
        },
        {
            'name': 'description',
            'type': 'string'
        },                
        {
            'name': 'keywords',
            'type': 'string'
        },    
    ],
    relations=[]
)

people_v1 = EntityTypeDefinition(
    entity_type=people,
    version=1,
    properties=[
        {
            'name': 'name',
            'type': 'string'
        },
        {
            'name': 'date_of_birth',
            'type': 'date'
        },        
    ],
    relations=[
        {
            'label': 'wrote',
            'type': 'book',
            'properties': []
        },
        {
            'label': 'is manager of',
            'type': 'book_store',
            'properties': []
        },        
    ]
)

session.add_all([book_store, book, subject, people, book_store_v0, book_store_v1, book_v1, subject_v1, people_v1])
session.commit()

#### Add data

issac = Node(definition=people_v1, properties={'name': 'Issac Newton', 'date_of_birth': '1643-01-04T00:00:00'})
albert = Node(definition=people_v1, properties={'name': 'Albert Einstein', 'date_of_birth': '1879-03-14T00:00:00'})
galileo = Node(definition=people_v1, properties={'name': 'Galileo Galilei', 'date_of_birth': '1564-02-15T00:00:00'})
marie = Node(definition=people_v1, properties={'name': 'Marie Curie', 'date_of_birth': '1867-11-07T00:00:00'})
stephen = Node(definition=people_v1, properties={'name': 'Stephen Hawking', 'date_of_birth': '1942-01-08T00:00:00'})
charles = Node(definition=people_v1, properties={'name': 'Charles Darwin', 'date_of_birth': '1809-02-12T00:00:00'})

physics_subject = Node(definition=subject_v1, properties={
    'title': 'physics', 'description': 'Cool stuff', 'keywords': 'nerd, casual talking, standup jokes'}
)

biology_subject = Node(definition=subject_v1, properties={
    'title': 'biology', 'description': 'Dead frogs and plants', 'keywords': 'high school trauma'}
)

principia_mathematica = Node(definition=book_v1, properties={
    'title': 'Philosophiæ naturalis principia mathematica', 'publishing_date': '1687-06-05T00:00:00',
}, relates_to=[
    Relation(relates_to=issac, label='author'),
    Relation(relates_to=physics_subject, label='subject'),
])

substances_radioactives_thesis = Node(definition=book_v1, properties={
    'title': 'Recherches sur les substances radioactives', 'publishing_date': '1903-06-05T00:00:00',
}, relates_to=[
    Relation(relates_to=marie, label='author'),
    Relation(relates_to=physics_subject, label='subject'),
])

origin_of_species = Node(definition=book_v1, properties={
    'title': 'On the Origin of Species', 'publishing_date': '1859-11-24T00:00:00',
}, relates_to=[
    Relation(relates_to=charles, label='author'),
    Relation(relates_to=biology_subject, label='subject'),
])

beautiful_store = Node(definition=book_store_v1, properties={
    'name':'Beautiful Store', 'address': 'Around the corner', 'telephone_number': '+54 11 6749-4534'
}, relates_to=[
    Relation(relates_to=stephen, label='managed by'),
    Relation(relates_to=principia_mathematica, label='has', properties={'quantity': 5, 'price': 20.6}),
    Relation(relates_to=substances_radioactives_thesis, label='has', properties={'quantity': 3, 'price': 21.3}),
])

ugly_store = Node(definition=book_store_v1, properties={
    'name':'Ugly Store', 'address': 'Far far away', 'telephone_number': '+54 2323 42-7511'
}, relates_to=[
    Relation(relates_to=marie, label='managed by'),
    Relation(relates_to=principia_mathematica, label='has', properties={'quantity': 2, 'price': 18.5}),
    Relation(relates_to=origin_of_species, label='has', properties={'quantity': 15, 'price': 7.6}),    
])

session.add_all(
    [
        issac, albert, galileo, marie, stephen, charles,
        physics_subject, biology_subject, 
        principia_mathematica, substances_radioactives_thesis, origin_of_species,
        beautiful_store, ugly_store,
    ]
)
session.commit()
