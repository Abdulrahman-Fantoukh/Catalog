from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Category, Base, Item
 
engine = create_engine('sqlite:///itemcatalog.db')

Base.metadata.bind = engine
 
DBSession = sessionmaker(bind=engine)

session = DBSession()


#first Category
football = Category(name = "Football")

session.add(football)
session.commit()


ball = Item(title = "Ball", description = "used to kick it to the goal",category = football)

session.add(ball)
session.commit()

shoes = Item(title = "shoes", description = "wear it because you will need it",category = football)

session.add(shoes)
session.commit()

#second Category
snowboarding = Category(name = "Snowboarding")

session.add(snowboarding)
session.commit()


goggles = Item(title = "Goggles", description = "to protect your eyes to get snow",category = snowboarding)

session.add(goggles)
session.commit()

snowboard = Item(title = "snowboard", description = "its good :)",category = snowboarding)

session.add(snowboard)
session.commit()

print ("added menu items!")