from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
 
Base = declarative_base()

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key = True)
    name =Column(String(200), nullable = False)
    email = Column(String(200), nullable = False)
    picture = Column(String(250))
    
class Category(Base):
    __tablename__ = 'category'
   
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    items = relationship('Item', backref='within')

    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
           'id'           : self.id,
           'name'         : self.name,
       }
 
class Item(Base):
    __tablename__ = 'item'


    title =Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)
    description = Column(String(250))
    category_id = Column(Integer,ForeignKey('category.id'))
    category = relationship(Category)
    #user_id = Column(Integer,ForeignKey('user.id'))
    #user = relationship(User)


    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
           'cat_id'         : self.category_id,
           'description'         : self.description,
           'id'         : self.id,
           'title'         : self.title,
       }

engine = create_engine('sqlite:///itemcatalog.db')
 

Base.metadata.create_all(engine)
