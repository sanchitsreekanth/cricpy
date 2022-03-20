from cricpy.constants.db_constants import DBConstants


class URLConstants:
    """Constants related to URLS"""

    BASE_URL = "https://www.espncricinfo.com"
    SERIES_URL = "series"
    SERIES_IDS = {
        "ipl-2021-1249214": 2021, 
        "ipl-2020-21-1210595": 2020,
        "ipl-2019-1165643": 2019,
        "ipl-2018-1131611":2018,
        "ipl-2017-1078425":2017,
        "ipl-2016-968923":2016,
        "pepsi-indian-premier-league-2015-791129": 2015,
        "pepsi-indian-premier-league-2014-695871": 2014,
        "indian-premier-league-2013-586733": 2013,
        "indian-premier-league-2012-520932": 2012,
        "indian-premier-league-2011-466304":2011,
        "indian-premier-league-2009-10-418064":2010,
        "indian-premier-league-2009-374163":2009,
        "indian-premier-league-2007-08-313494":2008
        }
    SERIES_MATCH_URL_CLASS_NAME = "match-info-link-FIXTURES"


class CommonConstants:
    """Constants used across the module"""

    TABLE_INFO = {
        "matches": DBConstants.CREATE_MATCHES_TABLE_QUERY,
        "match_id": DBConstants.CREATE_MATCH_ID_TABLE_QUERY
        }
    
    TEAM_CODES = {
        "Chennai Super Kings":"CSK",
        "Delhi Capitals": "DC",
        "Mumbai Indians": "MI",
        "Kolkata Knight Riders": "KKR",
        "Rajasthan Royals": "RR",
        "Royal Challengers Bangalore": "RCB",
        "Sunrisers Hyderabad": "SRH",
        "Punjab Kings":"PBKS",
        "Kings XI Punjab": "PBKS",
        "Delhi Daredevils": "DC",
        "Deccan Chargers": "SRH",
        "Rising Pune Supergiants": "RPS",
        "Rising Pune Supergiant": "RPS",
        "Gujarat Lions": "GL"
    }
    
    MATCH_DATA_RESPONSE_DATA = {
        "match_id":None,
        "year":None,
        "match_number":None,
        "match_date":None,
        "venue":None,
        "city":None,
        "first_innings":None,
        "second_innings":None,
        "winner":None,
        "status":None,
        "mom":None,
        "rpo_1":None,
        "rpo_2":None,
        "fow_1":None,
        "fow_2":None,
        "fow_overs_1":None,
        "fow_overs_2":None
    }
