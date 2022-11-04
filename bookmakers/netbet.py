from bs4 import BeautifulSoup
import requests
from w3lib.html import replace_entities
from requests_html import HTMLSession
import re
from bookmakers import Important_Class
import logging, traceback


################################################################################################################################################################
                            #Globals variables#
bookmaker = "netbet"
url_netbet = 'https://www.netbet.fr'                    
pattern_ligue1 = "/football/france/ligue-1-uber-eats/"
pattern_pl = "/football/angleterre/premier-league/"
pattern_israel = '/football/israel/ligat-ha-al/'
url_match_test = 'https://www.netbet.fr/football/france/ligue-1-uber-eats/lens-toulouse'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'}
nb_outcome = 3
################################################################################################################################################################
                                #Fonctions utiles#

def get_page(url): #OKAY
    #Make request
    res = requests.get(url, headers=headers, timeout=5)
    res.close()
    return res.text

################################################################################################################################################################
                                #Fonctions pricipales#

def MatchsLinksScrap(pattern): #OKAY
    session = HTMLSession()
    r = session.get(url_netbet + pattern)
    r.html.render(sleep=1, keep_page=True, scrolldown=1)
    #HTML Parser
    links = []
    motif = re.compile(pattern)
    for str in r.html.links :
        test = motif.search(str)
        if test :
            links.append(str)
    session.close()
    r.close()
    return links


def build_match(url_match, name_league):
    #Get soup
    soup = BeautifulSoup(get_page(url_match), 'html.parser')
    soup =  soup.find(id='main')
    soup = soup.find_all('li', 'uk-open')

    bets = {}
    #On va récupérer et traiter la soup
    for bet_boxe in soup:
        bet_boxTitle = bet_boxe.find('div', 'title uk-accordion-title')
        bet_boxTitle = bet_boxe.find('span', 'label').contents[0]
        bet_boxe = bet_boxe.find("div", "uk-accordion-content")
        if len(bet_boxe.find_all("div", "nb-event_odds_wrapper")) <= 1:
            for bet in bet_boxe.find_all("div", "nb-event_odds_wrapper"):
                bet_outcomes = bet.find_all('a')
                if len(bet_outcomes) <= nb_outcome and len(bet_outcomes) > 1:
                    betTitle = bet_boxTitle
                    outcomes = {}
                    for outcome in bet_outcomes:
                        outcome_name = ''.join(outcome.find('div', 'nb-odds_choice').contents)
                        odd = float(outcome.find('div', 'nb-odds_amount').contents[0].replace(",", "."))
                        outcomes[outcome_name] = odd
                    bets[betTitle] = outcomes
        else :
            for bet in bet_boxe.find_all("div", "nb-event_odds_wrapper"):
                bet_outcomes = bet.find_all('a')
                if len(bet_outcomes) <= nb_outcome and len(bet_outcomes) > 1: 
                    betTitle =  bet_boxTitle + ' ' + bet.find('p').contents[0]
                    outcomes = {}
                    for outcome in bet_outcomes:
                        outcome_name = ''.join(outcome.find('div', 'nb-odds_choice').contents)
                        odd = float(outcome.find('div', 'nb-odds_amount').contents[0].replace(",", '.'))
                        outcomes[outcome_name] = odd
                    bets[betTitle] = outcomes
    competitorName1 = Important_Class.format_name_g(list(bets['Qui va gagner le match ?'].keys())[0])
    competitorName2 = Important_Class.format_name_g(list(bets['Qui va gagner le match ?'].keys())[-1])

    bets_replace = {}
    for i, (betTitle, outcomes) in enumerate(bets.items()):
        betTitle_replace = Important_Class.format_name_g(betTitle)
        betTitle_replace = Important_Class.format_name(betTitle_replace, competitorName1, competitorName2, bookmaker, name_league)
        outcomes_replace = {}
        if betTitle_replace in trad_bets.keys() :
            for i, (outcome_name, odd) in enumerate(outcomes.items()):
                outcome_name_replace = Important_Class.format_name_g(outcome_name)
                outcome_name_replace_old = outcome_name_replace
                outcome_name_replace = Important_Class.format_name(outcome_name_replace, competitorName1, competitorName2, bookmaker, name_league)
                outcome_name_replace = Important_Class.check_outcome(betTitle_replace, competitorName1, competitorName2, outcome_name_replace, outcome_name_replace_old, trad_bets, bookmaker, name_league)
                outcomes_replace[outcome_name_replace] = odd
            betTitle_replace = trad_bets[betTitle_replace]["title"]
            bets_replace[betTitle_replace] = outcomes_replace

    match = Important_Class.Match(competitorName1, competitorName2, bets_replace, url_match)

    if Important_Class.debug:
        Important_Class.Match.show(match)
    return match


def get_league_matches(pattern, name_league):
    matches = []
    links = MatchsLinksScrap(pattern)
    for link in links :
        url_match = url_netbet + link
        try : 
            match = build_match(url_match, name_league)
        except requests.exceptions.ReadTimeout:
            print(f"Timeout match {url_match}")
        except :
            logging.warning(f"Erreur {bookmaker} / match {url_match}"+f"\n Traceback : {traceback.format_exc()}")
        else:
            matches.append(match)
    return matches




################################################################################################################################################################
pattern_foot = {
    "allemagne-1" : "/football/allemagne/bundesliga/",
    "allemagne-2" : "/football/allemagne/bundesliga-2/",
    "angleterre-1" : "/football/angleterre/premier-league/",
    "angleterre-2" : "/football/angleterre/championship/",
    "australie" : "/football/australie/a-league/",
    "autriche" : "/football/autriche/bundesliga-aut/",
    "belgique" : "/football/belgique/jupiler-league/",
    "bresil" : "/football/bresil/brasileirao/",
    "bulgarie" : "/football/bulgarie/first-professional-league/",
    "chili" : "/football/chili/campeonato-afp-planvital/",
    "danemark" : "/football/danemark/superligaen/",
    "ecosse" : "/football/ecosse/premiership/",
    "espagne-1" : "/football/espagne/laliga/",
    "espagne-2" : "/football/espagne/laliga2/",
    "usa" : "/football/etats-unis/major-league-soccer/",
    "europe-1" : "/football/ligue-des-champions/ligue-des-champions/",
    "europe-2" : "/football/ligue-europa/ligue-europa/",
    "france-1" : "/football/france/ligue-1-uber-eats/",
    "france-2" : "/football/france/ligue-2-bkt/",
    "grece" : "/football/grece/super-league/",
    "israel" : "/football/israel/ligat-ha-al/",
    "italie-1" : "/football/italie/serie-a/",
    "italie-2" : "/football/italie/serie-b/",
    "japon" : "/football/japon/j-league/",
    "norvege" : "/football/norvege/eliteserien/",
    "pays-bas" : "/football/pays-bas/eredivisie/",
    "pologne" : "/football/pologne/ekstraklasa/",
    "portugal-1" : "/football/portugal/primeira-liga/",
    "portugal-2" : "/football/portugal/segunda-liga/",
    "reptcheque" : "/football/republique-tcheque/fortuna-liga/",
    "roumanie" : "/football/roumanie/liga-1/",
    "slovenie" : "/football/slovenie/prvaliga/",
    "suede" : "/football/suede/allsvenskan/",
    "suisse" : "/football/suisse/credit-suisse-super-league/",
    "turquie" : "/football/turquie/super-lig/"
}

trad_bets = {
    "Qui va gagner le match ?" : {
        "title" : "1x2",
        "Home" : "Home",
        "Nul" : "Nul",
        "Away" : "Away"
    },

    "Double Chance0" : {
        "title" : "Double Chance",
        "1N" : "Home ou Match nul",
        "12" : "Home ou Away",
        "N2" : "Match nul ou Away"
    },

    "Qui va gagner le match ? (rembourse si match nul)" : {
        "title" : "Draw No Bet",
        "Home" : "Home",
        "Away" : "Away"
    },

    "Les 2 equipes marquent ?" : {
        "title" : "Both Teams To Score",
        "Oui" : "Oui",
        "Non" : "Non"
    },

    "Qui va gagner la 1ere mi-temps ?" : {
        "title" : "1st Half - 1x2",
        "Home" : "Home",
        "Nul" : "Nul",
        "Away" : "Away"
    },

    "Premiere equipe a marquer ?" : {
        "title" : "1st Goal",
        "Home" : "Home",
        "Pas de but" : "No Goal",
        "Away" : "Away"
    },

    "Home gagne les 2 mi-temps ?" : {
        "title" : "Home To Win Both Halves",
        "Oui" : "Oui",
        "Non" : "Non"
    },

    "Away gagne les 2 mi-temps ?" : {
        "title" : "Away To Win Both Halves",
        "Oui" : "Oui",
        "Non" : "Non"
    },

    "Home gagne au moins une des 2 mi-temps ?" : {
        "title" : "Home To Win Either Half",
        "Oui" : "Oui",
        "Non" : "Non"
    },

    "Away gagne au moins une des 2 mi-temps ?" : {
        "title" : "Away To Win Either Half",
        "Oui" : "Oui",
        "Non" : "Non"
    },

    "Mi-temps avec le plus de buts ?" : {
        "title" : "Highest Scoring Half",
        "1ere" : "1st",
        "2eme" : "2e",
        "Autant" : "Same"
    },

    "Mi-temps avec le plus de buts pour Home ?" : {
        "title" : "Home Highest Scoring Half",
        "1ere" : "1st",
        "2eme" : "2e",
        "Autant" : "Same"
    },

    "Mi-temps avec le plus de buts pour Away ?" : {
        "title" : "Away Highest Scoring Half",
        "1ere" : "1st",
        "2eme" : "2e",
        "Autant" : "Same"
    },

    "Les 2 equipes marquent en 1ere mi-temps ?" : {
        "title" : "1st Half - Both Teams To Score",
        "Oui" : "Oui",
        "Non" : "Non"
    }
}



################################################################################################################################################################

