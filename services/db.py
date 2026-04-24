from app import app
from flask_sqlalchemy import SQLAlchemy
from os import getenv
from sqlalchemy import text

database_url = getenv("DATABASE_URL", "sqlite:///local.db")

app.config["SQLALCHEMY_DATABASE_URI"] = database_url
db = SQLAlchemy(app)

file = open('schema.sql', 'r')
schema = file.read()
file.close()

app.app_context().push()

for command in schema.split(';'):
    command = command.strip()
    if command:
        db.session.execute(text(command))
db.session.commit()
