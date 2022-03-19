import logging
from os import path
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from cricpy.constants.commons import CommonConstants, URLConstants


class Parser(object):
    """

    Args:
        object ([type]): [description]
    """

    LOGGER = logging.getLogger(__name__)
    SERIES_URL = urljoin(URLConstants.BASE_URL, URLConstants.SERIES_URL)

    @classmethod
    def get_soup_object_from_url(cls, url, parser: str = "lxml"):
        """[summary]

        Args:
            url ([type]): [description]

        Returns:
            [type]: [description]
        """
        page = requests.get(url)
        return BeautifulSoup(page.content, parser)

    @classmethod
    def parser_match_ids_from_series(cls, series_id):
        """[summary]

        Args:
            series_id ([type]): [description]
        """
        match_ids = []
        URL = f"{cls.SERIES_URL}/{series_id}/match-results"
        soup = cls.get_soup_object_from_url(url=URL)
        for element in soup.find_all(
            "a", class_=URLConstants.SERIES_MATCH_URL_CLASS_NAME
        ):
            match_id = element["href"].split("/")[3]
            match_ids.append(match_id)
        return match_ids

    @classmethod
    def get_teams_from_soup(cls, soup):
        return (i.text for i in soup.find_all(class_="name-detail"))

    @classmethod
    def get_teams_innings_score_from_soup(cls, soup):
        scores = [i.text for i in soup.find_all("span", class_="score")]
        if len(scores) == 1:
            return (scores[0], None)
        elif len(scores) == 0:
            return (None, None)
        return tuple(scores)

    @classmethod
    def get_winner_from_status(cls, status):
        if "won by" in status:
            return tuple([i.strip() for i in status.split("won by")])
        else:
            return (None, None)

    @classmethod
    def get_match_summary_card(cls, soup):
        match_summary = soup.find_all("tbody")
        for index, table in enumerate(match_summary):
            table_data = table.find_all("tr")[1].find("td").text
            if table_data == "Toss":
                return match_summary[index].find_all("tr")
        return None

    @classmethod
    def get_innings_details(cls, soup: BeautifulSoup):
        first_innings, second_innings = cls.get_teams_from_soup(soup)
        (
            first_innings_score,
            second_innings_score,
        ) = cls.get_teams_innings_score_from_soup(soup)
        return first_innings, second_innings, first_innings_score, second_innings_score

    @classmethod
    def get_runs_per_over(cls, series_id, match_id):
        url = path.join(
            URLConstants.BASE_URL,
            f"{URLConstants.SERIES_URL}/{series_id}/{match_id}/match-statistics",
        )
        soup = cls.get_soup_object_from_url(url=url)

        over_details = soup.find_all(
            "g", class_="rv-xy-plot__series rv-xy-plot__series--bar"
        )
        if not over_details:
            return (None, None, None, None, None)
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
        print(first_innings_runs)
        print(second_innings_runs)

    @classmethod
    def parse_match_info(cls, series_id, match_id):
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
            "first_innings": first_innings,
            "second_innings": second_innings,
            "first_innings_score": first_innings_score,
            "second_innings_score": second_innings_score,
            "city": city,
            "mom": man_of_the_match,
            "toss": toss,
            "status": status,
            "winner": winner,
            "match_date": match_date,
        }
        response_dict.update(result)
        return response_dict
