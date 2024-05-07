import requests
from bs4 import BeautifulSoup
from collections import OrderedDict


# This function finds all the game and bundle links in a GGDeals page
# Parameters: search_for - game title to search for
# Returns: List od first five unique links that start with /game or /pack
def init_search(search_for):
    response = requests.get("https://gg.deals/search/?title=" + search_for)
    soup = BeautifulSoup(response.text, features="html.parser")

    # Finds all the links with /game or /pack
    links = soup.find_all(
        "a",
        href=lambda href: href
        and (href.startswith("/game/") or href.startswith("/pack/")),
    )

    # Add links to unique_lists then use OrderedDict to keep only unique values
    unique_links = list()
    for link in links:
        unique_links.append(link["href"])
    unique_links = list(OrderedDict.fromkeys(unique_links))

    # Raise error if no links were found
    if unique_links == []:
        raise Exception("Error: No Links found with the search parameters")

    return unique_links[:5]


def get_best_offers_official(search_for):
    response = requests.get("https://gg.deals" + search_for)
    soup = BeautifulSoup(response.text, features="html.parser")


def main():
    search_for = input()

    links_to_display = init_search(search_for)

    for i, link in enumerate(links_to_display):
        print("{}. {}".format(i + 1, link))
    search_for = int(input())
    search_for = links_to_display[search_for - 1]

    get_best_offers_official(search_for)


main()
