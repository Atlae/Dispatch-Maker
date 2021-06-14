import requests
from bs4 import BeautifulSoup
from colorama import Fore, Back, Style

def update(USERNAME, PASSWORD, TEXT):
    username = USERNAME.lower().replace(" ", "_")

    url = "https://www.nationstates.net/cgi-bin/api.cgi"

    headers = {
        'user-agent': f"Owner Report (dev. Atlae) (in use by {username})".format(USERNAME),
        'X-Password': PASSWORD,
        }

    # Dispatch stuff
    title = "{}'s Cards Owner Report".format(USERNAME)

    data = {
        'nation': username,
        'c': 'dispatch',
        'dispatch': 'add',
        'title': title,
        'text': TEXT,
        'category': '3',
        'subcategory': '305',
        'mode': 'prepare'
    }

    params = {
        'nation': username,
        'q': 'dispatchlist',
    }

    dispatches = requests.get(url, headers=headers, params=params)
    dispatch_list = [title.string for title in BeautifulSoup(dispatches.text, 'xml').find_all("TITLE")]
    dispatch_id_list = [dispatch.get('id') for dispatch in BeautifulSoup(dispatches.text, 'xml').find_all("DISPATCH")]

    try:
        if dispatch_list.index(title) != -1:
            data["dispatch"] = "edit"
            data["dispatchid"] = dispatch_id_list[dispatch_list.index(title)]
    except ValueError:
        pass

    respond = requests.post(url, headers=headers, data=data)
    soup = BeautifulSoup(respond.text, features='xml')
    try:
        token = soup.find('SUCCESS').string
        print(Back.GREEN + respond.text + Style.RESET_ALL)
    except:
        print("It was not a success. :(")
        print(Back.RED + respond.text + Style.RESET_ALL)
    
    pin = respond.headers["X-Pin"]
    autologin = respond.headers["X-Autologin"]
    headers["pin"] = pin
    headers["autologin"] = autologin
    data["mode"] = 'execute'
    data["token"] = token
    print('-----------------------------')
    
    respond = requests.post(url, headers=headers, data=data)
    soup = BeautifulSoup(respond.text, features='xml')
    if len(soup.find('SUCCESS')) > 0:
        print(Back.GREEN + respond.text + Style.RESET_ALL)
    else:
        print(Back.RED + respond.text + Style.RESET_ALL)
