from app import app
from flask_sqlalchemy import SQLAlchemy
from os import getenv
from sqlalchemy import text

app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL").replace("://", "ql://", 1)
db = SQLAlchemy(app)

file = open('schema.sql', 'r')
schema = file.read()
file.close()

app.app_context().push()
db.session.execute(text(schema))
db.session.commit()