from bookmakers import unibet, betclic, winamax, zebet, netbet
import sys, time
from f_annex import mail

remote = False
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

if __name__ == "__main__":
    try :
        print("lol")
    except :
        contenu = f"Unexpected error:, {sys.exc_info()[0]}"

    else :
        if remote :
            contenu = f"Le scrapping c'est bien passe a {time.localtime()}"
            mail.envoie_mail("keracles10@gmail.com", contenu)
