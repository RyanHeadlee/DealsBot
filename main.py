from details import init_search, get_best_offers_official


def main():
    search_for = input()

    links_to_display = init_search(search_for)

    for i, link in enumerate(links_to_display):
        print("{}. {}".format(i + 1, link))
    search_for = int(input())
    search_for = links_to_display[search_for - 1]

    shop_names, game_names, current_prices, links = get_best_offers_official(search_for)
    print("\nThe best offers from official storefronts:")
    for i, (shop_name, game_name, price, link) in enumerate(
        zip(shop_names, game_names, current_prices, links)
    ):
        print(
            "{}. Storefront: {} Title: {} Price: {} Link: {}".format(
                i + 1, shop_name, game_name, price, link
            )
        )


main()
