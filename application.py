from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item
from flask import session as login_session
import random
import string


app = Flask(__name__)

engine = create_engine('sqlite:///itemcatalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Show all restaurants
@app.route('/')
@app.route('/catalog/')
def showCategories():
    categories = session.query(Category)
    return render_template('catalog.html', categories = categories)

@app.route('/catalog/<int:catagory_id>/')
@app.route('/catalog/<int:catagory_id>/details')
def categoryDetails(catagory_id):
    category = session.query(Category).filter_by(id=catagory_id).one()
    items = session.query(Item).filter_by(catagory_id=category.id).all()
    return render_template('categoryDetails.html', items=items, category=category)

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000,threaded =False)