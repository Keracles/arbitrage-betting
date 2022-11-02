from bs4 import BeautifulSoup
import requests
from w3lib.html import replace_entities
from requests_html import HTMLSession
from bookmakers import Important_Class
import json
from difflib import SequenceMatcher
import pickle


################################################################################################################################################################
                            #Globals variables#
bookmaker = "unibet"
url_unibet = 'https://www.unibet.fr'                    
api_ligue1 = "https://www.unibet.fr/zones/v3/sportnode/markets.json?nodeId=435774672&filter=R%25C3%25A9sultat&marketname=R%25C3%25A9sultat%2520du%2520match"
api_pl = 'https://www.unibet.fr/zones/v3/sportnode/markets.json?nodeId=703695255&filter=R%C3%A9sultat&marketname=R%C3%A9sultat%20du%20match'
url_match_test = 'https://www.unibet.fr/sport/football/event/leicester-manchester-city-2576687_1.html'
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
    r = requests.get(f"https://www.unibet.fr/zones/event.json?eventId={num_match}")
    return json.loads(r.text)
################################################################################################################################################################
                                #Fonctions pricipales#

def MatchsLinksScrap(api_league):
    links = []
    r =  requests.get(api_league)
    json_file = json.loads(r.text)
    for day in json_file["marketsByType"][0]['days']:
        for event in day["events"]:
            links.append(event["markets"][0]["eventFriendlyUrl"])
    r.close()
    return links


def build_match(url_match):
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
                betTitle = Important_Class.format_name(betTitle, competitorName1, competitorName2,bookmaker)
                if betTitle in trad_bets.keys() : 
                    for outcome in bet["selections"]:
                        outcome_name = Important_Class.format_name_g(outcome['name'])
                        outcome_name_old = outcome_name
                        outcome_name = Important_Class.format_name(outcome_name, competitorName1, competitorName2, bookmaker)
                        odd = round((float(outcome['currentPriceUp'])/int(outcome['currentPriceDown'])) + 1, 2)

                        try :
                            outcome_name = trad_bets[betTitle][outcome_name]
                            outcomes[outcome_name] = odd
                        except KeyError : 
                            print(f"KEY ERROR SPOTTED, str rentré {outcome_name_old}, Transformé en {outcome_name} Team en présence : {competitorName1} et {competitorName2}")
                            s1 = SequenceMatcher(None, outcome_name_old, competitorName1)
                            s2 = SequenceMatcher(None, outcome_name_old, competitorName2)
                            if s2.ratio() > s1.ratio() :
                                print(f"On rajoute la règle : {outcome_name_old} en {competitorName2}")
                                with open(f'bookmakers\\trad_bookmakers\{bookmaker}.pkl', 'rb') as f:
                                    loaded_dict = pickle.load(f)
                                    f.close()
                                with open(f'bookmakers\\trad_bookmakers\{bookmaker}.pkl', 'wb') as f:
                                    loaded_dict[outcome_name_old] = competitorName2
                                    pickle.dump(loaded_dict, f)
                                    f.close()
                            else :
                                print(f"On rajoute la règle : {outcome_name_old} en {competitorName1}")
                                with open(f'bookmakers\\trad_bookmakers\{bookmaker}.pkl', 'rb') as f:
                                    loaded_dict = pickle.load(f)
                                    f.close()
                                with open(f'bookmakers\\trad_bookmakers\{bookmaker}.pkl', 'wb') as f:
                                    loaded_dict[outcome_name_old] = competitorName2
                                    pickle.dump(loaded_dict, f)
                                    f.close()
                            Important_Class.actualisation_trad(bookmaker)
                        except :
                            raise



                    betTitle = trad_bets[betTitle]["title"]
                    bets[betTitle] = outcomes
    
    match = Important_Class.Match(competitorName1, competitorName2, bets)

    return match


def get_league_matches(api_league):
    matches = []
    links = MatchsLinksScrap(api_league)
    d = len(links)
    n = 1
    for link in links :
        url_match = url_unibet + link
        match = build_match(url_match)
        matches.append(match)
        print(f"Unibet avancement : {100*n/d}%")
        n += 1
    return matches


################################################################################################################################################################
pattern_foot = {
    "allemagne-1" : "https://www.unibet.fr/zones/v3/sportnode/markets.json?nodeId=116432547&filter=R%C3%A9sultat&marketname=R%C3%A9sultat%20du%20match",
    "allemagne-2" : "https://www.unibet.fr/zones/v3/sportnode/markets.json?nodeId=30914428&filter=R%C3%A9sultat&marketname=R%C3%A9sultat%20du%20match",
    "angleterre-1" : "https://www.unibet.fr/zones/v3/sportnode/markets.json?nodeId=116875930&filter=R%C3%A9sultat&marketname=R%C3%A9sultat%20du%20match",
    "angleterre-2" : "https://www.unibet.fr/zones/v3/sportnode/markets.json?nodeId=116876043&filter=R%C3%A9sultat&marketname=R%C3%A9sultat%20du%20match",
    "australie" : "https://www.unibet.fr/zones/v3/sportnode/markets.json?nodeId=702488951&filter=R%C3%A9sultat&marketname=R%C3%A9sultat%20du%20match",
    "autriche" : "https://www.unibet.fr/zones/v3/sportnode/markets.json?nodeId=30990209&filter=R%C3%A9sultat&marketname=R%C3%A9sultat%20du%20match",
    "belgique" : "https://www.unibet.fr/zones/v3/sportnode/markets.json?nodeId=31087161&filter=R%C3%A9sultat&marketname=R%C3%A9sultat%20du%20match",
    "bresil" : "https://www.unibet.fr/zones/v3/sportnode/markets.json?nodeId=30918991&filter=R%C3%A9sultat&marketname=R%C3%A9sultat%20du%20match",
    "bulgarie" : "https://www.unibet.fr/zones/v3/sportnode/markets.json?nodeId=32152172&filter=R%C3%A9sultat&marketname=R%C3%A9sultat%20du%20match",
    "chili" : "https://www.unibet.fr/zones/v3/sportnode/markets.json?nodeId=242528229&filter=R%C3%A9sultat&marketname=R%C3%A9sultat%20du%20match",
    "danemark" : "https://www.unibet.fr/zones/v3/sportnode/markets.json?nodeId=30910871&filter=R%C3%A9sultat&marketname=R%C3%A9sultat%20du%20match",
    "ecosse" : "https://www.unibet.fr/zones/v3/sportnode/markets.json?nodeId=31413185&filter=R%C3%A9sultat&marketname=R%C3%A9sultat%20du%20match",
    "espagne-1" : "https://www.unibet.fr/zones/v3/sportnode/markets.json?nodeId=116876665&filter=R%C3%A9sultat&marketname=R%C3%A9sultat%20du%20match",
    "espagne-2" : "https://www.unibet.fr/zones/v3/sportnode/markets.json?nodeId=32184870&filter=R%C3%A9sultat&marketname=R%C3%A9sultat%20du%20match",
    "usa" : "https://www.unibet.fr/zones/v3/sportnode/markets.json?nodeId=31618329&filter=R%C3%A9sultat&marketname=R%C3%A9sultat%20du%20match",
    "europe-1" : "https://www.unibet.fr/zones/v3/sportnode/markets.json?nodeId=445490388&filter=R%C3%A9sultat&marketname=R%C3%A9sultat%20du%20match",
    "europe-2" : "https://www.unibet.fr/zones/v3/sportnode/markets.json?nodeId=445503791&filter=R%C3%A9sultat&marketname=R%C3%A9sultat%20du%20match",
    "france-1" : "https://www.unibet.fr/zones/v3/sportnode/markets.json?nodeId=703695044&filter=R%C3%A9sultat&marketname=R%C3%A9sultat%20du%20match",
    "france-2" : "https://www.unibet.fr/zones/v3/sportnode/markets.json?nodeId=703695047&filter=R%C3%A9sultat&marketname=R%C3%A9sultat%20du%20match",
    "grece" : "https://www.unibet.fr/zones/v3/sportnode/markets.json?nodeId=32690446&filter=R%C3%A9sultat&marketname=R%C3%A9sultat%20du%20match",
    "israel" : "https://www.unibet.fr/zones/v3/sportnode/markets.json?nodeId=33158892&filter=R%C3%A9sultat&marketname=R%C3%A9sultat%20du%20match",
    "italie-1" : "https://www.unibet.fr/zones/v3/sportnode/markets.json?nodeId=116876945&filter=R%C3%A9sultat&marketname=R%C3%A9sultat%20du%20match",
    "italie-2" : "https://www.unibet.fr/zones/v3/sportnode/markets.json?nodeId=32975099&filter=R%C3%A9sultat&marketname=R%C3%A9sultat%20du%20match",
    "japon" : "https://www.unibet.fr/zones/v3/sportnode/markets.json?nodeId=30911324&filter=R%C3%A9sultat&marketname=R%C3%A9sultat%20du%20match",
    "norvege" : "https://www.unibet.fr/zones/v3/sportnode/markets.json?nodeId=30910939&filter=R%C3%A9sultat&marketname=R%C3%A9sultat%20du%20match",
    "pays-bas" : "https://www.unibet.fr/zones/v3/sportnode/markets.json?nodeId=31086981&filter=R%C3%A9sultat&marketname=R%C3%A9sultat%20du%20match",
    "pologne" : "https://www.unibet.fr/zones/v3/sportnode/markets.json?nodeId=31921084&filter=R%C3%A9sultat&marketname=R%C3%A9sultat%20du%20match",
    "portugal-1" : "https://www.unibet.fr/zones/v3/sportnode/markets.json?nodeId=436203630&filter=R%C3%A9sultat&marketname=R%C3%A9sultat%20du%20match",
    "portugal-2" : "https://www.unibet.fr/zones/v3/sportnode/markets.json?nodeId=32000383&filter=R%C3%A9sultat&marketname=R%C3%A9sultat%20du%20match",
    "reptcheque" : "https://www.unibet.fr/zones/v3/sportnode/markets.json?nodeId=31413119&filter=R%C3%A9sultat&marketname=R%C3%A9sultat%20du%20match",
    "roumanie" : "https://www.unibet.fr/zones/v3/sportnode/markets.json?nodeId=31921477&filter=R%C3%A9sultat&marketname=R%C3%A9sultat%20du%20match",
    "slovenie" : "https://www.unibet.fr/zones/v3/sportnode/markets.json?nodeId=30990203&filter=R%C3%A9sultat&marketname=R%C3%A9sultat%20du%20match",
    "suede" : "https://www.unibet.fr/zones/v3/sportnode/markets.json?nodeId=30911983&filter=R%C3%A9sultat&marketname=R%C3%A9sultat%20du%20match",
    "suisse" : "https://www.unibet.fr/zones/v3/sportnode/markets.json?nodeId=30917369&filter=R%C3%A9sultat&marketname=R%C3%A9sultat%20du%20match",
    "turquie" : "https://www.unibet.fr/zones/v3/sportnode/markets.json?nodeId=58869345&filter=R%C3%A9sultat&marketname=R%C3%A9sultat%20du%20match"
}


trad_bets = {
    "1x2" : {
        "title" : "1x2",
        "Home" : "Home",
        "Match nul" : "Nul",
        "Away" : "Away"
    },

    "Double Chance" : {
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

    "Draw No Bet" : {
        "title" : "Draw No Bet",
        "Home" : "Home",
        "Away" : "Away"
    },

    "Both Teams To Score" : {
        "title" : "Both Teams To Score",
        "Oui" : "Oui",
        "Non" : "Non"
    },

    "1st Half - 1x2" : {
        "title" : "1st Half - 1x2",
        "Home" : "Home",
        "Match nul" : "Nul",
        "Away" : "Away"
    },

    "1st Goal" : {
        "title" : "1st Goal",
        "Home" : "Home",
        "Aucun" : "No Goal",
        "Away" : "Away"
    },

    "" : {
        "title" : "Home To Win Both Halves",
        "Oui" : "Oui",
        "Non" : "Non"
    },

    "Home To Win Both Halves" : {
        "title" : "Away To Win Both Halves",
        "Oui" : "Oui",
        "Non" : "Non"
    },

    "Home To Win Either Half" : {
        "title" : "Home To Win Either Half",
        "Oui" : "Oui",
        "Non" : "Non"
    },

    "Away To Win Either Half" : {
        "title" : "Away To Win Either Half",
        "Oui" : "Oui",
        "Non" : "Non"
    },

    "Highest Scoring Half" : {
        "title" : "Highest Scoring Half",
        "1ère Mi-temps" : "1st",
        "2e Mi-temps" : "2e",
        "Egalité" : "Same"
    },

    "" : {
        "title" : "Home Highest Scoring Half",
        "1ère Mi-temps" : "1st",
        "2e Mi-temps" : "2e",
        "Egalité" : "Same"
    },

    "" : {
        "title" : "Away Highest Scoring Half",
        "1ère Mi-temps" : "1st",
        "2e Mi-temps" : "2e",
        "Egalité" : "Same"
    },

    "" : {
        "title" : "1st Half - Both Teams To Score",
        "Oui" : "Oui",
        "Non" : "Non"
    }
}


################################################################################################################################################################

