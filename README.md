# Dispatch-Maker
This Dispatch Maker takes an owner report (using Racoda's [owner report](https://github.com/dithpri/RCES/tree/master/owner_report)) and formats it into a BBCode dispatch.

## Process
1. Run `query.py` to create a list of cards to find the owners of.
    - If the cards you're looking for aren't queryable, you can manually add the card URLs in `query_links.txt`.
    - **Sample queries**

    | What I want to search  | My query |
    | ------------- | ------------- |
    | S2 TEP cards I haven't collected | `region:the_east_pacific&!deck:s2_tep_collector` |
    | Cards with the Delegate badge at auction | `badge:delegate&auction` |
    | GIF flags *(pronounced with a hard G don't @ me)* | `flag:gif` |
         
2. Run `owner_report.py`.
    - It may yell at you that you may need to download the [sans](https://pypi.org/project/sans/) library (by Darcania/Zephyrkul). 
        - If so, make sure that you are using a version of Python that is at least 3.6 but at most 3.8 (3.9 not included).
        - Run `pip install sans` in your command line/terminal.
    - Select [2] to search the cards that were just queried.
        - [1] or [3] would also search the cards in the decks of the puppets you listed.
    
3. Run `bbcode.py` to format the output of the owner report.
    - The owner report returns a .tsv file named with a timestamp, for example `2021-04-20 11-59-59.tsv`.
    - When running `bbcode.py`, do not enter in the .tsv extension (the code does that for you) so just enter in `2021-04-20 11-59-59`, for example.

Make sure to credit Racoda and myself in your dispatch.
