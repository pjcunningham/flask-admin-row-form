# coding: utf-8
__author__ = 'Paul Cunningham'
__copyright = 'Copyright 2019, Paul Cunningham'

import random
from flask.cli import click, with_appcontext
from models import db, Student


@click.command('create-database')
@with_appcontext
def create_database():

    # Create 100 students

    db.drop_all()
    db.create_all()

    for _ in range(0, 100):
        _project = Student(
            cost=random.randrange(10, 200),
            is_paid=False
        )
        db.session.add(_project)

    db.session.commit()

