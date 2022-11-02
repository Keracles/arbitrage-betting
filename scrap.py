from bookmakers import unibet, betclic, winamax, zebet, netbet


bookmakers = [unibet, betclic, winamax, zebet, netbet]



def get_foot_bookmakers(bookmaker):
    bookmaker_dict = {}
    for name_league, pattern in bookmaker.pattern_foot.items() :
            print(name_league)
            bookmaker_dict[name_league] = bookmaker.get_league_matches(pattern)
    return bookmaker_dict


def get_foot():
    bet_bible = {}
    for bookmaker in bookmakers :
        if bookmaker == winamax :
            bet_bible[str(bookmaker)] = get_foot_bookmakers(bookmaker)
    return bet_bible

