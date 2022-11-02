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
url_betclic = 'https://www.unibet.fr'                    
url_ligue1 = "https://www.unibet.fr/zones/v3/sportnode/markets.json?nodeId=435774672&filter=R%25C3%25A9sultat&marketname=R%25C3%25A9sultat%2520du%2520match"
url_match_test = 'https://www.unibet.fr/sport/football/event/lorient-lille-2553704_1.html'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'}

################################################################################################################################################################
                                #Fonctions utiles#

def get_page(url):
    session = HTMLSession()
    r = session.get(url)
    r.html.render(sleep=1, scrolldown=1)
    soup = BeautifulSoup(r.html.find('*')[0].html, 'html.parser')
    return soup

def get_json(num_match):
    r = requests.get(f"https://www.unibet.fr/zones/event.json?eventId={num_match}")
    return json.loads(r.text)
################################################################################################################################################################
                                #Fonctions pricipales#

def MatchsLinksScrap(url_league):
    links = []
    r =  requests.get(url_league)
    json_file = json.loads(r.text)
    for day in json_file["marketsByType"][0]['days']:
        for event in day["events"]:
            links.append(event["markets"][0]["eventFriendlyUrl"])
    return links


def build_match(url_match):
    #Get number
    split = url_match.split('-')
    split = split[-1]
    split = split.split('.')
    match_id = split[0]
    
    #On va récupérer et traiter le json
    json = get_json(match_id) 
    competitorName1 = json["eventHeader"]['homeName']
    competitorName2 = json["eventHeader"]['awayName']
    bets = {}
    
    for bet_out in json['marketClassList']:
        for bet in bet_out['marketList']:
            if len(bet['selections']) <=3 :
                outcomes = {}
                betTitle = bet["marketType"]
                for outcome in bet["selections"]:
                    outcome_name = outcome['name']
                    odd = round((int(outcome['currentPriceUp'])/int(outcome['currentPriceDown'])) + 1, 2)
                    outcomes[outcome_name] = odd
                bets[betTitle] = outcomes
    
    print(bets)
    match = Match(competitorName1, competitorName2, bets)

    return 


def get_league_matches():
    matches = []
    links = MatchsLinksScrap(url_ligue1)
    d = len(links)
    n = 1
    for link in links :
        url_match = url_betclic + link
        match = build_match(url_match)
        matches.append(match)
        print(f"Unibet avancement : {100*n/d}%")
        n += 1
    return matches

################################################################################################################################################################

print(get_page("https://www.netbet.fr/football/france/ligue-1-uber-eats/lens-toulouse"))