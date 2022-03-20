import logging
from os import path
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from cricpy.constants.commons import CommonConstants, URLConstants
from cricpy.utils.commons import Utils


class Parser(object):
    """Class for parsing match data including stats and scorecards
    """

    LOGGER = logging.getLogger(__name__)
    SERIES_URL = urljoin(URLConstants.BASE_URL, URLConstants.SERIES_URL)

    @classmethod
    def get_soup_object_from_url(cls, url, parser: str = "lxml"):
        """Get soup object from a url that can be used in BeautifulSoup

        Args:
            url (string): URL of the page to be parsed

        Returns:
            [BeautifulSoup]: Soup object of the url
        """
        page = requests.get(url)
        return BeautifulSoup(page.content, parser)

    @classmethod
    def parser_match_names_from_series(cls, series_id):
        """Get the match names from ESPN Cricinfo for a series with id 'series_id'

        Args:
            series_id (string): Series id of the series
        """
        match_names = []
        URL = f"{cls.SERIES_URL}/{series_id}/match-results"
        soup = cls.get_soup_object_from_url(url=URL)
        for element in soup.find_all(
            "a", class_=URLConstants.SERIES_MATCH_URL_CLASS_NAME
        ):
            match_name = element["href"].split("/")[3]
            match_names.append(match_name)
        return match_names

    @classmethod
    def get_teams_from_soup(cls, soup):
        """Get the teams playing the match from soup object

        Args:
            soup (BeautifulSoup): bs4 object

        Returns:
            tuple: Tuple containing teams playing the match
        """
        return (i.text for i in soup.find_all(class_="name-detail"))

    @classmethod
    def get_teams_innings_score_from_soup(cls, soup):
        """Get innings score for each team playing the match

        Args:
            soup (BeautifulSoup): bs4 object

        Returns:
            tuple: Tuple containing innings score of teams playing the match
        """
        scores = [i.text for i in soup.find_all("span", class_="score")]
        if len(scores) == 1:
            return (scores[0], None)
        elif len(scores) == 0:
            return (None, None)
        return tuple(scores)

    @classmethod
    def get_winner_from_status(cls, status):
        """Get the result of the match from the match 'status'

        Args:
            status (string): Status of the match as given in cricinfo status card

        Returns:
            tuple: Tuple conatining the (winner,status) of the match
        """
        if "won by" in status:
            return tuple([i.strip() for i in status.split("won by")])
        else:
            return (None, None)

    @classmethod
    def get_match_summary_card(cls, soup):
        """Get the summary card of the match

        Args:
            soup (BeautifulSoup): bs4 object

        Returns:
            Union(BeautifulSoup,None): Match summary card as bs4 object if exists else None
        """
        match_summary = soup.find_all("tbody")
        for index, table in enumerate(match_summary):
            table_data = table.find_all("tr")[1].find("td").text
            if table_data == "Toss":
                return match_summary[index].find_all("tr")
        return None

    @classmethod
    def get_innings_details(cls, soup: BeautifulSoup):
        """Returns the innings details of a match

        Args:
            soup (BeautifulSoup): bs4 object
        """
        first_innings, second_innings = cls.get_teams_from_soup(soup)
        (
            first_innings_score,
            second_innings_score,
        ) = cls.get_teams_innings_score_from_soup(soup)
        return first_innings, second_innings, first_innings_score, second_innings_score

    @classmethod
    def get_runs_per_over(cls, series_id, match_id):
        """Returns an array containing the runs scored in each over of an innings

        Args:
            series_id (string): Series id
            match_id (string): Match id

        Returns:
            Tuple: Tuple containing the rpos of each innings as an array
        """
        url = path.join(
            URLConstants.BASE_URL,
            f"{URLConstants.SERIES_URL}/{series_id}/{match_id}/match-statistics",
        )
        soup = cls.get_soup_object_from_url(url=url)

        over_details = soup.find_all(
            "g", class_="rv-xy-plot__series rv-xy-plot__series--bar"
        )
        if not over_details:
            return (None, None)
        max_runs = int(
            soup.find("g", class_="rv-xy-plot__axis rv-xy-plot__axis--vertical")
            .find_all("text", class_="rv-xy-plot__axis__tick__text")[-1]
            .text
        )
        height_array = soup.find(
            "g", class_="rv-xy-plot__grid-lines undefined"
        ).find_all("line")
        max_height = height_array[0]["y1"]
        min_height = height_array[-1]["y1"]
        height = int(max_height) - int(min_height)
        first_innings_over_details = over_details[0].find_all("rect")
        first_innings_runs = [
            int((float(ele["height"]) / float(height)) * max_runs)
            for ele in first_innings_over_details[1:]
        ]
        if len(over_details) == 2:
            second_innings_over_details = over_details[1].find_all("rect")
            second_innings_runs = [
                int((float(ele["height"]) / float(height)) * max_runs)
                for ele in second_innings_over_details[1:]
            ]
        else:
            second_innings_runs = None
        return first_innings_runs, second_innings_runs

    @classmethod
    def get_fall_of_wickets(cls, series_id, match_id):
        """Returns tuple cintaining fow and over of fow for both innings

        Args:
            series_id (string): Series id
            match_id (string): Match id

        Returns:
            Tuple: (fow_innings_1,fow_innings_2,fow_over_innings_1,fow_over_innings_2)
        """
        url = path.join(
            URLConstants.BASE_URL,
            f"{URLConstants.SERIES_URL}/{series_id}/{match_id}/full-scorecard",
        )
        soup = cls.get_soup_object_from_url(url=url)
        table = soup.find_all("tfoot")
        if not table:
            return None, None, None, None
        first_innings_fow_details =table[0].find_all("td")[5].find_all("span")
        fow_1, fow_overs_1 = cls._get_fow_from_array(first_innings_fow_details)
        if len(table) == 2:
            second_innings_fow_details =table[1].find_all("td")[5].find_all("span")
            fow_2, fow_overs_2 = cls._get_fow_from_array(second_innings_fow_details)
        else:
            fow_overs_2 = fow_2 = None
        return fow_1, fow_2, fow_overs_1, fow_overs_2

    @classmethod
    def _get_fow_from_array(cls, fow_details_array):
        fow = []
        fow_overs = []
        for line in fow_details_array:
            split_text = line.get_text().replace(",", "").strip().split()
            fow.append(split_text[0])
            fow_overs.append(split_text[-2])
        return fow, fow_overs

    @classmethod
    def parse_match_info(cls, series_id, match_id):
        """Returns a JSON object containing match details and summary

        Args:
            series_id (string): Series id
            match_id (string): Match id

        Raises:
            Exception: If no match data is found

        Returns:
            Dict: Dictionary containing the match data including innings details, result, venue etc
        """
        response_dict = CommonConstants.MATCH_DATA_RESPONSE_DATA.copy()
        url = path.join(
            URLConstants.BASE_URL,
            f"{URLConstants.SERIES_URL}/{series_id}/{match_id}/full-scorecard",
        )
        soup = cls.get_soup_object_from_url(url=url)
        match_summary_card = cls.get_match_summary_card(soup)
        if match_summary_card is None:
            raise Exception(
                f"No match summary card found for match of ({series_id}, {match_id})"
            )

        match_summary_card = [
            [j.text for j in i.find_all("td")] for i in match_summary_card
        ]
        fow_1, fow_2, fow_overs_1, fow_overs_2 = cls.get_fall_of_wickets(
            series_id=series_id, match_id=match_id
        )
        rpo_1, rpo_2 = cls.get_runs_per_over(series_id, match_id)
        venue = match_summary_card[0][0].split(",")[0].strip().replace("'", "")
        city = match_summary_card[0][0].split(",")[-1].strip()
        match_date, toss, man_of_the_match = None, None, None
        for element in match_summary_card:
            if element[0] == "Toss":
                toss = element[1].split(",")[0].strip()
            elif "Match day" in element[0]:
                match_date = element[1].split("-")[0].strip()
            elif "Player Of The Match" in element[0]:
                man_of_the_match = element[1]
        match_result_card = soup.find(
            class_="match-info match-info-MATCH match-info-MATCH-half-width"
        )
        if not match_result_card:
            match_result_card = soup.find(
                class_="match-info match-info-MATCH match-info-MATCH-full-width"
            )
        result_text = match_result_card.find("div", class_="status-text").text
        winner, status = cls.get_winner_from_status(result_text)
        (
            first_innings,
            second_innings,
            first_innings_score,
            second_innings_score,
        ) = cls.get_innings_details(soup=match_result_card)
        result = {
            "venue": venue,
            "first_innings": Utils.get_team_symbol(first_innings),
            "second_innings": Utils.get_team_symbol(second_innings),
            "first_innings_score": first_innings_score,
            "second_innings_score": second_innings_score,
            "city": city,
            "mom": man_of_the_match,
            "toss": Utils.get_team_symbol(toss),
            "status": status,
            "winner": winner,
            "match_date": match_date,
            "rpo_1": rpo_1,
            "rpo_2": rpo_2,
            "fow_1": fow_1,
            "fow_2": fow_2,
            "fow_overs_1": fow_overs_1,
            "fow_overs_2": fow_overs_2,
        }
        response_dict.update(result)
        return response_dict
