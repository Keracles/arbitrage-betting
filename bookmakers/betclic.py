from bs4 import BeautifulSoup
import requests
from w3lib.html import replace_entities
from requests_html import HTMLSession
import re
from bookmakers import Important_Class
import multiprocessing as mp
import json


################################################################################################################################################################
                            #Globals variables#
bookmaker = "betclic"
url_betclic = 'https://www.betclic.fr'                    
pattern_ligue1 = "/football-s1/ligue-1-uber-eats-c4"
url_match_test = 'betclic.fr/football-s1/ligue-1-uber-eats-c4/lens-toulouse-m3001559137'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'}
nb_outcome = 3
################################################################################################################################################################
                                #Fonctions utiles#

def get_page(url):
    session = HTMLSession()
    r = session.get(url)
    r.html.render(sleep=1, scrolldown=1)
    soup = BeautifulSoup(r.html.find('*')[0].html, 'html.parser')
    r.close()
    return soup

def get_json(num_match):
    r = requests.get(f"https://offer.cdn.begmedia.com/api/pub/v5/events/{num_match}?application=2&countrycode=fr&language=fr&sitecode=frfr")
    return json.loads(r.text)
################################################################################################################################################################
                                #Fonctions pricipales#

def MatchsLinksScrap(pattern):
    session = HTMLSession()
    r = session.get(url_betclic + pattern)
    r.html.render(sleep=1, scrolldown=1, timeout = 30)
    #HTML Parser
    links = []
    
    motif = re.compile("m3")
    for str in r.html.links :
        test = motif.search(str)
        if test :
            links.append(str)
    r.close()
    return links


def build_match(url_match, name_league):
    #Obtenir le numéro du match
    split = url_match.split('-')
    num = split[-1]
    match_id = int(num[1:len(num)])

    #On va récupérer et traiter le json
    json = get_json(match_id) 
    competitorName1 = Important_Class.format_name_g(json["contestants"][0]['name'])
    competitorName2 = Important_Class.format_name_g(json["contestants"][1]['name'])
    bets = {}
    
    for bet in json['grouped_markets']:
        if 'markets' in bet.keys():
            bet = bet['markets'][0]
            if len(bet['selections']) <=nb_outcome :
                outcomes = {}
                betTitle = Important_Class.format_name_g(bet["name"])
                betTitle = Important_Class.format_name(betTitle, competitorName1, competitorName2, bookmaker, name_league)
                if Important_Class.debug :
                    a=1
                    print(betTitle)
                if betTitle in trad_bets.keys() :
                    if len(bet["selections"]) == 1:
                        if len(bet["selections"][0]) <=nb_outcome :
                            for outcome in bet["selections"][0]:
                                outcome_name = Important_Class.format_name_g(outcome['name'])
                                outcome_name_old = outcome_name 
                                outcome_name = Important_Class.format_name(outcome_name, competitorName1, competitorName2, bookmaker, name_league)
                                odd = outcome['odds']


                                outcome_name = Important_Class.check_outcome(betTitle, competitorName1, competitorName2, outcome_name, outcome_name_old, trad_bets, bookmaker, name_league)
                                outcomes[outcome_name] = odd
                            betTitle = trad_bets[betTitle]["title"]
                            bets[betTitle] = outcomes

                    else : 
                        for outcome in bet["selections"]:
                            outcome = outcome[0]
                            outcome_name = Important_Class.format_name_g(outcome['name'])
                            outcome_name_old = outcome_name 
                            outcome_name = Important_Class.format_name(outcome_name, competitorName1, competitorName2, bookmaker, name_league)
                            odd = outcome['odds']
                            outcome_name = Important_Class.check_outcome(betTitle, competitorName1, competitorName2, outcome_name, outcome_name_old, trad_bets, bookmaker, name_league)
                            outcomes[outcome_name] = odd
                        betTitle = trad_bets[betTitle]["title"]
                        bets[betTitle] = outcomes
    match = Important_Class.Match(competitorName1, competitorName2, bets, url_match)

    if Important_Class.debug:
        Important_Class.Match.show(match)

    return match


def get_league_matches(pattern, name_league):
    matches = []
    links = MatchsLinksScrap(pattern)
    for link in links :
        url_match = url_betclic + link
        try : 
            match = build_match(url_match, name_league)
        except requests.exceptions.ReadTimeout:
            print(f"Timeout match {url_match}")
            pass
        matches.append(match)
    return matches


################################################################################################################################################################
pattern_foot = {
    "allemagne-1" : "/football-s1/allemagne-bundesliga-c5",
    "allemagne-2" : "/football-s1/allemagne-bundesliga-2-c29",
    "angleterre-1" : "/football-s1/angl-premier-league-c3",
    "angleterre-2" : "/football-s1/angl-championship-c28",
    "australie" : "/football-s1/australie-a-league-c1874",
    "autriche" : "/football-s1/autriche-bundesliga-c35",
    "belgique" : "/football-s1/belgique-division-1a-c26",
    "bresil" : "/football-s1/bresil-serie-a-c187",
    "bulgarie" : "/football-s1/bulgarie-a-pfg-c548",
    "chili" : "/football-s1/chili-primera-c3584",
    "danemark" : "/football-s1/danemark-superliga-c88",
    "ecosse" : "/football-s1/ecosse-premiership-c33",
    "espagne-1" : "/football-s1/espagne-liga-primera-c7",
    "espagne-2" : "/football-s1/espagne-liga-segunda-c31",
    "usa" : "/football-s1/etats-unis-mls-c504",
    "europe-1" : "/football-s1/ligue-des-champions-c8",
    "europe-2" : "/football-s1/ligue-europa-c3453",
    "france-1" : "/football-s1/ligue-1-uber-eats-c4",
    "france-2" : "/football-s1/ligue-2-bkt-c19",
    "grece" : "/football-s1/grece-superleague-c38",
    "israel" : "/football-s1/israel-premier-league-c1876",
    "italie-1" : "/football-s1/italie-serie-a-c6",
    "italie-2" : "/football-s1/italie-serie-b-c30",
    "japon" : "/football-s1/japon-j-league-c503",
    "norvege" : "/football-s1/norvege-eliteserien-c156",
    "pays-bas" : "/football-s1/pays-bas-eredivisie-c21",
    "pologne" : "/football-s1/pologne-ekstraklasa-c221",
    "portugal-1" : "/football-s1/portugal-primeira-liga-c32",
    "portugal-2" : "/football-s1/portugal-segunda-liga-c939",
    "reptcheque" : "/football-s1/rep-tcheque-liga-c220",
    "roumanie" : "/football-s1/roumanie-liga-1-c552",
    "slovenie" : "/football-s1/slovenie-1-snl-c549",
    "suede" : "/football-s1/suede-allsvenskan-c145",
    "suisse" : "/football-s1/suisse-super-league-c27",
    "turquie" : "/football-s1/turquie-super-lig-c37"
}


trad_bets = {
    "Resultat du match" : {
        "title" : "1x2",
        "Home" : "Home",
        "Nul" : "Nul",
        "Away" : "Away"
    },

    "Match0" : {
        "title" : "Double Chance",
        "Home ou Nul" : "Home ou Match nul",
        "Home ou Away" : "Home ou Away",
        "Nul ou Away" : "Match nul ou Away"
    },

    "Resultat du match (rembourse si match nul)" : {
        "title" : "Draw No Bet",
        "Home" : "Home",
        "Away" : "Away"
    },

    "But pour les 2 equipes" : {
        "title" : "Both Teams To Score",
        "Oui" : "Oui",
        "Non" : "Non"
    },

    "1ere mi-temps - Resultat" : {
        "title" : "1st Half - 1x2",
        "Home" : "Home",
        "Nul" : "Nul",
        "Away" : "Away"
    },

    "1er but" : {
        "title" : "1st Goal",
        "Home" : "Home",
        "Pas de but" : "No Goal",
        "Away" : "Away"
    },

    "Home gagne les 2 mi-temps" : {
        "title" : "Home To Win Both Halves",
        "Oui" : "Oui",
        "Non" : "Non"
    },

    "Away gagne les 2 mi-temps" : {
        "title" : "Away To Win Both Halves",
        "Oui" : "Oui",
        "Non" : "Non"
    },

    "Home gagne au moins 1 mi-temps" : {
        "title" : "Home To Win Either Half",
        "Oui" : "Oui",
        "Non" : "Non"
    },

    "Away gagne au moins 1 mi-temps" : {
        "title" : "Away To Win Either Half",
        "Oui" : "Oui",
        "Non" : "Non"
    },

    "Mi-temps avec le plus de buts" : {
        "title" : "Highest Scoring Half",
        "1ere mi-temps" : "1st",
        "2eme mi-temps" : "2e",
        "Nul" : "Same"
    },

    "Mi-temps avec le + de buts - Home" : {
        "title" : "Home Highest Scoring Half",
        "1ere mi-temps" : "1st",
        "2eme mi-temps" : "2e",
        "Nul" : "Same"
    },

    "Mi-temps avec le + de buts - Away" : {
        "title" : "Away Highest Scoring Half",
        "1ere mi-temps" : "1st",
        "2eme mi-temps" : "2e",
        "Nul" : "Same"
    },

    "1ere Mi-temps - Les 2 equipes marquent" : {
        "title" : "1st Half - Both Teams To Score",
        "Oui" : "Oui",
        "Non" : "Non"
    }
}

################################################################################################################################################################
