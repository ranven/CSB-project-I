from sqlalchemy import text
from flask import session
from services.db import db
import services.auth as auth


def create_profile():
    user_id = auth.user_id()
    sql = "INSERT INTO profiles (user_id) VALUES (:user_id)"
    db.session.execute(sql, {"user_id": user_id})
    db.session.commit()


def get_profile(user_id):
    if user_id == 0:
        return False
    sql = "SELECT p.description, p.country, p.created_at, u.username FROM profiles p JOIN users u ON p.user_id = u.user_id WHERE u.user_id = :user_id"
    result = db.session.execute(sql, {"user_id": user_id})
    profile = result.fetchone()
    return profile


def update_profile(description, country):
    user_id = auth.user_id()
    if user_id == 0:
        return False

    # Flaw 3 (A03): Using a python f-string provides a SQL injection opportunity, as user-written parameters are directly passed to the SQL query. This allows executing unauthorized queries when user profile is updated in the frontend.
    db.session.execute(
        f"UPDATE profiles SET description='{description}', country='{country}' WHERE user_id = {user_id}")

    # Fix: To fix this, the update clause needs to use secure parameters that are passed rather than "joined" to the SQL query and executed as code. This way, the database treats the user-input parameters as strings to save to the table rather than SQL to execute. The following lines implement this parameterization
    # sql = text("UPDATE profiles SET description=:description, country=:country WHERE user_id =:user_id")
    # db.session.execute(sql, {"description": description, "country": country, "user_id": user_id})

    db.session.commit()
    return True
