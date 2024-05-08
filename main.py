from details import init_search, get_best_offers_official, get_best_offers_unofficial


def print_offers(shop_names, game_names, prices, links):
    for i, (shop_name, game_name, price, link) in enumerate(
        zip(shop_names, game_names, prices, links)
    ):
        print(
            '{}. | {} | "{}" - {} | {} |'.format(
                i + 1, shop_name, game_name, price, link
            )
        )


def main():
    search_for = input()
    print()

    links_to_display, titles_to_display = init_search(search_for)

    for i, title in enumerate(titles_to_display):
        print("{}. {}".format(i + 1, title))
    search_for = int(input())
    search_for = links_to_display[search_for - 1]

    shop_names_of, game_names_of, prices_of, links_of = get_best_offers_official(
        search_for
    )
    shop_names_uof, game_names_uof, prices_uof, links_uof = get_best_offers_unofficial(
        search_for
    )
    print("\nThe Best Offers From Official Storefronts:")
    print_offers(shop_names_of, game_names_of, prices_of, links_of)
    print("\nThe Best Offers From Unofficial Storefronts:")
    print_offers(shop_names_uof, game_names_uof, prices_uof, links_uof)


main()
