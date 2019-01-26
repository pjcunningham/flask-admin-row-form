# coding: utf-8
__author__ = 'Paul Cunningham'
__copyright = 'Copyright 2019, Paul Cunningham'

from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cost = db.Column(db.Integer(), nullable=False)
    is_paid = db.Column(db.Boolean(), nullable=False)

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        return "ID: {id}; Cost : {cost}".format(id=self.id, cost=self.cost)
