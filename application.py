from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item, User
from sqlalchemy.pool import SingletonThreadPool
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

# use back ref to build reference between category and item
# or do the list ob object idea
app = Flask(__name__)

engine = create_engine('sqlite:///itemcatalog.db',  poolclass=SingletonThreadPool)
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

CLIENT_ID = json.loads(open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Item catalog Application"

# Create anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)

@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print ("Token's client ID does not match app's.")
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['email'] = data['email']
    login_session['picture'] = data['picture']

    # see if user exists, if it doesn't make a new one
    user_id = getUserID(data["email"])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    flash("you are now logged in as %s" % login_session['username'])
    print ("done!")
    return output

# User Helper Functions
def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None

# DISCONNECT - Revoke a current user's token and reset their login_session
@app.route('/gdisconnect')
def gdisconnect():
    # Only disconnect a connected user.
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] == '200':
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        del login_session['gplus_id']
        del login_session['access_token']
        del login_session['username']
        del login_session['email']
        del login_session['user_id']
        flash("you loggedout successfully")
        return redirect('/')#redirect to show catalog then do the other steps to add delete edit
    else:
        response = make_response(json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response

#JSON API for catalog categories
@app.route('/<int:category_id>/JSON')
def categoryItemsJSON(category_id):
    items = session.query(Item).filter_by(
        category_id=category_id).all()
    return jsonify(Category=[category.serialize for category in items])

# JSON API for a category items
@app.route('/<int:category_id>/<int:item_id>/JSON')
def categoryItemJSON(category_id, item_id):
    item = session.query(Item).filter_by(id=item_id).one()
    return jsonify(Item=item.serialize)

# Show all categories
@app.route('/')
@app.route('/catalog/')
def showCategories():
    categories = session.query(Category)
    Items = session.query(Item).all()
    counter=0
    length= len(Items)
    print(length)
    latestItems =[]
    latestItemCat = []
    if length<=10:
        while counter<length:
            print(counter)
            print(Items[counter].title)
            latestItems.append(Items[counter])
            D = Items[counter]
            cat = session.query(Category).filter_by(id = D.category_id).one()
            latestItemCat.append(cat)
            counter+=1
        return render_template('catalog.html', categories = categories,theList = zip(latestItems,latestItemCat),pictureURL=login_session['picture'])
    else:
        while length-counter !=10:
            counter+=1
        
        while length-counter != 0:
            latestItems.append(Items[counter])
            D = Items[counter]
            cat = session.query(Category).filter_by(id = D.category_id).one()
            latestItemCat.append(cat)
            counter+=1
        if 'username' not in login_session:
            return render_template('catalog.html', categories = categories,theList = zip(latestItems,latestItemCat))
        else:
            return render_template('catalog.html', categories = categories,pictureURL=login_session['picture'],theList = zip(latestItems,latestItemCat))

# Show all category items
@app.route('/catalog/<int:category_id>/')
@app.route('/catalog/<int:category_id>/details')
def categoryDetails(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(Item).filter_by(category_id=category.id).all()
    if 'username' not in login_session:
        return render_template('publicCategoryDetails.html', items=items, category=category)
    return render_template('categoryDetails.html', items=items, category=category, category_id = category_id,pictureURL=login_session['picture'])

# show item description
@app.route('/catalog/<int:category_id>/<int:item_id>')
@app.route('/catalog/<int:category_id>/<int:item_id>/details')
def itemDetails(category_id,item_id):
    category = session.query(Category).filter_by(id=category_id).one()
    item = session.query(Item).filter_by(category_id=category_id,id = item_id).one()
    if 'username' not in login_session:
        return render_template('publicItemDetails.html', item=item, category=category)
    return render_template('itemDetails.html', item=item, category=category,pictureURL=login_session['picture'])

# Add new category item --- for main add item loop throw the Category and save it to variable 
@app.route('/catalog/<int:category_id>/details/new/', methods=['GET', 'POST'])
def newCategoryItem(category_id):
    if 'username' not in login_session:
        return redirect('/login')
    category = session.query(Category).filter_by(id=category_id).one()
    if request.method == 'POST':
        newItem = Item(title=request.form['title'], description=request.form['description'], category_id=category_id)
        session.add(newItem)
        session.commit()
        flash('New category Item %s Successfully Created' % (newItem.title))
        return redirect(url_for('categoryDetails', category_id=category_id,pictureURL=login_session['picture']))
    else:
        return render_template('newCategoryItem.html', category=category,pictureURL=login_session['picture'])

#for main add
@app.route('/catalog/new', methods=['GET', 'POST'])
def newItem():
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        if request.form['title']:
            category = session.query(Category).filter_by(name= request.form['category']).one()
            newItem = Item(title=request.form['title'], description=request.form['description'], category_id=category.id)
            session.add(newItem)
            session.commit()
            flash('New category Item %s Successfully Created' % (newItem.title))
            return redirect(url_for('categoryDetails', category_id=category.id,pictureURL=login_session['picture']))
    else:
        return render_template('newItemForm.html',pictureURL=login_session['picture'])

# Edit item 
@app.route('/catalog/<int:category_id>/<int:item_id>/edit/', methods=['GET', 'POST'])
def editItem(category_id,item_id):
    if 'username' not in login_session:
        return redirect('/login')
    category = session.query(Category).filter_by(id=category_id).one()
    editedItem = session.query(Item).filter_by(category_id=category_id,id = item_id).one()
    if request.method == 'POST':
        Cname = request.form['category']
        newC = session.query(Category).filter_by(name = Cname).one()
        newID = newC.id
        if request.form['title']:
            editedItem.title = request.form['title']
            editedItem.description = request.form['description']
            editedItem.category_id = newID
            newItem = editedItem
            session.delete(editedItem)
            session.add(newItem)
            session.commit()
            flash('%s Successfully Edited' % editedItem.title)
            return redirect(url_for('itemDetails',category_id =newID , item_id = newItem.id,pictureURL=login_session['picture']))
    else:
        return render_template('editItem.html', item=editedItem, category = category,pictureURL=login_session['picture'])

# Delete category item
@app.route('/catalog/<int:category_id>/<int:item_id>/delete/', methods=['GET', 'POST'])
def deleteItem(category_id,item_id):
    if 'username' not in login_session:
        return redirect('/login')
    category = session.query(Category).filter_by(id=category_id).one()
    deletedItem = session.query(Item).filter_by(category_id=category.id,id = item_id).one()
    if request.method == 'POST':
        session.delete(deletedItem)
        session.commit()
        flash('Item %s Successfully deleted' % (deletedItem.title))
        return redirect(url_for('categoryDetails', category_id=category_id,pictureURL=login_session['picture']))
    else:
        return render_template('deleteItem.html', category=category,item = deletedItem,pictureURL=login_session['picture'])


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000,threaded =False)