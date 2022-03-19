from cricpy.constants.commons import URLConstants
from cricpy.utils.db import DBUtils
from cricpy.utils.parser import Parser


a=DBUtils.select_from_table(table_name="match_id", columns=["series_id", "match_name"])



Parser.get_fall_of_wickets('ipl-2021-1249214', 'mumbai-indians-vs-royal-challengers-bangalore-1st-match-1254058')


def insert_to_match_id_table():
    rows = []
    for series_id,year in URLConstants.SERIES_IDS.items():
        ret = Parser.parser_match_ids_from_series(series_id)
        for match_name in ret:
            match_id = int(match_name.split('-')[-1])
            rows.append((match_id, match_name, series_id, year))
    DBUtils.insert_to_table(table_name="match_id", rows=rows)


Parser.get_fall_of_wickets('pepsi-indian-premier-league-2015-791129', 'royal-challengers-bangalore-vs-rajasthan-royals-29th-match-829763')
Parser.get_fall_of_wickets('indian-premier-league-2012-520932', 'royal-challengers-bangalore-vs-chennai-super-kings-34th-match-548340')
Parser.get_fall_of_wickets('indian-premier-league-2011-466304', 'delhi-daredevils-vs-pune-warriors-68th-match-501265')
Parser.get_fall_of_wickets('ipl-2017-1078425', 'royal-challengers-bangalore-vs-sunrisers-hyderabad-29th-match-1082619')