import sqlite3
import logging

# Project imports
from constants import config
from utilities.seed_data import users


def run_query(query: str = ""):
    conn = sqlite3.connect(config.DATABASE_NAME)

    cursor = conn.cursor()

    cursor.execute(query)

    conn.commit()
    conn.close()


def setup_db() -> None:
    """Creates and seeds tables."""

    logging.debug("Cleaning database.")
    run_query("DROP TABLE IF EXISTS User;")

    # FIXME: CHANGE `camp_id` to FK
    logging.debug("Creating User table")
    run_query(
        """CREATE TABLE User (
            id INTEGER PRIMARY KEY,
            username TEXT,
            password TEXT,
            dob TEXT,
            sex TEXT,
            phone_number TEXT,
            is_active BOOL DEFAULT True,
            is_admin BOOL DEFAULT False,
            camp_id INT DEFAULT NULL
        )"""
    )
    logging.debug("Done!")

    logging.debug("Seeding User table")
    for user in users.user_data:
        logging.debug(f'Creating User {user["username"]}')
        conn = sqlite3.connect(config.DATABASE_NAME)

        cursor = conn.cursor()

        cursor.execute(
            """INSERT INTO User 
                  (username, 
                      password, 
                      dob,
                      sex,
                      phone_number,
                      is_active,
                      is_admin,
                      camp_id
                      ) VALUES (
                      :username, 
                      :password, 
                      :dob,
                      :sex,
                      :phone_number,
                      :is_active,
                      :is_admin,
                      :camp_id
                  );
                  """,
            {
                "username": user["username"],
                "password": user["password"],
                "dob": user["dob"],
                "sex": user["sex"],
                "phone_number": user["phone_number"],
                "is_active": user["is_active"],
                "is_admin": user["is_admin"],
                "camp_id": user["camp_id"],
            },
        )
        conn.commit()
        conn.close()
