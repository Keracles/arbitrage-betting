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
            if len(bet['selections']) <= nb_outcome :
                outcomes = {}
                betTitle = bet["marketType"]
                betTitle = betTitle.replace(competitorName1, 'Home')
                betTitle = betTitle.replace(competitorName2, 'Away')
                for outcome in bet["selections"]:
                    outcome_name = outcome['name']
                    outcome_name = outcome_name.replace(competitorName1, 'Home')
                    outcome_name = outcome_name.replace(competitorName2, 'Away')
                    odd = round((int(outcome['currentPriceUp'])/int(outcome['currentPriceDown'])) + 1, 2)
                    outcomes[outcome_name] = odd
                bets[betTitle] = outcomes
    
    match = Match(competitorName1, competitorName2, bets)

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

build_match(url_match_test)