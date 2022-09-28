from bs4 import BeautifulSoup
import requests
import json
from Important_Class import Match
from w3lib.html import replace_entities
from requests_html import HTMLSession
import re



################################################################################################################################################################
                            #Globals variables#

path_driver = r'C:\Users\kerac\Documents\Tools\drivers\phantomjs.exe'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'}
url = "https://www.winamax.fr/paris-sportifs/sports/1/7/4"

################################################################################################################################################################
                                #Fonctions utiles#

def get_page(url):
    #Make request
    res = requests.get(url, headers=headers)
    return res.text

def get_json(url_match):
    html = get_page(url_match)
    split1 = html.split("var PRELOADED_STATE =")[1]
    split2 = split1.split(";</script>")[0]
    return json.loads(split2)

################################################################################################################################################################
                                #Fonctions pricipales#

def LeagueLinksScrap():
    session = HTMLSession()
    r = session.get(url)
    r.html.render(sleep=1, keep_page=True, scrolldown=1)
    #HTML Parser
    links = []
    motif = re.compile("/paris-sportifs/sports/1/7")
    for str in r.html.links :
        test = motif.search(str)
        if test :
            links.append(str)
    session.close()
    return links

def MatchsLinksScrap():
    session = HTMLSession()
    r = session.get(url)
    r.html.render(sleep=1, keep_page=True, scrolldown=1)
    #HTML Parser
    links = []
    motif = re.compile("/paris-sportifs/match")
    for str in r.html.links :
        test = motif.search(str)
        if test :
            links.append(str)
    session.close()
    return links
    


def build_match(url_match):
    json = get_json(url_match)
    matches_id = list(json["matches"].keys())
    competitorName1 = json["matches"][matches_id[-1]]['competitor1Name']
    competitorName2 = json["matches"][matches_id[-1]]['competitor2Name']
    bets_id = json["matches"][matches_id[-1]]['bets']
    bets = {}
    #On obtients la liste des bets
    for bet_id in bets_id:
        bet_id = str(bet_id)
        outcomes = {}
        betTitle = json["bets"][bet_id]["betTitle"]
        outcomes_id = json["bets"][bet_id]["outcomes"]

        if len(outcomes_id) <=3 :
            for outcome_id in outcomes_id:
                outcome_id = str(outcome_id)
                outcome_name = json['outcomes'][outcome_id]["label"]
                odd = json["odds"][outcome_id]
                outcomes[outcome_name] = odd
            bets[betTitle] = outcomes
    match = Match(competitorName1, competitorName2, bets)
    return match


def get_league_matches():
    matches = []
    links = MatchsLinksScrap()
    for link in links:
        url = "https://www.winamax.fr" + link
        match = build_match(url)
        matches.append(match)
    return matches

################################################################################################################################################################


print(get_league_matches())

        