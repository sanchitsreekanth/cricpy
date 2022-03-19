import click
from cricpy.utils.db import DBUtils
from cricpy.constants.commons import CommonConstants


@click.group()
def db():
    """Group for db cli commands
    """
    pass

@db.command()
def create():
    """Command to create a blank database without any information
    """
    for table_name, query in CommonConstants.TABLE_INFO.items():
        DBUtils.create_table(table_name, query)
        print(f"Created table {table_name}")
