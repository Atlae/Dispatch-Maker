#!/usr/bin/env python3

"""
 * Copyright (c) 2020 dithpri (Racoda) <dithpri@gmail.com>
 * This file is part of RCES: https://github.com/dithpri/RCES and licensed under
 * the MIT license. See LICENSE.md or
 * https://github.com/dithpri/RCES/blob/master/LICENSE.md for more details.
"""

import sys
import requests
from bs4 import BeautifulSoup

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)
    sys.stderr.flush()

try:
    from sans.api import Api
    from sans.utils import pretty_string
    from sans.errors import NotFound
except ImportError:
    eprint(
        """You need `sans` to run this script!
install it by running
    python3 -m pip install -U sans
or
    py -m pip install -U sans
or from https://pypi.org/project/sans/"""
    )
    input("Press enter to continue...")
    sys.exit(1)

import asyncio
import datetime
import re
from collections import defaultdict

async def ratelimit():
    while xra := Api.xra:
        xra = xra - datetime.datetime.now().timestamp()
        eprint(f"Rate limit reached: sleeping {int(xra)} seconds...")
        await asyncio.sleep(xra)

async def main():
    version = 4.0
    print("Version No. %.1f" % version)
    username = ""
    while not username:
        username = input("Please enter your (main) nation name: ")
    Api.agent = f"Owner Report (dev. Atlae) (in use by {username})"
    bidsTrue = False
    nation = input("What nation are you collecting from? ").lower().replace(" ", "_")
    query_season = 3
    while query_season not in [1, 2]:
        query_season = input("What season are you looking for? (1 or 2) ")
        try:
            query_season = int(query_season)
        except ValueError:
            print("That's not a number!")
        except query_season == 3:
            print("S3 will never come.")
    custom = input("Do you want to make your own custom query? (yes/no) ").lower().startswith('y')
    if not custom:
        region = input("What region are you searching? ").lower().replace(" ", "_")
        bids = input("Are you looking for the cards to bid on? (yes/no) ")
        if bids.lower().startswith('y'):
            bidsTrue = True

    if custom:
        posted_query = input("Please enter your query using the Advanced Cards Queries syntax: ")
        processed_query = posted_query.replace(":", "%3A").replace("&", "%26").replace("!", "%21").replace("|", "%7C").replace(" ", "+").replace("(", "%28").replace(")", "%29")
        query = f'http://azure.nsr3n.info/card_queries/get_daemon_advanced.sh?format=full&query={processed_query}&season={query_season}&format=full&submit=submit'
    elif bidsTrue:
        query = f'http://azure.nsr3n.info/card_queries/get_daemon_advanced.sh?format=full&query=region%3A{region}%26%21deck%3A{nation}%26%21bid%3A{nation}&season={query_season}&format=full&submit=submit'
    else:
        query = f'http://azure.nsr3n.info/card_queries/get_daemon_advanced.sh?format=full&query=region%3A{region}%26%21deck%3A{nation}&season={query_season}&format=full&submit=submit'

    print('Running...accessing r3n\'s server')
    reqs = requests.get(query)
    soup = BeautifulSoup(reqs.text, 'html.parser')
    print("Finished accessing r3n\'s server")

    print("Writing the output of said query into file")
    with open('cards.txt', 'w') as f:
        a = soup.find_all('a')
        for i in range(1, len(a)-1):
            f.write(a[i].get('href') + '\n')
        f.write(a[len(a)-1].get('href'))

    cards = set()
    with open("cards.txt", "r") as lines:
        linenum = 0
        for line in lines:
            linenum += 1
            if temp := re.match(r"^https?://(www\.)?nationstates.net/page=deck/card=(?P<id>[0-9]+)(/season=(?P<season>[0-9]+))?", line):
                id, season = temp.group("id"), temp.group("season")
            elif temp := re.match("(?P<id>[0-9]+)(([^0-9])+(?P<season>[0-9]+))?", line):
                id, season = temp.group("id"), temp.group("season")
            else:
                eprint(f"Unable to process line {linenum} because you put in a wrong format")
                continue
            if season:
                cards.add((id, season))
            else:
                for s in range(3):
                    cards.add((id, s))

    file_name = datetime.datetime.now().strftime(f"{nation} %Y-%m-%d %H-%M-%S.tsv")
    output_file = open(file_name, "x")
    output_file.write("[table][tr][td][b]CARD LINK[/b][/td][td][b]NUMBER OF OWNERS[/b][/td][td][b]NUMBER OF COPIES[/b][/td][td][b]OWNERS[/b][/td][/tr]\n")
    for card in cards:
        id, season = card
        owners_dict = defaultdict(int)
        num_owners = 0
        num_copies = 0
        owners_copies = "[i]No owners... :([/i]"
        await ratelimit()
        result = await Api("card owners", cardid=id, season=season)
        try:
            for owner in result.OWNERS.OWNER:
                num_copies += 1
                owners_dict[owner.text] += 1
        except AttributeError:
            if result.find("OWNERS") == None:
                eprint(f"Card {id} season {season} does not exist.")
                continue
        owners = owners_dict.keys()
        num_owners = len(owners)
        if num_owners > 0:
            owners_copies = ",".join(
                [
                    ":".join((a, str(b)))
                    for a, b in sorted(
                        owners_dict.items(), key=lambda x: x[1], reverse=True
                    )
                ]
            )
            owners_copies = re.sub(r":\d,", "[/nation][*][nation]", owners_copies)
            owners_copies = re.sub(r":\d", "[/nation]", owners_copies)
            owners_copies = "[list][*][nation]" + owners_copies + "[/list]"
        output_file.write(
            f"[tr][td][url=https://www.nationstates.net/page=deck/card={id}/season={season}]Link to Card[/url][/td][td]{num_owners}[/td][td]{num_copies}[/td][td]{owners_copies}[/td][/tr]\n"
        )
        print(f"Added {card}")
    output_file.write("[tr][td][i]This table was generated with the help of [nation]Racoda[/nation]'s RCES owner report, which can be found [url=https://github.com/dithpri/RCES]here.[/url] I coded a way to automate this [url=https://github.com/Atlae/Dispatch-Maker]here[/url]. -[nation]Atlae[/nation][/i][/td][/tr][/table]")

if __name__ == "__main__":
    asyncio.run(main())
