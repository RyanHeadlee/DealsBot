from details import init_search, get_best_offers_official, get_best_offers_unofficial


def main():
    search_for = input()

    links_to_display = init_search(search_for)

    for i, link in enumerate(links_to_display):
        print("{}. {}".format(i + 1, link))
    search_for = int(input())
    search_for = links_to_display[search_for - 1]

    shop_names_of, game_names_of, current_prices_of, links_of = (
        get_best_offers_official(search_for)
    )
    shop_names_uof, game_names_uof, current_prices_uof, links_uof = (
        get_best_offers_unofficial(search_for)
    )
    print("\nThe best offers from official storefronts:")
    for i, (shop_name, game_name, price, link) in enumerate(
        zip(shop_names_of, game_names_of, current_prices_of, links_of)
    ):
        print(
            "{}. Storefront: {} Title: {} Price: {} Link: {}".format(
                i + 1, shop_name, game_name, price, link
            )
        )
    print("\nThe best offers from unofficial storefronts:")
    for i, (shop_name, game_name, price, link) in enumerate(
        zip(shop_names_uof, game_names_uof, current_prices_uof, links_uof)
    ):
        print(
            "{}. Storefront: {} Title: {} Price: {} Link: {}".format(
                i + 1, shop_name, game_name, price, link
            )
        )


main()
