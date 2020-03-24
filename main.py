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
session = db_session.create_session()
session.add(user)
session.commit()
