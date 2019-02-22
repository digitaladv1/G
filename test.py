from tinydb import TinyDB, Query
db=TinyDB('World.json')





print(db.all()[0])
