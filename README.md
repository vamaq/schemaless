# Graph schemaless POC using a RDBMS... kind of

So, the idea of this repository is just to work as a playground to test some ideas on a schemaless approach using a RDBMS (quite contradictory right?).

Using a property graph DB like neo4j might be the right call instead of using this approach, but at the same time, some systems might need a migration path and this implementation might help on setting the bases.

Additionally a validation method was put in place in order to keep track of the supported defined attributes and relations. I guess it might be called an ontology validation.

Conceptually speaking this might look as a salad, but it’s not so bad after you play a little bit with it.

Enjoy your salad!

## Setup

1. Create virtual environment

```sh
make virtualenv
```

2. Start DB

```sh
make db-start
```

3. Apply migrations

In a new console:

```sh
. venv/bin/activate
make db-migrations
```

4. Start the backend web server

```sh
. venv/bin/activate
make back-start
```

5. Start the frontend web server

In a new console:

```sh
make front-start
```

## Some notes

The backend API works on the 8090 port and the frontend on the 8080.
A proxy is configured on vue.config.js in order to route frontend calls to the backend server https://cli.vuejs.org/config/#devserver-proxy
