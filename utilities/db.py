import sqlite3
import logging

# Project imports
from constants import config
from utilities.seed_data import camp_data, camp_resource_data, plan_data, user_data


def reset_db() -> None:
    logging.debug("Resetting database")
    run_query("DROP TABLE IF EXISTS User;")
    run_query("DROP TABLE IF EXISTS Plan;")
    run_query("DROP TABLE IF EXISTS Camp;")
    run_query("DROP TABLE IF EXISTS CampResources;")


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(config.DATABASE_NAME)
    conn.execute("PRAGMA foreign_keys = ON")  # foreign key constraint
    return conn


def run_query(query: str = "") -> None:
    """Simply runs a query which does not produce output."""
    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(query)

    conn.commit()
    conn.close()


def run_query_get_rows(query: str = "") -> list[dict]:
    """Runs query and returns rows as list of dictionaries."""
    conn = get_connection()

    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute(query)

    records = [dict(item) for item in cursor.fetchall()]

    conn.commit()
    conn.close()

    return records


def insert_query_with_values(query: str, values: dict) -> None:
    """Inserts values into db."""
    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(query, values)

    conn.commit()
    conn.close()


def create_and_seed_user_table() -> None:
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
    for user in user_data:
        logging.debug(f'Creating User {user["username"]}')

        insert_query_with_values(
            query="""INSERT INTO User 
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
            values={
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


def create_and_seed_plan_table() -> None:
    logging.debug("Creating Plan table")
    run_query(
        """CREATE TABLE `Plan` (
            `id` INTEGER PRIMARY KEY,
            `title` TEXT,
            `description` TEXT,
            `location` TEXT,
            `start_datetime` TEXT,
            `end_datetime` TEXT DEFAULT NULL,
            `central_email` TEXT,
            `affected_estimate` INT
            );"""
    )
    logging.debug("Done!")

    logging.debug("Seeding Plan table")
    for plan in plan_data:
        logging.debug(f'Creating plan {plan["title"]}')

        insert_query_with_values(
            query="""INSERT INTO Plan 
                  (
                    title,
                    description,
                    location,
                    start_datetime,
                    end_datetime,
                    central_email
                      ) VALUES (
                      :title, 
                      :description, 
                      :location, 
                      :start_datetime, 
                      :end_datetime, 
                      :central_email
                  );
                  """,
            values={
                "title": plan["title"],
                "description": plan["description"],
                "location": plan["location"],
                "start_datetime": plan["start_datetime"],
                "end_datetime": plan["end_datetime"],
                "central_email": plan["central_email"],
            },
        )


def create_and_seed_camp_table() -> None:
    logging.debug("Creating Camp table")
    run_query(
        """CREATE TABLE `Camp` (
        `id` INTEGER PRIMARY KEY,
        `name` TEXT,
        `location` TEXT,
        `maxCapacity` INT,
        `plan_id` INT, 
        FOREIGN KEY (plan_id) REFERENCES Plan (id) 
        ON DELETE CASCADE
        ON UPDATE CASCADE
        );"""
    )
    logging.debug("Done!")

    logging.debug("Seeding Camp table")
    for camp in camp_data:
        logging.debug(f'Creating Camp {camp["name"]} for Plan {camp["plan_id"]}')

        insert_query_with_values(
            query="""INSERT INTO Camp 
                  (
                    name,
                    location,
                    maxCapacity,
                    plan_id
                      ) VALUES (
                      :name, 
                      :location, 
                      :maxCapacity, 
                      :plan_id
                  );
                  """,
            values={
                "name": camp["name"],
                "location": camp["location"],
                "maxCapacity": camp["maxCapacity"],
                "plan_id": camp["plan_id"],
            },
        )


def create_and_seed_camp_resources_table() -> None:
    logging.debug("Creating CampResources table")
    run_query(
        """CREATE TABLE `CampResources` (
        `id` INTEGER PRIMARY KEY,
        `name` TEXT,
        `amount` TEXT,
        `camp_id` INT, 
        FOREIGN KEY (camp_id) REFERENCES Camp (id) 
        ON DELETE CASCADE
        ON UPDATE CASCADE
        );"""
    )
    logging.debug("Done!")

    logging.debug("Seeding CampResources table")
    for camp_resource in camp_resource_data:
        logging.debug(
            f'Creating CampResources {camp_resource["name"]} for Camp {camp_resource["camp_id"]}'
        )

        insert_query_with_values(
            query="""INSERT INTO CampResources 
                  (
                    name,
                    amount,
                    camp_id
                      ) VALUES (
                      :name, 
                      :amount, 
                      :camp_id
                  );
                  """,
            values={
                "name": camp_resource["name"],
                "amount": camp_resource["amount"],
                "camp_id": camp_resource["camp_id"],
            },
        )


def setup_db(reset_database=True) -> None:
    """Creates and seeds tables."""

    if reset_database:
        reset_db()

    create_and_seed_user_table()
    create_and_seed_plan_table()
    create_and_seed_camp_table()
    create_and_seed_camp_resources_table()
