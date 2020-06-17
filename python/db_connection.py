import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def sql_create_leagues_table():
    return """ CREATE TABLE IF NOT EXISTS leagues (
                id integer PRIMARY KEY,
                name text NOT NULL,
                url text NOT NULL,
                for float NOT NULL,
                agn float NOT NULL,
                ttl float NOT NULL
            ); """

def sql_create_teams_table():
    return """CREATE TABLE IF NOT EXISTS teams (
                id integer PRIMARY KEY,
                name text NOT NULL,
                for float NOT NULL,
                agn float NOT NULL,
                ttl float NOT NULL,
                league_id integer NOT NULL,
                FOREIGN KEY (league_id) REFERENCES leagues (id)
            );"""

def create_leagues(conn, league):
    """
    Create a new task
    :param conn:
    :param task:
    :return:
    """

    sql = ''' INSERT INTO leagues(name, url, for, agn, ttl)
              VALUES(?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, league)
    return cur.lastrowid

def create_teams(conn, team):
    """
    Create a new task
    :param conn:
    :param task:
    :return:
    """

    sql = ''' INSERT INTO teams(name,for,agn,ttl,league_id)
              VALUES(?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, team)
    return cur.lastrowid