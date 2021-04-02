import re

"""
1. Change "	" to "[/td][td]"
2. Put [tr][td] at the front and [/list][/td][/tr] at the end of each line
3. Change ":\d," (regex) to "[/nation][*][nation]"
4. Change ":\d" (regex) to "[/nation]"
5. Change "\[\/td\]\[td\]\d*\[\/td\]\[td\]\d*\[\/td\]\[td\]\d*\[\/td\]\[td\]" (regex) to "/season=2]Link to Card[/url][/td][td][list][*][nation]"
6. Change "^\[tr\]\[td\]" (regex) to "[tr][td][url=https://www.nationstates.net/page=deck/card="
7. Change "\[\*\]\[nation\]\[\/list\]" (regex) to "[i]No owners... :([/i][/list]"

Add [table]
Add [tr][td][b]CARD LINK[/b][/td][td][b]OWNERS[/b][/td][/tr]
Add [/table] at the end
"""

list = input("Name the file you'd like to search (preferably generated using Racoda's owner report) without the .tsv extension (Example: 2069-04-20 00-01-00 unless you custom named it): ")
f = open(list + ".tsv", "r")
g = open(list + " formatted.txt", "w")
h = open("cards.txt", "r")
season = []
for card in h:
    index = re.search(r"\d$", card)
    season.append(card[index.start()])
count = 0
next(f)
g.write("[table]")
g.write("[tr][td][b]CARD LINK[/b][/td][td][b]OWNERS[/b][/td][/tr]\n[tr][td]")
for line in f:
    line = line.replace("\t", "[/td][td]")
    line = line.replace("\n", "[/list][/td][/tr]\n[tr][td]")
    line = re.sub(r":\d,", "[/nation][*][nation]", line)
    line = re.sub(r":\d", "[/nation]", line)
    line = re.sub(r"\[\/td\]\[td\]\d*\[\/td\]\[td\]\d*\[\/td\]\[td\]\d*\[\/td\]\[td\]", f"/season={season[count]}]Link to Card[/url][/td][td][list][*][nation]", line)
    line = re.sub(r"^", "[url=https://www.nationstates.net/page=deck/card=", line)
    line = re.sub(r"\[\*\]\[nation\]\[\/list\]", "[i]No owners... :([/i][/list]", line)
    count = count + 1
    g.write(line)
g.write("[i]This table was generated with the help of [nation]Racoda[/nation]'s RCES owner report, which can be found [url=https://github.com/dithpri/RCES]here.[/url] I coded a way to automate this [url=https://github.com/Atlae/Dispatch-Maker]here[/url]. -[nation]Atlae[/nation][/i][/td][/tr][/table]")

f.close()
g.close()
