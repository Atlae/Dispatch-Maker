# Dispatch-Maker
This Dispatch Maker v.4.0 takes an owner report (using Racoda's [owner report](https://github.com/dithpri/RCES/tree/master/owner_report)) and formats it into a BBCode dispatch.

## Process
1. The dispatch making process is now new and improved! You only need to run one program instead of three. Run `allinone.py`.
    - It may yell at you that you may need to download the [sans](https://pypi.org/project/sans/) library (by Darcania/Zephyrkul). 
        - If so, make sure that you are using a version of Python that is at least 3.6 but at most 3.8 (3.9 not included).
        - Run `pip install sans` in your command line/terminal.

2. The program will now ask for information, namely your main nation (for the API agent) and the nation you collect from. It will also ask you to enter in a custom query if you're comfortable with that.
    - If the cards you're looking for aren't queryable, you can manually add the card URLs in `cards.txt`.
    - **Sample queries**

    | What I want to search  | My query |
    | ------------- | ------------- |
    | S2 TEP cards I haven't collected | `region:the_east_pacific&!deck:s2_tep_collector` |
    | Cards with the Delegate badge at auction | `badge:delegate&auction` |
    | GIF flags *(pronounced with a hard G don't @ me)* | `flag:gif` |
    
3. Your new file should be available at `[main nation] [timestamp].tsv`, all formatted with BBCode and ready to go! Simply add this to your dispatch.
    - Make sure to credit Racoda and myself in your dispatch.
    - The next feature that will be added is to auto-generate these dispatches by the API. Stay tuned!