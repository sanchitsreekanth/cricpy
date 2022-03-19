"""
Module contains database related functionality
"""
import logging
from pathlib import Path
import sqlite3
from sqlite3 import Error, DatabaseError
from os import path


class DBUtils:
    """
    Class that contains methods for database operations
    """
    LOGGER = logging.getLogger("DBUtils")
    DB_PATH = path.join(Path(__file__).parents[1].absolute(), "data")
      
    @classmethod
    def create_db_connection(cls, db_name:str):
        """
        Create the database with name specified by db_name and create the tables
        Args:
            db_name (str): Name of the database to create
        """
        conn = None
        try:
            conn = sqlite3.connect(path.join(cls.DB_PATH,db_name))
            cls.LOGGER.info("Connecting to database: %s" % db_name)
            return conn
        except Error as e:
            print(e)
        return conn
    
    @classmethod
    def create_table(cls, table_name:str, query_string:str):
        """[summary]

        Args:
            table_name (str): [description]
            query_string (str, optional): [description]. Defaults to None.
        """
        cls.LOGGER.info("Creating table: %s" %table_name)
        conn = cls.create_db_connection(db_name="ipl.db")
        cursor = conn.cursor()
        try:
            cursor.execute(query_string)
            cls.LOGGER.info("SUCCESS: created table")
        except DatabaseError as e:
            print("ERROR: %s" % e)
            
    @classmethod
    def insert_to_table(cls, table_name,rows):
        conn = cls.create_db_connection(db_name="ipl.db")
        cursor = conn.cursor()
        try:
            value_length_string = "?"+ ''.join([", ?" for _ in range(len(rows[0])-1)])
            cursor.executemany(f"INSERT OR IGNORE INTO {table_name} VALUES ({value_length_string});", rows)
            conn.commit()
        except DatabaseError as e:
            print("ERROR: %s" %e)
            
    @classmethod
    def select_from_table(cls,table_name, columns:str="*"):
        conn = cls.create_db_connection(db_name="ipl.db")
        cursor = conn.cursor()
        try:
            if columns != "*":
                columns = ','.join(columns)
            cursor.execute(f"SELECT {columns} FROM {table_name};")
            return cursor.fetchall()
        except DatabaseError as e:
            print("ERROR: %s" %e)
        
        

        
        