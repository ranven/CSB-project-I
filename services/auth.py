import secrets
from werkzeug.security import check_password_hash, generate_password_hash
from flask import abort, session
from services.db import db


def signup(username, password):
    # Flaw 4 (A02): Instead of creating a securely hashed password using a cryptographic library, passwords are saved to database as plain text. This is a very bad practice and violates data protection.
    # Fix: Instead of saving passwords to db in plain text, a proper cryptographic algorithm is used to generate a hash for the password, which is then saved to db and checked against when signing in. To implement fix, comment out lines 10, 15 and 30 and remove line 29
    # hash_value = generate_password_hash(password)

    try:
        sql = "INSERT INTO users (username, password) VALUES (:username, :password)"
        # db.session.execute(sql, {"username": username, "password": password})
        db.session.execute(sql, {"username": username, "password": hash_value})
        db.session.commit()
    except:
        return False

    return login(username, password)


def login(username, password):
    sql = "SELECT user_id, password FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username": username})
    user = result.fetchone()

    if user:
        if user.password == password:
            # if check_password_hash(user.password, password):
            session["user_id"] = user.user_id
            session["username"] = username
            session["csrf_token"] = secrets.token_hex(16)
            return True
    return False


def logout():
    del session["user_id"]
    del session["username"]
    del session["csrf_token"]


def user_id():
    return session.get("user_id", 0)
