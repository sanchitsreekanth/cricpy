"""
Module contains database related functionality
"""
import logging
from pathlib import Path
import sqlite3
from os.path import join


class DBUtils:
    """
    Class that contains methods for database operations
    """
    LOGGER = logging.getLogger("DBUtils")
    DB_PATH = join(Path(__file__).parents[1].absolute(), "data")
      
    @classmethod
    def initiliase_database(cls, db_name:str):
        """
        Create the database with name specified by db_name and create the tables
        Args:
            db_name (str): Name of the database to create
        """
        sqlite3.connect(join(cls.DB_PATH,db_name))
        cls.LOGGER.info("Connecting to database: %s" % db_name)
        