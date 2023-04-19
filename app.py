import os
import json
import functools
import logging
from flask import (Flask, render_template, request, url_for, redirect, jsonify)
# from flask import current_app, flash, jsonify, make_response, redirect, request, url_for
from sqlalchemy.sql import func
from sqlalchemy.exc import IntegrityError



from flask_sqlalchemy import SQLAlchemy
from dataclasses import dataclass

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'sqlite_database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

@dataclass
class Drink(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(120))
    created_at =  db.Column(db.DateTime(timezone=True),server_default=func.now())

    def __init__(self, name, description):
        self.name = name
        self.description = description

    def __repr__(self):
        return f"id:name-desc=[{self.id} : {self.name} - {self.description}]"

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/drinks')
def drinks():
    Drinks = Drink.query.all()
    return render_template('drinks.html', Drinks=Drinks)

@app.route('/reset')
def reset():
    db.drop_all() 
    db.create_all()
    db.session.add(Drink(name="Grape Soda", description="Wine like juicy tuity"))
    db.session.add(Drink(name="Cola Soda", description="Coke like juicy liquid"))
    db.session.add(Drink(name="Pepsi Soda", description="Pepsimax like juicy sauce"))
    db.session.add(Drink(name="Filt Soda", description="Lilt like juicy water"))
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
    return render_template('reset.html')


if __name__ == '__main__':
    app.run(debug = True)
    reset()



