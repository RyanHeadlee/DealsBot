import requests
from bs4 import BeautifulSoup, Tag
from collections import OrderedDict
from urllib.parse import urljoin


# This function finds all the game and bundle links in a GGDeals page
# Parameters: search_for - game title to search for
# Returns: List of first five unique links that start with /game or /pack,
# and List of first five titles
def init_search(search_for: str) -> tuple[list, list]:
    response = requests.get("https://gg.deals/search/?title=" + search_for)
    soup = BeautifulSoup(response.text, features="html.parser")

    # Finds all the links with /game or /pack or div with title
    data = soup.find_all(
        "a",
        class_="game-info-title title",
        href=lambda href: href
        and (href.startswith("/game/") or href.startswith("/pack/")),
    )

    # Add links to unique_lists then use OrderedDict to keep only unique values
    # Add titles to unique_titles, should match w/ unique_lists
    unique_links, unique_titles = [], []
    for dat in data:
        unique_links.append(dat["href"])
        unique_titles.append(dat.attrs.get("data-title-multiline-auto-hide"))
    unique_links = list(OrderedDict.fromkeys(unique_links))

    return unique_links[:5], unique_titles[:5]


# This function extracts all the information from the div
# Parameters: store_div: div for either official or unofficial
# Returns: lists of the shop names, game names, prices, and links to the storefront
def get_details(store_div: Tag) -> tuple[list, list, list, list]:
    shop_names, game_names, current_prices, links = [], [], [], []
    game_details = store_div.find_all(
        "div",
        class_=lambda c: c
        and c.startswith(
            "relative hoverable-box d-flex flex-wrap flex-align-center game-item cta-full item game-deals-item game-list-item keep-unmarked-container"
        ),
    )
    for game_detail in game_details:
        if isinstance(game_detail, Tag):
            # Extract the attributes
            shop_name = game_detail.attrs.get("data-shop-name")
            game_name = game_detail.attrs.get("data-game-name")
            current_price = game_detail.find(
                "span", class_="price-inner game-price-current"
            ).text
            link = game_detail.find("a", class_="full-link")["href"]
            link = urljoin("https://gg.deals", link)

            # Append the attributes
            game_names.append(game_name)
            shop_names.append(shop_name)
            current_prices.append(current_price)
            links.append(link)

    return shop_names, game_names, current_prices, links


# This function gets all the important information about the searched game (Official)
# Parameters: search_for: link chosen to enter
# Returns: lists of the shop names, game names, prices, and links to the storefront
def get_best_offers_official(search_for: str) -> tuple[list, list, list, list]:
    response = requests.get("https://gg.deals" + search_for)
    soup = BeautifulSoup(response.text, features="html.parser")
    official_stores_div = soup.find("div", id="official-stores")

    if official_stores_div:
        shop_names, game_names, current_prices, links = get_details(official_stores_div)
    else:
        raise Exception("Error: Official Store div could not be found")

    return shop_names, game_names, current_prices, links


# This function gets all the important information about the searched game (Unofficial)
# Parameters: search_for: link chosen to enter
# Returns: lists of the shop names, game names, prices, and links to the storefront
def get_best_offers_unofficial(search_for: str) -> tuple[list, list, list, list]:
    response = requests.get("https://gg.deals" + search_for)
    soup = BeautifulSoup(response.text, features="html.parser")
    unofficial_stores_div = soup.find("div", id="keyshops")

    if unofficial_stores_div:
        shop_names, game_names, current_prices, links = get_details(
            unofficial_stores_div
        )
    else:
        raise Exception("Error: Unofficial Store div could not be found")

    return shop_names, game_names, current_prices, links


# This function formats the offers into a readable string
# Params: the details of the offers
# Returns: the formatted string
def format_offer_string(
    shop_names: list, game_names: list, prices: list, links: list
) -> str:
    formatted_offer = ""
    for i, (shop_name, game_name, price, link) in enumerate(
        zip(shop_names, game_names, prices, links)
    ):
        formatted_offer += '{}. | {} | "{}" - {} | <{}> |\n'.format(
            i + 1, shop_name, game_name, price, link
        )

    return formatted_offer
