# Dispatch-Maker
This Dispatch Maker v7.0 takes an owner report (using Racoda's [owner report](https://github.com/dithpri/RCES/tree/master/owner_report)) and formats it into a BBCode dispatch, using the NationStates API.

## Disclaimer
---
Please use discretion when operating Dispatch-Maker. Please be cognizant of the character limit of dispatches and the spam that dispatches create. Please refer to the [NationStates Rules](https://forum.nationstates.net/viewtopic.php?f=16&t=260044#017) regarding spam as well.
## Process
1. The dispatch making process is now new and improved! You only need to run one program instead of three. Run `run_me.py` or `run_me.bat`.
    - It may yell at you that you may need to download the [sans](https://pypi.org/project/sans/) library (by Darcania/Zephyrkul). 
        - If so, make sure that you are using a version of Python that is at least 3.6 but at most 3.8 (3.9 not included).
        - Run `pip install sans` in your command line/terminal.
        - If you do have 3.9 or an earlier version of Python, download a version of Python like 3.8 and run the following in your command prompt: `py -3.8 run_me.py` (or your version). 
          - Else, `python run_me.py` should work.
        - **IMPORTANT:** If running Dispatch-Maker from a command-line interface, it is *highly* recommended that you `cd` to the directory before running the file as follows:
          - ```C:/Users/NAME > cd C:/Users/NAME/your/path/here & python run_me.py```
          - Do not ```C:/Users/NAME > C:/Users/NAME/your/path/here/run_me.py```
            - This will result in an error if you want to input cards manually in `cards.txt` but the directory `C:/Users/NAME` does not contain `cards.txt`.
            - If you insist, create a `cards.txt` file in your `C:/Users/NAME` directory *before* running the file.
     - Alternatively, you can run `run_me.bat`. This batch file was written mostly for automation purposes such as Task Scheduler for Windows or cron for MacOS and Linux.

2. The program will now ask for information, namely the nation you collect from and its password (Note: I do **not** see the password, it is local only to your device). It will also ask you to enter in a custom query if you're comfortable with that.
   
    - If you want to collect cards across seasons, you can do so by entering `0` where it asks for the season. And of course, Season 3 does not exist.
    - If the cards you're looking for aren't queryable, you can manually add the card URLs in `cards.txt`. When it asks you to enter in a custom query leave it blank and press enter.
      - There are two ways to manually enter cards into `cards.txt`.
        - `[URL] [name]` like `https://www.nationstates.net/page=deck/card=1/season=1 testlandia` (season is optional if you want to check both seasons)
        - `[id] [name] [season]` like `1 testlandia 1`, season is also optional.
        - `{'id': '[id]', 'name': '[name]', 'season': '[season]'}` like `{'id': '1', 'name: 'testlandia', 'season': '1'}` *(not recommended)* This method ensures that if there is a pre-existing JSON list in `cards.txt`, that it would not break. The season is not optional here.
    - **Sample queries**

    | What I want to search  | My query |
    | ------------- | ------------- |
    | S2 TEP cards I haven't collected | `region:the_east_pacific&!deck:s2_tep_collector` |
    | Cards with the Delegate badge at auction | `badge:delegate&auction` |
    | GIF flags *(pronounced with a hard G don't @ me)* | `flag:gif` |

    - As of Version 7.0, Dispatch-Maker now utilizeds *argparse* so you can enter these arguments via command line.
      - Usage: 
      ```
      run_me [-h] [--u [USERNAME]] [--p [PASSWORD]] [--s [SEASON]] [--q [QUERY]]

      optional arguments:
      -h, --help      show this help message and exit
      --u [USERNAME]  Plese enter your username.
      --p [PASSWORD]  Please enter your password (only you can see it).
      --s [SEASON]    The season you want to search.
      --q [QUERY]     Please enter your query using the Advanced Cards Queries Syntax.
      ```
3. Your new file should be available at `[nation] [timestamp].txt`, all formatted with BBCode and ready to go! But that's not it! It will then use the API to create or edit a new dispatch.
    - If you'd like to add any words before the table in the dispatch, please do so in `preamble.txt`.
    - There is a character limit to dispatches. Please be cognizant about the number of cards that you want to place in a dispatch. Splitting across dispatches is an option, although not entirely recommended.
    - The next feature to be added sometime in the future is a config file so you don't always have to enter your username and password. Stay tuned!