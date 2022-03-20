import csv
import logging
from os.path import join
from pathlib import Path
from typing import List

from cricpy.constants.commons import CommonConstants


class Utils:
    """[summary]"""

    LOGGER = logging.getLogger("DBUtils")
    CSV_PATH = join(Path(__file__).parents[1].absolute(), "data")

    @classmethod
    def write_data_to_csv(cls, filename, headers: List, data: List):
        """Writes rows contained in 'data' into a csv

        Args:
            filename (string): filename of the output CSV
            headers (List): Headers of the CSV
            data (List): List containing rows, each as a List that is to be outputted as CSV
        """
        destination = join(cls.CSV_PATH, filename)
        with open(destination, "w", newline="") as filename:
            writer = csv.writer(filename)
            writer.writerow(headers)
            writer.writerows(data)
            print("Successfully wrote data to file: " + destination)

    @classmethod
    def get_team_symbol(cls, team_name):
        team_symbol = CommonConstants.TEAM_CODES.get(team_name, None)
        return team_symbol if team_symbol else team_name
