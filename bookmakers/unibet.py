from bs4 import BeautifulSoup
import requests
from requests_html import HTMLSession
from bookmakers import Important_Class
import json
from f_annex import exceptions
import logging, traceback


################################################################################################################################################################
                            #Globals variables#
bookmaker = "unibet"
url_unibet = 'https://www.unibet.fr'                    
api_ligue1 = "https://www.unibet.fr/zones/v3/sportnode/markets.json?nodeId=435774672&filter=R%25C3%25A9sultat&marketname=R%25C3%25A9sultat%2520du%2520match"
api_pl = 'https://www.unibet.fr/zones/v3/sportnode/markets.json?nodeId=703695255&filter=R%C3%A9sultat&marketname=R%C3%A9sultat%20du%20match'
url_match_test = 'https://www.unibet.fr/sport/football/event/leicester-manchester-city-2576687_1.html'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0 Win64 x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'}
nb_outcome = 3
################################################################################################################################################################
                                #Fonctions utiles#

def get_page(url):
    session = HTMLSession()
    r = session.get(url, timeout=10)
    r.html.render(sleep=1, scrolldown=1)
    soup = BeautifulSoup(r.html.find('*')[0].html, 'html.parser')
    r.close()
    return soup

def get_json(num_match):
    r = requests.get(f"https://www.unibet.fr/zones/event.json?eventId={num_match}")
    return json.loads(r.text)
################################################################################################################################################################
                                #Fonctions pricipales#

def MatchsLinksScrap(api_league):
    links = []
    r =  requests.get(api_league)
    json_file = json.loads(r.text)

    try :
        json_file["marketsByType"][0]['days'] 
    except KeyError:
        raise exceptions.NoMatchinLeague



    for day in json_file["marketsByType"][0]['days']:
        for event in day["events"]:
            links.append(event["markets"][0]["eventFriendlyUrl"])
    r.close()
    return links


def build_match(url_match, name_league):
    #Get number
    split = url_match.split('-')
    split = split[-1]
    split = split.split('.')
    match_id = split[0]
    
    #On va récupérer et traiter le json
    json = get_json(match_id)
    competitorName1 = Important_Class.format_name_g(json["eventHeader"]['homeName'])
    competitorName2 = Important_Class.format_name_g(json["eventHeader"]['awayName'])
    bets = {}

    
    for bet_out in json['marketClassList']:
        for bet in bet_out['marketList']:
            if len(bet['selections']) <= nb_outcome :
                outcomes = {}
                betTitle = Important_Class.format_name_g(bet["marketType"])
                betTitle = Important_Class.format_name(betTitle, competitorName1, competitorName2,bookmaker, name_league)
                if Important_Class.debug:
                    a=1
                    #print(betTitle)
                if betTitle in trad_bets.keys() : 
                    for outcome in bet["selections"]:
                        outcome_name = Important_Class.format_name_g(outcome['name'])
                        outcome_name_old = outcome_name
                        outcome_name = Important_Class.format_name(outcome_name, competitorName1, competitorName2, bookmaker, name_league)
                        odd = round((float(outcome['currentPriceUp'])/int(outcome['currentPriceDown'])) + 1, 2)
                        outcome_name = Important_Class.check_outcome(betTitle, competitorName1, competitorName2, outcome_name, outcome_name_old, trad_bets, bookmaker, name_league)
                        outcomes[outcome_name] = odd

                    betTitle = trad_bets[betTitle]["title"]
                    bets[betTitle] = outcomes
    
    
    match = Important_Class.Match(competitorName1, competitorName2, bets, url_match)

    if Important_Class.debug:
        Important_Class.Match.show(match)
    return match


def get_league_matches(api_league, name_league):
    matches = []
    links = MatchsLinksScrap(api_league)
    for link in links :
        url_match = url_unibet + link
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
    "allemagne-1" : "https://www.unibet.fr/zones/v3/sportnode/markets.json?nodeId=116432547&filter=R%C3%A9sultat&marketname=R%C3%A9sultat%20du%20match",
    "allemagne-2" : "https://www.unibet.fr/zones/v3/sportnode/markets.json?nodeId=30914428&filter=R%C3%A9sultat&marketname=R%C3%A9sultat%20du%20match",
    'allemagne-c' : "https://www.unibet.fr/zones/v3/sportnode/markets.json?nodeId=31413114&filter=Comp%C3%A9tition&marketname=Vainqueur%20de%20la%20comp%C3%A9tition",
    "andorre" : "https://www.unibet.fr/zones/v3/sportnode/markets.json?nodeId=541596310&filter=R%C3%A9sultat&marketname=R%C3%A9sultat%20du%20match",
    "angleterre-1" : "https://www.unibet.fr/zones/v3/sportnode/markets.json?nodeId=116875930&filter=R%C3%A9sultat&marketname=R%C3%A9sultat%20du%20match",
    "angleterre-2" : "https://www.unibet.fr/zones/v3/sportnode/markets.json?nodeId=116876043&filter=R%C3%A9sultat&marketname=R%C3%A9sultat%20du%20match",
    "algerie" : "https://www.unibet.fr/zones/v3/sportnode/markets.json?nodeId=34494743&filter=R%C3%A9sultat&marketname=R%C3%A9sultat%20du%20match",
    "armenie" : "https://www.unibet.fr/zones/v3/sportnode/markets.json?nodeId=79202948&filter=R%C3%A9sultat&marketname=R%C3%A9sultat%20du%20match",
    "australie" : "https://www.unibet.fr/zones/v3/sportnode/markets.json?nodeId=702488951&filter=R%C3%A9sultat&marketname=R%C3%A9sultat%20du%20match",
    "autriche" : "https://www.unibet.fr/zones/v3/sportnode/markets.json?nodeId=30990209&filter=R%C3%A9sultat&marketname=R%C3%A9sultat%20du%20match",
    "azerbaidjan" : "https://www.unibet.fr/zones/v3/sportnode/markets.json?nodeId=32292530&filter=R%C3%A9sultat&marketname=R%C3%A9sultat%20du%20match",
    "belgique" : "https://www.unibet.fr/zones/v3/sportnode/markets.json?nodeId=31087161&filter=R%C3%A9sultat&marketname=R%C3%A9sultat%20du%20match",
    "bosnie" : "https://www.unibet.fr/zones/v3/sportnode/markets.json?nodeId=31920220&filter=R%C3%A9sultat&marketname=R%C3%A9sultat%20du%20match",
    "bresil" : "https://www.unibet.fr/zones/v3/sportnode/markets.json?nodeId=30918991&filter=R%C3%A9sultat&marketname=R%C3%A9sultat%20du%20match",
    "bulgarie" : "https://www.unibet.fr/zones/v3/sportnode/markets.json?nodeId=32152172&filter=R%C3%A9sultat&marketname=R%C3%A9sultat%20du%20match",
    "chili" : "https://www.unibet.fr/zones/v3/sportnode/markets.json?nodeId=242528229&filter=R%C3%A9sultat&marketname=R%C3%A9sultat%20du%20match",
    "chypre" : "https://www.unibet.fr/zones/v3/sportnode/markets.json?nodeId=33838215&filter=R%C3%A9sultat&marketname=R%C3%A9sultat%20du%20match",
    "colombie" : "https://www.unibet.fr/zones/v3/sportnode/markets.json?nodeId=242528554&filter=R%C3%A9sultat&marketname=R%C3%A9sultat%20du%20match",
    "croatie" : "https://www.unibet.fr/zones/v3/sportnode/markets.json?nodeId=31049077&filter=R%C3%A9sultat&marketname=R%C3%A9sultat%20du%20match",
    "danemark" : "https://www.unibet.fr/zones/v3/sportnode/markets.json?nodeId=30910871&filter=R%C3%A9sultat&marketname=R%C3%A9sultat%20du%20match",
    "ecosse" : "https://www.unibet.fr/zones/v3/sportnode/markets.json?nodeId=31413185&filter=R%C3%A9sultat&marketname=R%C3%A9sultat%20du%20match",
    "equateur" : "https://www.unibet.fr/zones/v3/sportnode/markets.json?nodeId=428385947&filter=R%C3%A9sultat&marketname=R%C3%A9sultat%20du%20match",
    "espagne-1" : "https://www.unibet.fr/zones/v3/sportnode/markets.json?nodeId=116876665&filter=R%C3%A9sultat&marketname=R%C3%A9sultat%20du%20match",
    "espagne-2" : "https://www.unibet.fr/zones/v3/sportnode/markets.json?nodeId=32184870&filter=R%C3%A9sultat&marketname=R%C3%A9sultat%20du%20match",
    "espagne-c" : "https://www.unibet.fr/zones/v3/sportnode/markets.json?nodeId=116876843&filter=Comp%C3%A9tition&marketname=Vainqueur%20de%20la%20comp%C3%A9tition",
    "estonie" : "https://www.unibet.fr/zones/v3/sportnode/markets.json?nodeId=30911949&filter=R%C3%A9sultat&marketname=R%C3%A9sultat%20du%20match",
    "usa" : "https://www.unibet.fr/zones/v3/sportnode/markets.json?nodeId=31618329&filter=R%C3%A9sultat&marketname=R%C3%A9sultat%20du%20match",
    "europe-1" : "https://www.unibet.fr/zones/v3/sportnode/markets.json?nodeId=445490388&filter=R%C3%A9sultat&marketname=R%C3%A9sultat%20du%20match",
    "europe-2" : "https://www.unibet.fr/zones/v3/sportnode/markets.json?nodeId=445503791&filter=R%C3%A9sultat&marketname=R%C3%A9sultat%20du%20match",
    "france-1" : "https://www.unibet.fr/zones/v3/sportnode/markets.json?nodeId=703695044&filter=R%C3%A9sultat&marketname=R%C3%A9sultat%20du%20match",
    "france-2" : "https://www.unibet.fr/zones/v3/sportnode/markets.json?nodeId=703695047&filter=R%C3%A9sultat&marketname=R%C3%A9sultat%20du%20match",
    "georgie" : "https://www.unibet.fr/zones/v3/sportnode/markets.json?nodeId=60702022&filter=R%C3%A9sultat&marketname=R%C3%A9sultat%20du%20match",
    "gibraltar" : "https://www.unibet.fr/zones/v3/sportnode/markets.json?nodeId=159391344&filter=R%C3%A9sultat&marketname=R%C3%A9sultat%20du%20match",
    "grece" : "https://www.unibet.fr/zones/v3/sportnode/markets.json?nodeId=32690446&filter=R%C3%A9sultat&marketname=R%C3%A9sultat%20du%20match",
    "hongrie" : "https://www.unibet.fr/zones/v3/sportnode/markets.json?nodeId=31920363&filter=R%C3%A9sultat&marketname=R%C3%A9sultat%20du%20match",
    "irlande" : "https://www.unibet.fr/zones/v3/sportnode/markets.json?nodeId=30921708&filter=R%C3%A9sultat&marketname=R%C3%A9sultat%20du%20match",
    "irlande-nord" : "https://www.unibet.fr/zones/v3/sportnode/markets.json?nodeId=32154495&filter=R%C3%A9sultat&marketname=R%C3%A9sultat%20du%20match",
    "israel" : "https://www.unibet.fr/zones/v3/sportnode/markets.json?nodeId=33158892&filter=R%C3%A9sultat&marketname=R%C3%A9sultat%20du%20match",
    "italie-1" : "https://www.unibet.fr/zones/v3/sportnode/markets.json?nodeId=116876945&filter=R%C3%A9sultat&marketname=R%C3%A9sultat%20du%20match",
    "italie-2" : "https://www.unibet.fr/zones/v3/sportnode/markets.json?nodeId=32975099&filter=R%C3%A9sultat&marketname=R%C3%A9sultat%20du%20match",
    "italie-c" : "https://www.unibet.fr/zones/v3/sportnode/markets.json?nodeId=116876964&filter=Comp%C3%A9tition&marketname=Vainqueur%20de%20la%20comp%C3%A9tition",
    "japon" : "https://www.unibet.fr/zones/v3/sportnode/markets.json?nodeId=30911324&filter=R%C3%A9sultat&marketname=R%C3%A9sultat%20du%20match",
    "kosovo" : "https://www.unibet.fr/zones/v3/sportnode/markets.json?nodeId=466473777&filter=R%C3%A9sultat&marketname=R%C3%A9sultat%20du%20match",
    "lituanie" : "https://www.unibet.fr/zones/v3/sportnode/markets.json?nodeId=31611153&filter=R%C3%A9sultat&marketname=R%C3%A9sultat%20du%20match",
    "macedoine" : "https://www.unibet.fr/zones/v3/sportnode/markets.json?nodeId=32292595&filter=Buts&marketname=But%20sur%20penalty",
    "malte" : "https://www.unibet.fr/zones/v3/sportnode/markets.json?nodeId=46257828&filter=R%C3%A9sultat&marketname=R%C3%A9sultat%20du%20match",
    "maroc" :  "https://www.unibet.fr/zones/v3/sportnode/markets.json?nodeId=34495011&filter=R%C3%A9sultat&marketname=R%C3%A9sultat%20du%20match",
    "norvege" : "https://www.unibet.fr/zones/v3/sportnode/markets.json?nodeId=30910939&filter=R%C3%A9sultat&marketname=R%C3%A9sultat%20du%20match",
    "paraguay" : "https://www.unibet.fr/zones/v3/sportnode/markets.json?nodeId=703695253&filter=R%C3%A9sultat&marketname=R%C3%A9sultat%20du%20match",
    "pays-bas" : "https://www.unibet.fr/zones/v3/sportnode/markets.json?nodeId=31086981&filter=R%C3%A9sultat&marketname=R%C3%A9sultat%20du%20match",
    "pays-galles" : "https://www.unibet.fr/zones/v3/sportnode/markets.json?nodeId=32601860&filter=R%C3%A9sultat&marketname=R%C3%A9sultat%20du%20match",
    "pologne" : "https://www.unibet.fr/zones/v3/sportnode/markets.json?nodeId=31921084&filter=R%C3%A9sultat&marketname=R%C3%A9sultat%20du%20match",
    "portugal-1" : "https://www.unibet.fr/zones/v3/sportnode/markets.json?nodeId=436203630&filter=R%C3%A9sultat&marketname=R%C3%A9sultat%20du%20match",
    "portugal-2" : "https://www.unibet.fr/zones/v3/sportnode/markets.json?nodeId=32000383&filter=R%C3%A9sultat&marketname=R%C3%A9sultat%20du%20match",
    "portugal-c" : "https://www.unibet.fr/zones/v3/sportnode/markets.json?nodeId=35709342&filter=R%C3%A9sultat&marketname=R%C3%A9sultat%20du%20match",
    "reptcheque" : "https://www.unibet.fr/zones/v3/sportnode/markets.json?nodeId=31413119&filter=R%C3%A9sultat&marketname=R%C3%A9sultat%20du%20match",
    "roumanie" : "https://www.unibet.fr/zones/v3/sportnode/markets.json?nodeId=31921477&filter=R%C3%A9sultat&marketname=R%C3%A9sultat%20du%20match",
    "saint-marin" : "https://www.unibet.fr/zones/v3/sportnode/markets.json?nodeId=703695296&filter=R%C3%A9sultat&marketname=R%C3%A9sultat%20du%20match",
    "serbie" : "https://www.unibet.fr/zones/v3/sportnode/markets.json?nodeId=32151637&filter=R%C3%A9sultat&marketname=R%C3%A9sultat%20du%20match",
    "slovaquie" : "https://www.unibet.fr/zones/v3/sportnode/markets.json?nodeId=30917363&filter=R%C3%A9sultat&marketname=R%C3%A9sultat%20du%20match",
    "slovenie" : "https://www.unibet.fr/zones/v3/sportnode/markets.json?nodeId=30990203&filter=R%C3%A9sultat&marketname=R%C3%A9sultat%20du%20match",
    "suede" : "https://www.unibet.fr/zones/v3/sportnode/markets.json?nodeId=30911983&filter=R%C3%A9sultat&marketname=R%C3%A9sultat%20du%20match",
    "suisse" : "https://www.unibet.fr/zones/v3/sportnode/markets.json?nodeId=30917369&filter=R%C3%A9sultat&marketname=R%C3%A9sultat%20du%20match",
    "tunisie" : "https://www.unibet.fr/zones/v3/sportnode/markets.json?nodeId=30910741&filter=R%C3%A9sultat&marketname=R%C3%A9sultat%20du%20match",
    "turquie" : "https://www.unibet.fr/zones/v3/sportnode/markets.json?nodeId=58869345&filter=R%C3%A9sultat&marketname=R%C3%A9sultat%20du%20match",
    "ukraine" : "https://www.unibet.fr/zones/v3/sportnode/markets.json?nodeId=30919092&filter=R%C3%A9sultat&marketname=R%C3%A9sultat%20du%20match",
    "cdm" : "https://www.unibet.fr/zones/v3/sportnode/markets.json?nodeId=371933633&filter=R%C3%A9sultat&marketname=R%C3%A9sultat%20du%20match"

}


trad_bets = {
    "1x2" : {
        "title" : "1x2",
        "Home" : "Home",
        "Match nul" : "Nul",
        "Away" : "Away"
    },

    "" : {
        "title" : "Double Chance",
        "Home ou Match nul" : "Home ou Match nul",
        "Home FC ou Match nul" : "Home ou Match nul",
        "Home ou Away" : "Home ou Away",
        "Home FC ou Away" : "Home ou Away",
        'Home Wanderers ou Away' : "Home ou Away",
        'Home United Or Away City' : "Home ou Away",
        "Match nul ou Away" : "Match nul ou Away",
        'Egalité ou Away' : 'Match nul ou Away',
        "Home ou Away FC" :  "Home ou Away"
    },

    "Draw no bet" : {
        "title" : "Draw No Bet",
        "Home" : "Home",
        "Away" : "Away"
    },

    "Both teams to score" : {
        "title" : "Both Teams To Score",
        "Oui" : "Oui",
        "Non" : "Non"
    },

    "1st half - 1x2" : {
        "title" : "1st Half - 1x2",
        "Home" : "Home",
        "Match nul" : "Nul",
        "Away" : "Away"
    },

    "1st goal" : {
        "title" : "1st Goal",
        "Home" : "Home",
        "Aucun" : "No Goal",
        "Away" : "Away"
    },

    "Home To Win Both Halves" : {
        "title" : "Home To Win Both Halves",
        "Oui" : "Oui",
        "Non" : "Non"
    },

    "Away to win both halves" : {
        "title" : "Away To Win Both Halves",
        "Oui" : "Oui",
        "Non" : "Non"
    },

    "Home to win either half" : {
        "title" : "Home To Win Either Half",
        "Oui" : "Oui",
        "Non" : "Non"
    },

    "Away to win either half" : {
        "title" : "Away To Win Either Half",
        "Oui" : "Oui",
        "Non" : "Non"
    },

    "Highest scoring half" : {
        "title" : "Highest Scoring Half",
        "1ere mi-temps" : "1st",
        "2e mi-temps" : "2e",
        "Egalite" : "Same"
    },

    "" : {
        "title" : "Home Highest Scoring Half",
        "1ere mi-temps" : "1st",
        "2e mi-temps" : "2e",
        "Egalité" : "Same"
    },

    "" : {
        "title" : "Away Highest Scoring Half",
        "1ere mi-temps" : "1st",
        "2e mi-temps" : "2e",
        "Egalité" : "Same"
    },

    "" : {
        "title" : "1st Half - Both Teams To Score",
        "Oui" : "Oui",
        "Non" : "Non"
    }
}


################################################################################################################################################################

