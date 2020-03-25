from data import db_session
from data.users import User

db_session.global_init("db/mars_explorer.sqlite")

user = User()
user.surname = "Scott"
user.name = "Ridley"
user.age = "21"
user.position = "captain"
user.speciality = "research engineer"
user.address = "module_1"
user.email = "scott_chief@mars.org"

user2 = User()
user2.surname = "Iton"
user2.name = "Amy"
user2.age = "19"
user2.position = "first mate"
user2.speciality = "pilot"
user2.address = "module_2"
user2.email = "amy_iton@mars.org"

user3 = User()
user3.surname = "Gurt"
user3.name = "David"
user3.age = "25"
user3.position = "navigator"
user3.speciality = "navigator"
user3.address = "module_1"
user3.email = "davgu@mars.org"

user4 = User()
user4.surname = "Kotty"
user4.name = "Ray"
user4.age = "20"
user4.position = "second mate"
user4.speciality = "terraforming engineer"
user4.address = "module_3"
user4.email = "kotty@mars.org"

session = db_session.create_session()
session.add(user)
session.add(user2)
session.add(user3)
session.add(user4)
session.commit()
