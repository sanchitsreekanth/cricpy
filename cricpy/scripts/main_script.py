import click
from .db_script import db

@click.group()
def cricpy_main():
    """Main group function cricpy cli commands
    """
    pass

cricpy_main.add_command(db)