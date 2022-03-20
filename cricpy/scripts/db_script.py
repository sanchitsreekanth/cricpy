import click
from cricpy.constants.commons import CommonConstants, URLConstants
from cricpy.utils.db import DBUtils
from cricpy.utils.parser import Parser


@click.group()
def db():
    """Group for db cli commands"""
    pass


@db.command()
def create():
    """Command to create a blank database without any information"""
    for table_name, query in CommonConstants.TABLE_INFO.items():
        DBUtils.create_table(table_name, query)
        print(f"Created table {table_name}")


@db.command()
def init():
    """Initialise the database with match data for all tables"""
    rows = []
    for series_id, year in URLConstants.SERIES_IDS.items():
        match_names = Parser.parser_match_names_from_series(series_id)
        for match_name in match_names:
            match_id = int(match_name.split("-")[-1])
            rows.append((match_id, match_name, series_id, year))
    DBUtils.insert_to_table(table_name="match_id", rows=rows)
