#! /usr/bin/env python3

from argparse import ArgumentParser, Namespace
from datetime import datetime
import requests

from holiday import Holiday

YEAR_NOW = datetime.now().year
API_URL = "https://date.nager.at/api/v3/PublicHolidays/"


def get_holidays(country_code: str) -> list[Holiday]:
    """Get holidays for a country.

    Returns a list of holidays for a country.
    """

    url = API_URL + str(YEAR_NOW) + "/" + country_code
    response = requests.get(url)

    holidays = [
        Holiday(
            date=datetime.strptime(holiday["date"], "%Y-%m-%d").date(),
            name=holiday["name"],
            local_name=holiday["localName"],
            country_code=country_code,
            fixed=holiday["fixed"],
            global_=holiday["global"],
        )
        for holiday in response.json()
    ]

    return holidays


def filter_holidays(
    holidays: list[Holiday], past: bool, local: bool, one: bool
) -> list[Holiday]:
    """Filter holidays.

    Returns a list of holidays filtered by the arguments provided.
    It can filter by past (returns also past holidays), local (returns also local holidays)
    and one (returns only the next holiday).
    """

    # Filter local holidays if not requested
    if not local:
        holidays = list(filter(lambda x: x.is_global(), holidays))

    # Filter past holidays if not requested
    if not past:
        holidays = list(filter(lambda x: x.date >= datetime.now().date(), holidays))

    # Filter all holidays but the next one
    if one:
        holidays = [holidays[0]]

    return holidays


def _get_args() -> Namespace:
    """Get command line arguments.

    Returns a parser object with the command line arguments.
    """

    parser = ArgumentParser()
    parser.add_argument(
        "-c",
        "--country_code",
        help="Country code.",
        default="ES",
        type=str,
        required=False,
    )
    parser.add_argument(
        "-1",
        "--one",
        help="Show only the next holiday. By default, all holidays are shown.",
        action="store_true",
    )
    parser.add_argument(
        "-l",
        "--local",
        help="Show also local holidays. By default, only global holidays are shown.",
        default=False,
        action="store_true",
    )
    parser.add_argument(
        "-p",
        "--past",
        help="Show also past holidays. By default, only future holidays are shown.",
        default=False,
        action="store_true",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = _get_args()

    # Get country code
    cc = args.country_code
    if not cc:
        print("No country code provided. Please provide a country code.")
        cc = input("> ")

    all_holidays = get_holidays(cc)

    # Filter holidays to display only the ones requested
    filtered_holidays = filter_holidays(all_holidays, args.past, args.local, args.one)

    # Print holidays
    for holiday in filtered_holidays:
        print(holiday)
