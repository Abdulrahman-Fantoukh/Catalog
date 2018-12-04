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

# Show all categories
@app.route('/')
@app.route('/catalog/')
def showCategories():
    categories = session.query(Category)
    return render_template('catalog.html', categories = categories)

# Show all category items
@app.route('/catalog/<int:category_id>/')
@app.route('/catalog/<int:category_id>/details')
def categoryDetails(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(Item).filter_by(category_id=category.id).all()
    return render_template('categoryDetails.html', items=items, category=category)

# show item description
@app.route('/catalog/<int:category_id>/<int:item_id>')
@app.route('/catalog/<int:category_id>/<int:item_id>/details')
def itemDetails(category_id,item_id):
    category = session.query(Category).filter_by(id=category_id).one()
    item = session.query(Item).filter_by(category_id=category.id,id = item_id).one()
    return render_template('itemDetails.html', item=item, category=category)

# Add new category item
@app.route('/catalog/<int:category_id>/details/new/', methods=['GET', 'POST'])
def newCategoryItem(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    if request.method == 'POST':
        newItem = Item(title=request.form['title'], description=request.form['description'], category_id=category_id)
        session.add(newItem)
        session.commit()
        flash('New category Item %s Successfully Created' % (newItem.title))
        return redirect(url_for('categoryDetails', category_id=category_id))
    else:
        return render_template('newCategoryItem.html', category=category)

# Edit item 
@app.route('/catalog/<int:category_id>/<int:item_id>/edit/', methods=['GET', 'POST'])
def editItem(category_id,item_id):
    category = session.query(Category).filter_by(id=category_id).one()
    editedItem = session.query(Item).filter_by(category_id=category.id,id = item_id).one()
    if request.method == 'POST':
        if request.form['title']:
            editedItem.title = request.form['title']
            editedItem.description = request.form['description']
            flash('%s Successfully Edited' % editedItem.title)
            return redirect(url_for('itemDetails',category_id = category.id, item_id = editedItem.id))
    else:
        return render_template('editItem.html', item=editedItem, category = category)

# Delete category item
@app.route('/catalog/<int:category_id>/<int:item_id>/delete/', methods=['GET', 'POST'])
def deleteItem(category_id,item_id):
    category = session.query(Category).filter_by(id=category_id).one()
    deletedItem = session.query(Item).filter_by(category_id=category.id,id = item_id).one()
    if request.method == 'POST':
        session.delete(deletedItem)
        session.commit()
        flash('Item %s Successfully deleted' % (deletedItem.title))
        return redirect(url_for('categoryDetails', category_id=category_id))
    else:
        return render_template('deleteItem.html', category=category,item = deletedItem)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000,threaded =False)