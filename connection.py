from typing import List, Dict
from psycopg2 import sql
from psycopg2.extras import RealDictCursor
import database_comman


@database_comman.connection_handler
def db_mod_list_with_return(cursor: RealDictCursor, query, list_of_var) -> list:
    cursor.execute(query, list_of_var)
    return cursor.fetchall()


@database_comman.connection_handler
def db_mod_list_without_return(cursor: RealDictCursor, query, list_of_var):
    cursor.execute(query, list_of_var)
