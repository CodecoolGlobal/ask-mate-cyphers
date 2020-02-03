from typing import List, Dict
from psycopg2 import sql
from psycopg2.extras import RealDictCursor
import database_comman


@database_comman.connection_handler
def db_mod_with_return(cursor: RealDictCursor, query) -> list:
    cursor.execute(query)
    return cursor.fetchall()


@database_comman.connection_handler
def db_mod_without_return(cursor: RealDictCursor, query):
    cursor.execute(query)
