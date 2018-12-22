from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Category, Base, Item, User

engine = create_engine('sqlite:///itemcatalog.db')

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# users
user1 = User(name="Lujain Ghul", email="lujain.ghul@gmail.com")

session.add(user1)
session.commit()

user2 = User(name="Abdulrahman", email="abdulrahman@gmail.com")

session.add(user2)
session.commit()


# first Category
football = Category(name="Football")

session.add(football)
session.commit()


worldCup = Item(title="World Cup", description='''The 2018 FIFA World Cup was
the 21st FIFA World Cup, an international football tournament contested by
the men's national teams of the member associations of FIFA once every
four years. It took place in Russia from 14 June to 15 July 2018.
It was the first World Cup to be held in Eastern Europe,
and the 11th time that it had been held in Europe.
At an estimated cost of over $14.2 billion,
it was the most expensive World Cup.
It was also the first World Cup to use
the video assistant referee (VAR) system.''', category=football, user=user1)

session.add(worldCup)
session.commit()

championsleague = Item(title="champions league", description='''The UEFA
Champions League (abbreviated as UCL) is an annual club football
competition organised by the Union of European Football Associations
(UEFA) and contested by top-division European clubs. It is one of the
most prestigious tournaments in the world and the most prestigious club
competition in European football, played by the national league champions
(and, for some nations, one or more runners-up) of the strongest UEFA
national associations. The UEFA Champions League final is the most
watched annual sporting event worldwide.''', category=football, user=user1)

session.add(championsleague)
session.commit()

# second Category
movies = Category(name="Movies")

session.add(movies)
session.commit()


interstellar = Item(title="Interstellar", description='''In Earth's future,
a global crop blight and second Dust Bowl are slowly rendering the planet
uninhabitable. Professor Brand (Michael Caine), a brilliant NASA physicist,
is working on plans to save mankind by transporting Earth's population to a
new home via a wormhole. But first, Brand must send former NASA pilot Cooper
(Matthew McConaughey) and a team of researchers through the wormhole and
across the galaxy to find out which of three planets could be mankind's
new home.''', category=movies, user=user2)

session.add(interstellar)
session.commit()

TSR = Item(title="The Shawshank Redemption", description='''Andy Dufresne
(Tim Robbins) is sentenced to two consecutive life terms in prison for
the murders of his wife and her lover and is sentenced to a tough prison.
However, only Andy knows he didn't commit the crimes. While there, he forms
a friendship with Red (Morgan Freeman), experiences brutality of prison life,
adapts, helps the warden, etc.,
all in 19 years.''', category=movies, user=user2)

session.add(TSR)
session.commit()


# third Category
smartphones = Category(name="Smartphones")

session.add(smartphones)
session.commit()


samsungNote8 = Item(title="Samsung Note 8", description='''The Samsung Galaxy
Note 8 is an Android phablet smart phone designed, developed and marketed by
Samsung Electronics. Unveiled on 23 August 2017, it is the successor to the
discontinued Samsung Galaxy Note 7. It became available on
15 September 2017.''', category=smartphones, user=user1)

session.add(samsungNote8)
session.commit()

iphonex = Item(title="iphone X", description='''iPhone X is a
smartphone designed, developed, and marketed by Apple Inc. It was the
eleventh generation of the iPhone. It was announced
on September 12, 2017, alongside the iPhone 8 and iPhone 8 Plus,
at the Steve Jobs Theater in the Apple Park campus.
The phone was released on November 3, 2017,
marking the iPhone series'
tenth anniversary.''', category=smartphones, user=user1)

session.add(iphonex)
session.commit()

# fourth Category
geography = Category(name="Geography")

session.add(geography)
session.commit()


saudiArabia = Item(title="Saudi Arabia", description='''The Kingdom
of Saudi Arabia is a country situated in Southwest Asia,
the largest country of Arabia, by the Arabian Peninsula,
bordering the Arabian Gulf(Persian Gulf) and the Red Sea,
north of Yemen. Its extensive coastlines on the Arabian Gulf
and Red Sea provide great leverage on shipping through the
Persian Gulf and Suez Canal.''', category=geography, user=user2)

session.add(saudiArabia)
session.commit()

molossia = Item(title="Molossia", description='''Molossia,
officially the Republic of Molossia, is a claimed micronation
bordering the United States, founded by Kevin Baugh and headquartered
at his home near Dayton, Nevada. The Republic of Molossia has claimed
itself a nation but it is not recognised as a country by the United
Nations or any major government.''', category=geography, user=user2)

session.add(molossia)
session.commit()

# Fifth Category
celebrities = Category(name="Celebrities")

session.add(celebrities)
session.commit()


pewdiepie = Item(title="Pewdiepie", description='''Felix Arvid Ulf Kjellberg,
known online as PewDiePie, is a Swedish YouTuber,
comedian and video game commentator, formerly best known for his Let's Play
commentaries and now mostly known for his comedic formatted shows
like Meme Review,
You Lough You Lose and Pew News''', category=celebrities, user=user2)

session.add(pewdiepie)
session.commit()

# sixth Category
cars = Category(name="Cars")

session.add(cars)
session.commit()


bmw = Item(title="BMW", description='''originally an initialism for
Bayerische Motoren Werke in German, or Bavarian Motor Works in English)
is a German multinational company which currently produces luxury automobiles
and motorcycles, and also produced aircraft engines until 1945.
The company was founded in 1916 and has its headquarters in Munich,
Bavaria. BMW produces motor vehicles in Germany, Brazil, China, India,
South Africa, the United Kingdom, and the United States. In 2015,
BMW was the world's twelfth largest producer of motor vehicles,
with 2,279,503 vehicles produced.''', category=cars, user=user2)

session.add(bmw)
session.commit()


print("added menu items!")
