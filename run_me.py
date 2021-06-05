#!/usr/bin/env python3

"""
 * Copyright (c) 2020 dithpri (Racoda) <dithpri@gmail.com>
 * This file is part of RCES: https://github.com/dithpri/RCES and licensed under
 * the MIT license. See LICENSE.md or
 * https://github.com/dithpri/RCES/blob/master/LICENSE.md for more details.
"""

import os
import sys
import requests

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
from autodispatch import update

async def ratelimit():
    while xra := Api.xra:
        xra = xra - datetime.datetime.now().timestamp()
        eprint(f"Rate limit reached: sleeping {int(xra)} seconds...")
        await asyncio.sleep(xra)

async def main():
    version = 6.0
    print("Version No. %.1f" % version)
    username = input("What nation are you collecting from? ")
    nation = username.lower().replace(" ", "_")
    password = input("What is the password of that nation? ")
    Api.agent = f"Owner Report (dev. Atlae) (in use by {username})"
    query_season = -1
    while query_season not in [0, 1, 2, 3]:
        query_season = input("What season are you looking for? (1 or 2, 0 for both) ")
        try:
            query_season = int(query_season)
        except ValueError:
            print("That's not a number!")
    if query_season == 3:
        print("S3 will never come.")
        await asyncio.sleep(0)
        sys.exit()
    posted_query = input("Please enter your query using the Advanced Cards Queries Syntax. Leave blank if you have a list in cards.txt: ")
    custom = len(posted_query) > 0
    cards = []
    if custom:
        open("cards.txt", "w")
        if query_season != 0:
            processed_query = posted_query.replace(":", "%3A").replace("&", "%26").replace("!", "%21").replace("|", "%7C").replace(" ", "+").replace("(", "%28").replace(")", "%29")
            query = f'http://azure.nsr3n.info/card_queries/get_daemon_advanced.sh?format=full&query={processed_query}&season={query_season}&format=json&submit=submit'
            
            print('Running...accessing r3n\'s server')
            reqs = requests.get(query)
            cards = reqs.json()['cards']
            print("Finished accessing r3n\'s server")

            print("Writing the output of said query into file")
            with open('cards.txt', 'a') as f:
                for i in range(len(cards)):
                    f.write(str(cards[i]) + '\n')
        else:
            while query_season < 2:
                query_season += 1
                processed_query = posted_query.replace(":", "%3A").replace("&", "%26").replace("!", "%21").replace("|", "%7C").replace(" ", "+").replace("(", "%28").replace(")", "%29")
                query = f'http://azure.nsr3n.info/card_queries/get_daemon_advanced.sh?format=full&query={processed_query}&season={query_season}&format=json&submit=submit'
                
                print('Running...accessing r3n\'s server')
                reqs = requests.get(query)
                cards = reqs.json()['cards']
                print("Finished accessing r3n\'s server")

                print("Writing the output of said query into file")
                with open('cards.txt', 'a') as f:
                    for i in range(len(cards)):
                        f.write(str(cards[i]) + '\n')
    else:
        if not os.path.exists("cards.txt"):
            eprint("""
`cards.txt` does not exist in your directory! 
If you are listing the address in your command-line interface like this:
    C:/Users/NAME > C:/Users/NAME/your/path/here/allinone.py

Please create `cards.txt` in your C:/Users/NAME directory or `cd` to the directory (strongly recommended) like this:
    C:/Users/NAME > cd C:/Users/NAME/your/path/here & python allinone.py
            """)
            input("Press enter to continue...")
            await asyncio.sleep(0)
            sys.exit(1)
        with open("cards.txt", "r") as lines:
            linenum = 0
            for line in lines.readlines():
                linenum += 1
                if temp := re.match(r"^https?://(www\.)?nationstates.net/page=deck/card=(?P<id>[0-9]+)/?(/season=(?P<season>[0-9]+))?/?(\s+)(?P<name>\w+)", line):
                    id, season, name = temp.group("id"), temp.group("season"), temp.group("name")
                elif temp := re.match("(?P<id>[0-9]+)\s+(?P<name>\w+)(\s+(?P<season>[0-9]+))?", line):
                    id, name, season = temp.group("id"), temp.group("name"), temp.group("season")
                elif temp := re.match("{'id': '(?P<id>[0-9]+)', 'name': '(?P<name>\w+)', 'season': '(?P<season>[0-9]+)'}", line):
                    id, name, season = temp.group("id"), temp.group("name"), temp.group("season")
                else:
                    eprint(f"Unable to process line {linenum} because you put in a wrong format")
                    continue
                if season is not None:
                    cards.append({'id': id, 'name': name, 'season': season})
                else:
                    for s in range(1,3):
                        cards.append({'id': id, 'name': name, 'season': s})

    file_name = datetime.datetime.now().strftime(f"{nation} %Y-%m-%d %H-%M-%S.txt")
    with open(file_name, "x") as output_file:
        if os.path.exists("preamble.txt"):
            with open("preamble.txt", 'r') as p:
                output_file.write(p.read() + "\n")
        output_file.write("[box][i]This table was generated with the help of [nation]Racoda[/nation]'s RCES owner report, which can be found [url=https://github.com/dithpri/RCES]here.[/url] I coded a way to automate this [url=https://github.com/Atlae/Dispatch-Maker]here[/url]. -[nation]Atlae[/nation] ([nation]The Atlae Isles[/nation])[/i][/box]\n")
        output_file.write("[box][table][tr][td][b]NAME[/b][/td][td][b]CARD LINK[/b][/td][td][b]NUMBER OF OWNERS[/b][/td][td][b]NUMBER OF COPIES[/b][/td][td][b]OWNERS[/b][/td][/tr]\n")
        for card in cards:
            id = card['id']
            name = card['name']
            season = card['season']
            owners_dict = defaultdict(int)
            num_owners = 0
            num_copies = 0
            owners_copies = "[list][*][i]No owners... :([/i][/list]"
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
                owners_copies = re.sub(r":\d+,", "[/nation][*][nation]", owners_copies)
                owners_copies = re.sub(r":\d+", "[/nation]", owners_copies)
                owners_copies = "[list][*][nation]" + owners_copies + "[/list]"
            output_file.write(
                f"[tr][td]{name}[/td][td][url=https://www.nationstates.net/page=deck/card={id}/season={season}]Link to Card[/url][/td][td]{num_owners}[/td][td]{num_copies}[/td][td]{owners_copies}[/td][/tr]\n"
            )
            print(f"Added {card}")
        output_file.write("[/table][/box]")
    with open(file_name, "r") as output_file:
        update(username, password, output_file.read())

if __name__ == "__main__":
    asyncio.run(main(), debug=False)
