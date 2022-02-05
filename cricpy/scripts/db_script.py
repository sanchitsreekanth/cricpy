import click
from cricpy.commons.db_utils import DBUtils


@click.group()
def db():
    """Group for db cli commands
    """
    pass

@db.command()
def create():
    """Command to create a blank database without any information
    """
    DBUtils.initiliase_database(db_name="ipl.db")
