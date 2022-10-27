from bs4 import BeautifulSoup
import requests
from w3lib.html import replace_entities
from requests_html import HTMLSession
import re
from Important_Class import Match
import multiprocessing as mp
import json


################################################################################################################################################################
                            #Globals variables#
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
    return soup

def get_json(num_match):
    r = requests.get(f"https://offer.cdn.begmedia.com/api/pub/v5/events/{num_match}?application=2&countrycode=fr&language=fr&sitecode=frfr")
    return json.loads(r.text)
################################################################################################################################################################
                                #Fonctions pricipales#

def MatchsLinksScrap(pattern):
    session = HTMLSession()
    r = session.get(url_betclic + pattern)
    r.html.render(sleep=1, scrolldown=1)
    #HTML Parser
    links = []
    motif = re.compile("m3")
    for str in r.html.links :
        test = motif.search(str)
        if test :
            links.append(str)
    session.close()
    return links


def build_match(url_match):
    #Obtenir le numéro du match
    split = url_match.split('-')
    num = split[-1]
    match_id = int(num[1:len(num)])

    #On va récupérer et traiter le json
    json = get_json(match_id) 
    competitorName1 = json["contestants"][0]['name']
    competitorName2 = json["contestants"][1]['name']
    bets = {}
    
    for bet in json['grouped_markets']:
        if 'markets' in bet.keys():
            bet = bet['markets'][0]
            if len(bet['selections']) <=nb_outcome :
                outcomes = {}
                betTitle = bet["name"]
                betTitle = betTitle.replace(competitorName1, 'Home')
                betTitle = betTitle.replace(competitorName2, 'Away')
                if len(bet["selections"]) == 1:
                    if len(bet["selections"][0]) <=nb_outcome :
                        for outcome in bet["selections"][0]:
                            outcome_name = outcome['name']
                            outcome_name = outcome_name.replace(competitorName1, 'Home')
                            outcome_name = outcome_name.replace(competitorName2, 'Away')
                            odd = outcome['odds']
                            outcomes[outcome_name] = odd
                        bets[betTitle] = outcomes

                else : 
                    for outcome in bet["selections"]:
                        outcome = outcome[0]
                        outcome_name = outcome['name']
                        outcome_name = outcome_name.replace(competitorName1, 'Home')
                        outcome_name = outcome_name.replace(competitorName2, 'Away')
                        odd = outcome['odds']
                        outcomes[outcome_name] = odd
                    bets[betTitle] = outcomes
    match = Match(competitorName1, competitorName2, bets)
    print(bets)
    return match


def get_league_matches(pattern):
    matches = []
    links = MatchsLinksScrap(pattern)
    d = len(links)
    n = 1
    for link in links :
        url_match = url_betclic + link
        match = build_match(url_match)
        matches.append(match)
        print(f"Betclic avancement : {100*n/d}%")
        n += 1
    return matches

################################################################################################################################################################
build_match(url_match_test)