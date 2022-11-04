import sys, time, traceback, f_annex.param as param
from f_annex import mail, exceptions, surebets_finder
from bookmakers import unibet, betclic, winamax, zebet, netbet
import logging
from datetime import datetime
import requests

bookmakers = [unibet, betclic, winamax, zebet, netbet]

def get_foot_bookmakers(bookmaker):
    print(f"Début {bookmaker.bookmaker}")
    bookmaker_dict = {}
    d = len(bookmaker.pattern_foot.items())
    n = 1
    for name_league, pattern in bookmaker.pattern_foot.items() :
            if name_league == "portugal-1" or True :
                try :
                    bookmaker_dict[name_league] = bookmaker.get_league_matches(pattern, name_league)
                except exceptions.NoMatchinLeague :
                    print(f"Pour le bookmaker {bookmaker.bookmaker}, il n'y a pas de matchs trouvés pour la league {name_league}")

                except KeyboardInterrupt :
                    raise
            
                except requests.exceptions.ReadTimeout:
                    print(f"Timeout league {bookmaker.bookmaker}-{name_league}")
                
                except :
                    print(f"Erreur dans cette ligue {bookmaker.bookmaker}/{name_league} pour l'erreur {sys.exc_info()}")
                    logging.warning(f"Erreur dans cette ligue {bookmaker.bookmaker}/{name_league} pour l'erreur {sys.exc_info()}"+f"\n Traceback : {traceback.format_exc()}")
                


                print(f"{bookmaker.bookmaker} avancement : {100*n/d}%  -  League {name_league}")
                n+=1
    return bookmaker_dict


def get_foot():
    bet_bible = {}
    for bookmaker in bookmakers :
        if bookmaker == winamax or True :
            bet_bible[bookmaker.bookmaker] = get_foot_bookmakers(bookmaker)
    return bet_bible

if __name__ == "__main__":
    d = datetime.now()
    logging.basicConfig(filename=f"logs/{d.strftime('%Y-%m-%d_%H-%M')}.log", encoding='utf-8', level=logging.WARNING)
    try :
        bet_bible = get_foot()
    except :
        contenu = f"Unexpected error:, {sys.exc_info()[0]}"
        raise

    else :
        if param.remote :
            contenu = f"Le scrapping c'est bien passe a {time.localtime()}"
            mail.envoie_mail("keracles10@gmail.com", contenu)

        bets_arrange = surebets_finder.merge_dict(bet_bible)
        findings = surebets_finder.finder(bets_arrange)

        if len(findings) != 0 :
            print("Voici les surebets trouvés :")
            for str in findings:
                print(str)
            mail.envoie_mail("keracles10@gmail.com", f"{d.strftime('%m-%d_%Hh%M')} Surebets trouvés - Arbitrage-Betting Robot", mail.creation_mail(findings))
        else :
            mail.envoie_mail("keracles10@gmail.com", f"{d.strftime('%m-%d_%Hh%M')} Rien du tout - Arbitrage-Betting Robot", "Pas de Surebets trouvés. Idiots")
            print("Pas de Surebets trouvés. Idiots")
