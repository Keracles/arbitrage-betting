from socket import timeout
from bs4 import BeautifulSoup
import requests
import json
from Important_Class import Match
from w3lib.html import replace_entities
from requests_html import HTMLSession
import re



################################################################################################################################################################
                            #Globals variables#
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'}
url_winamax = 'https://www.winamax.fr'
pattern_ligue1 = "/paris-sportifs/sports/1/7/4"
url_match_test = 'https://www.winamax.fr/paris-sportifs/match/34172247'
nb_outcome = 3
################################################################################################################################################################
                                #Fonctions utiles#

def get_page(url):
    #Make request
    res = requests.get(url, headers=headers)
    res.close()
    return res.text

def get_json(url_match):
    html = get_page(url_match)
    split1 = html.split("var PRELOADED_STATE =")[1]
    split2 = split1.split(";</script>")[0]
    return json.loads(split2)

################################################################################################################################################################
                                #Fonctions pricipales#


def MatchsLinksScrap(pattern):
    session = HTMLSession()
    print(url_winamax + pattern)
    r = session.get(url_winamax + pattern)
    r.html.render(sleep=1, keep_page=True, scrolldown=1, timeout= 15)
    #HTML Parser
    links = []
    motif = re.compile('/paris-sportifs/match/')
    for str in r.html.links :
        test = motif.search(str)
        if test :
            links.append(str)
    session.close()
    r.close()
    return links
    


def build_match(url_match):
    json = get_json(url_match)
    matches_id = list(json["matches"].keys())
    competitorName1 = json["matches"][matches_id[-1]]['competitor1Name']
    competitorName2 = json["matches"][matches_id[-1]]['competitor2Name']
    if competitorName1 == None:
        competitorName1 = "NotMatch"
        competitorName2 = "NotMatch"
    bets_id = json["matches"][matches_id[-1]]['bets']
    bets = {}
    #On obtients la liste des bets
    for bet_id in bets_id:
        bet_id = str(bet_id)
        outcomes = {}
        betTitle = json["bets"][bet_id]["betTitle"]
        betTitle = betTitle.replace(competitorName1, 'Home')
        betTitle = betTitle.replace(competitorName2, 'Away')
        outcomes_id = json["bets"][bet_id]["outcomes"]

        if len(outcomes_id) <= nb_outcome :
            for outcome_id in outcomes_id:
                outcome_id = str(outcome_id)
                outcome_name = json['outcomes'][outcome_id]["label"]
                outcome_name = outcome_name.replace(competitorName1, 'Home')
                outcome_name = outcome_name.replace(competitorName2, 'Away')
                odd = json["odds"][outcome_id]
                outcomes[outcome_name] = odd
            bets[betTitle] = outcomes
    print(bets)
    match = Match(competitorName1, competitorName2, bets)
    return match


def get_league_matches(pattern):
    matches = []
    links = MatchsLinksScrap(pattern)
    d = len(links)
    n = 1
    for link in links:
        url = url_winamax + link
        print(url)
        match = build_match(url)
        matches.append(match)
        print(f"Winamax avancement : {100*n/d}%")
        n += 1
    return matches

################################################################################################################################################################
pattern_foot = {
    "allemagne-1" : "/paris-sportifs/sports/1/30/42",
    "allemagne-2" : "/paris-sportifs/sports/1/30/41",
    "angleterre-1" : "/paris-sportifs/sports/1/1/1",
    "angleterre-2" : "/paris-sportifs/sports/1/1/2",
    "australie" : "/paris-sportifs/sports/1/34/144",
    "autriche" : "/paris-sportifs/sports/1/17/29",
    "belgique" : "/paris-sportifs/sports/1/33/38",
    "bresil" : "/paris-sportifs/sports/1/13/83",
    "bulgarie" : "/paris-sportifs/sports/1/78/232",
    "chili" : "/paris-sportifs/sports/1/49/67280",
    "chypre" : "/paris-sportifs/sports/1/102/681",
    "danemark" : "/paris-sportifs/sports/1/8/12",
    "ecosse" : "/paris-sportifs/sports/1/22/54",
    "espagne-1" : "/paris-sportifs/sports/1/32/36",
    "espagne-2" : "/paris-sportifs/sports/1/32/37",
    "usa" : "/paris-sportifs/sports/1/26/7048",
    "europe-1" : "/paris-sportifs/sports/1/800000542/23",
    "europe-2" : "/paris-sportifs/sports/1/800000542/10909",
    "france-1" : "/paris-sportifs/sports/1/7/4",
    "france-2" : "/paris-sportifs/sports/1/7/19",
    "grece" : "/paris-sportifs/sports/1/67/127",
    "israel" : "/paris-sportifs/sports/1/66/877",
    "italie-1" : "/paris-sportifs/sports/1/31/33",
    "italie-2" : "/paris-sportifs/sports/1/31/34",
    "japon" : "/paris-sportifs/sports/1/52/82",
    "norvege" : "/paris-sportifs/sports/1/5/5",
    "paraguay" : "/paris-sportifs/sports/1/280/16752",
    "pays-bas" : "/paris-sportifs/sports/1/35/39",
    "pologne" : "/paris-sportifs/sports/1/47/64",
    "portugal-1" : "/paris-sportifs/sports/1/44/52",
    "portugal-2" : "/paris-sportifs/sports/1/44/280",
    "reptcheque" : "/paris-sportifs/sports/1/18/49",
    "roumanie" : "/paris-sportifs/sports/1/77/219",
    "slovenie" : "/paris-sportifs/sports/1/24/94",
    "suede" : "/paris-sportifs/sports/1/9/24",
    "suisse" : "/paris-sportifs/sports/1/25/1060",
    "turquie" : "/paris-sportifs/sports/1/46/62"
}

trad_bets = {
    "" : {
        "title" : "1x2",
        "" : "Home",
        "" : "Nul",
        "" : "Away"
    },

    "" : {
        "title" : "Double Chance",
        "" : "Home ou Match nul",
        "" : "Home ou Away",
        "" : "Match nul ou Away"
    },

    "" : {
        "title" : "Draw No Bet",
        "" : "Home",
        "" : "Away"
    },

    "" : {
        "title" : "Both Teams To Score",
        "" : "Oui",
        "" : "Non"
    },

    "" : {
        "title" : "1st Half - 1x2",
        "" : "Home",
        "" : "Nul",
        "" : "Away"
    },

    "" : {
        "title" : "1st Goal",
        "" : "Home",
        "" : "No Goal",
        "" : "Away"
    },

    "" : {
        "title" : "Home To Win Both Halves",
        "" : "Oui",
        "" : "Non"
    },

    "" : {
        "title" : "Away To Win Both Halves",
        "" : "Oui",
        "" : "Non"
    },

    "" : {
        "title" : "Home To Win Either Half",
        "" : "Oui",
        "" : "Non"
    },

    "" : {
        "title" : "Away To Win Either Half",
        "" : "Oui",
        "" : "Non"
    },

    "" : {
        "title" : "Highest Scoring Half",
        "" : "1st",
        "" : "2e",
        "" : "Same"
    },

    "" : {
        "title" : "Home Highest Scoring Half",
        "" : "1st",
        "" : "2e",
        "" : "Same"
    },

    "" : {
        "title" : "Away Highest Scoring Half",
        "" : "1st",
        "" : "2e",
        "" : "Same"
    },

    "" : {
        "title" : "1st Half - Both Teams To Score",
        "" : "Oui",
        "" : "Non"
    }
}

get_league_matches(pattern_foot["angleterre-1"])

