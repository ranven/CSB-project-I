import secrets
from werkzeug.security import check_password_hash, generate_password_hash
from flask import abort, session
from services.db import db
from datetime import datetime, timedelta


def signup(username, password):
    # Flaw 4 (A02): Instead of creating a securely hashed password using a cryptographic library, passwords are saved to database as plain text. This is a very bad practice and violates data protection.
    # Fix: Instead of saving passwords to db in plain text, a proper cryptographic algorithm is used to generate a hash for the password, which is then saved to db and checked against when signing in. To implement fix, comment out lines 10, 15 and 45 and remove line 44
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
    sql = "SELECT user_id, password, failed_attempts, locked_until FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username": username})
    user = result.fetchone()

    # Flaw 5 (A07): There is no rate limiting or cooldown period on login, allowing endless attempts to try to log in.
    # Fix: implement a check for login attempts. If user has tried five times, they will experience a cooldown period of 10 minutes before they can retry, and are given a suitable response status for too many requests.
    # To fix, comment out lines 36-40, 45-46 and 53-60

    if user:
        # attempt = datetime.now()

        # if user.locked_until:
        #    unlock_time = datetime.fromisoformat(user.locked_until)
        #    if attempt < unlock_time:
        #        abort(
        #            429, description="Too many failed attempts. Please try again later.")

        if user.password == password:
            # if check_password_hash(user.password, password):

            # db.session.execute("UPDATE users SET failed_attempts = 0, locked_until = NULL WHERE user_id = :id", {"id": user.user_id})
            # db.session.commit()

            session["user_id"] = user.user_id
            session["username"] = username
            session["csrf_token"] = secrets.token_hex(16)
            return True
        else:
            # new_attempts = user.failed_attempts + 1
            # lock_time = None
            # if new_attempts >= 5:
            #    lock_time = (attempt + timedelta(minutes=10)).isoformat()

            # db.session.execute("UPDATE users SET failed_attempts = :attempts, locked_until = :lock WHERE user_id = :id",
            #                   {"attempts": new_attempts, "lock": lock_time, "id": user.user_id})
            # db.session.commit()
            return False
    return False


def logout():
    del session["user_id"]
    del session["username"]
    del session["csrf_token"]


def user_id():
    return session.get("user_id", 0)
