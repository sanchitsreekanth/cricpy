from typing import List
import logging
from os.path import join
from pathlib import Path
import csv


class Utils:
    """[summary]
    """
    
    LOGGER = logging.getLogger("DBUtils")
    CSV_PATH = join(Path(__file__).parents[1].absolute(), "data")
    
    @classmethod
    def write_data_to_csv(cls,filename,headers:List,data:List):
        """[summary]

        Args:
            filename ([type]): [description]
            headers (List): [description]
            data (List): [description]
        """
        destination = join(cls.CSV_PATH,filename)
        with open(destination, 'w', newline="") as filename:
            writer = csv.writer(filename)
            writer.writerow(headers)
            writer.writerows(data)
            print("Successfully wrote data to file: " + destination)
            
