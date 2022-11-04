import requests
import json
from bookmakers import Important_Class
from requests_html import HTMLSession
import re
import logging, traceback



################################################################################################################################################################
                            #Globals variables#

bookmaker = 'winamax'
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
    r = session.get(url_winamax + pattern)
    r.html.render(sleep=5, keep_page=True, timeout= 30)
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
    


def build_match(url_match, name_league):
    json = get_json(url_match)
    matches_id = list(json["matches"].keys())
    competitorName1 = Important_Class.format_name_g(json["matches"][matches_id[-1]]['competitor1Name'])
    competitorName2 = Important_Class.format_name_g(json["matches"][matches_id[-1]]['competitor2Name'])
    if competitorName1 == None:
        competitorName1 = "NotMatch"
        competitorName2 = "NotMatch"
    bets_id = json["matches"][matches_id[-1]]['bets']
    bets = {}
    #On obtients la liste des bets
    for bet_id in bets_id:
        bet_id = str(bet_id)
        outcomes = {}
        betTitle = Important_Class.format_name_g(json["bets"][bet_id]["betTitle"])
        betTitle = Important_Class.format_name(betTitle, competitorName1, competitorName2,bookmaker, name_league)
        outcomes_id = json["bets"][bet_id]["outcomes"]

        if Important_Class.debug :
            #print("Balise 1 : ", betTitle)
            a=1

        if len(outcomes_id) <= nb_outcome :
            if betTitle in trad_bets.keys() : 
                for outcome_id in outcomes_id:
                        outcome_id = str(outcome_id)
                        outcome_name = Important_Class.format_name_g(json['outcomes'][outcome_id]["label"])
                        outcome_name_old = outcome_name
                        outcome_name = Important_Class.format_name(outcome_name, competitorName1, competitorName2, bookmaker, name_league)
                        odd = round(float(json["odds"][outcome_id]),2)

                        outcome_name = Important_Class.check_outcome(betTitle, competitorName1, competitorName2, outcome_name, outcome_name_old, trad_bets, bookmaker, name_league)
                        outcomes[outcome_name] = odd

                        
                betTitle = trad_bets[betTitle]["title"]
                bets[betTitle] = outcomes
    match = Important_Class.Match(competitorName1, competitorName2, bets, url_match)

    if Important_Class.debug :
        Important_Class.Match.show(match)
    return match





def get_league_matches(pattern, name_league):
    matches = []
    links = MatchsLinksScrap(pattern)
    for link in links:
        url_match = url_winamax + link
        try : 
            match = build_match(url_match, name_league)
        except requests.exceptions.ReadTimeout:
            print(f"Timeout match {url_match}")
        except :
            logging.warning(f"Erreur {bookmaker} / match {url_match}"+f"\n Traceback : {traceback.format_exc()}")
        matches.append(match)
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
    "danemark" : "/paris-sportifs/sports/1/8/12",
    "ecosse" : "/paris-sportifs/sports/1/22/54",
    "espagne-1" : "/paris-sportifs/sports/1/32/36",
    "espagne-2" : "/paris-sportifs/sports/1/32/37",
    "usa" : "/paris-sportifs/sports/1/26/18",
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
    "Resultat" : {
        "title" : "1x2",
        "Home" : "Home",
        "Match nul" : "Nul",
        "Egalite" : "Nul",
        "Away" : "Away"
    },

    "" : {
        "title" : "Double Chance",
        "Home ou match nul" : "Home ou Match nul",
        "Home ou Away" : "Home ou Away",
        "Away ou match nul" : "Match nul ou Away"
    },

    "Vainqueur (rembourse si match nul)" : {
        "title" : "Draw No Bet",
        "Home" : "Home",
        "Away" : "Away"
    },

    "Les 2 equipes marquent" : {
        "title" : "Both Teams To Score",
        "Oui" : "Oui",
        "Non" : "Non"
    },

    "Mi-temps - resultat" : {
        "title" : "1st Half - 1x2",
        "Home" : "Home",
        "Match nul" : "Nul",
        "Egalite" : "Nul",
        "Away" : "Away"
    },

    "Equipe qui marque le 1er but" : {
        "title" : "1st Goal",
        "Home" : "Home",
        "Aucune" : "No Goal",
        "Away" : "Away"
    },

    "Home gagne les deux mi-temps" : {
        "title" : "Home To Win Both Halves",
        "Oui" : "Oui",
        "Non" : "Non"
    },

    "Away gagne les deux mi-temps" : {
        "title" : "Away To Win Both Halves",
        "Oui" : "Oui",
        "Non" : "Non"
    },

    "Home gagne une des mi-temps" : {
        "title" : "Home To Win Either Half",
        "Oui" : "Oui",
        "Non" : "Non"
    },

    "Away gagne une des mi-temps" : {
        "title" : "Away To Win Either Half",
        "Oui" : "Oui",
        "Non" : "Non"
    },

    "Mi-temps avec le plus de buts" : {
        "title" : "Highest Scoring Half",
        "1re mi-temps" : "1st",
        "2de mi-temps" : "2e",
        "Egalite" : "Same"
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

    "Mi-temps - les 2 equipes marquent" : {
        "title" : "1st Half - Both Teams To Score",
        "Oui" : "Oui",
        "Non" : "Non"
    }
}

