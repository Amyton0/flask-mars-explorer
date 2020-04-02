from data import db_session
from data.users import User

db = input()

db_session.global_init("db/" + db)

session = db_session.create_session()
for user in session.query(User).filter(User.address == "module_1"):
    print(user)
