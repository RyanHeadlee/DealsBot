from details import (
    init_search,
    get_best_offers_official,
    get_best_offers_unofficial,
    format_offer_string,
)
import discord
from discord import Intents
from discord.ext import commands
import asyncio

intents = Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="$", intents=intents)


# ex. $deal hades || $deal Call of Duty
@bot.command()
async def deal(ctx, *, game_name):
    await ctx.send("Searching for deals for {}".format(game_name))

    # Get first five links and titles
    links, titles_to_display = init_search(game_name)

    # Get formatted list of the game titles
    games_list = "\n".join(
        "{}. {}".format(i + 1, title) for i, title in enumerate(titles_to_display)
    )
    # Print the game titles on discord
    await ctx.send(
        "Found the following games: \n{}\nPlease select a game by typing its number (1-{}):".format(
            games_list, len(titles_to_display)
        )
    )

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    try:
        # Get user input from game list
        user_choice = await bot.wait_for("message", check=check, timeout=60)
        index = int(user_choice.content) - 1

        # Index must be in range between 1 and length of the links found (max 5)
        if index < 0 or index >= len(links):
            await ctx.send("Invalid selection.")
            return
        selected_game = links[index]

        # Get best offers from official and unofficial storefronts
        shop_names_of, game_names_of, prices_of, links_of = get_best_offers_official(
            selected_game
        )
        shop_names_uof, game_names_uof, prices_uof, links_uof = (
            get_best_offers_unofficial(selected_game)
        )

        # Check if any offers were found, if so print offers to discord
        if len(shop_names_of) != 0:
            official_formatted = format_offer_string(
                shop_names_of, game_names_of, prices_of, links_of
            )
            await ctx.send(
                "**Best Offers From Official Storefronts:**\n{}".format(
                    official_formatted
                )
            )

        # Check if any offers were found, if so print offers to discord
        if len(shop_names_uof) != 0:
            unofficial_formatted = format_offer_string(
                shop_names_uof, game_names_uof, prices_uof, links_uof
            )
            await ctx.send(
                "**Best Offers From Unofficial Storefronts:**\n{}".format(
                    unofficial_formatted
                )
            )

        # If both offers are unavailable, print No Offers Available to discord
        if (len(shop_names_uof) <= 0) & (len(shop_names_of) <= 0):
            await ctx.send("No Offers Available")
    except asyncio.TimeoutError:
        await ctx.send("Timed Out")
    except ValueError:
        await ctx.send("Invalid Selection")


bot.run("MTIzNzgzNjA5NTIyMDA5MzA0Mg.GcxgFb.tMVKdSUEiwhWhb6MMP9zHF5sztxWmo2oaIY1fU")
