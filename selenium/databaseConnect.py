from sqlalchemy import create_engine, MetaData,Table
import os
from databaseConnectDetails import *


username = unameHeroku
password = passwordHeroku


URI = 'mysql://'+str(username)+':'+str(password)+'@us-cdbr-iron-east-04.cleardb.net/heroku_f8b7f102c73b268'
engine = create_engine(URI)
connection = engine.connect()

print(engine.table_names())

metadata = MetaData()

user = Table('user', metadata, autoload=True , aoutoload_with=engine)

#print(repr(user))

stmt = 'SELECT * FROM user'
result_proxy = connection.execute(stmt)
results = result_proxy.fetchall()
print results


