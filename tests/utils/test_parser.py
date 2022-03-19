import pytest
from unittest import TestCase
from cricpy.utils.parser import Parser
from cricpy.constants.commons import CommonConstants


class TestParseMatchInfo(TestCase):
    
    def setUp(self):
        self.series_id = "ipl-2021-1249214"
        self.match_id = "chennai-super-kings-vs-kolkata-knight-riders-final-1254117"
        
    def test_parse_match_info_for_direct_case(self):
        response = Parser.parse_match_info(series_id=self.series_id, match_id=self.match_id)
        expected_response = {
            "mom": "Faf du Plessis",
            "venue": "Dubai International Cricket Stadium",
            "match_date":"15 October 2021",
            "first_innings":"Chennai Super Kings",
            "second_innings":"Kolkata Knight Riders",
            "first_innings_score":"192/3",
            "second_innings_score":"165/9"
        }
        d = CommonConstants.MATCH_DATA_RESPONSE_DATA.copy()
        d.update(expected_response)
        self.assertEquals(d, response)