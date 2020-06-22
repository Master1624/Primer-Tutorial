from flask import Flask
from flask_mysqldb import MySQL
from tutorial import secret

app = Flask(__name__)
app.config['SERVER_NAME']='localhost:8000'
app.config['SECRET_KEY'] = 'e3a27f516cb98cd89b3db1a2cf87add9'

app.config['MYSQL_HOST'] = secret.dbhost
app.config['MYSQL_USER'] = secret.dbuser
app.config['MYSQL_PASSWORD'] = secret.dbpassword
app.config['MYSQL_DB'] = secret.dbname

db = MySQL(app)

from tutorial import routes