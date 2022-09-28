from bs4 import BeautifulSoup
from w3lib.html import replace_entities
from requests_html import HTMLSession
import re
from bookmakers.Important_Class import Match
import multiprocessing as mp
import time, os


################################################################################################################################################################
                            #Globals variables#
url_betclic = 'https://www.betclic.fr/'                    
url_ligue1 = "https://www.betclic.fr/football-s1/ligue-1-uber-eats-c4"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'}

################################################################################################################################################################
                                #Fonctions utiles#

def get_page(url):
    session = HTMLSession()
    r = session.get(url)
    r.html.render(sleep=1, scrolldown=1)
    soup = BeautifulSoup(r.html.find('*')[0].html, 'html.parser')
    return soup

################################################################################################################################################################
                                #Fonctions pricipales#

def MatchsLinksScrap(url_league):
    session = HTMLSession()
    r = session.get(url_league)
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
    bets_r = {}
    soup = get_page(url_match)
    bets = soup.find_all("sports-markets-single-market")
    #On obtients la liste des bets

    for bet in bets :
        outcomes = bet.find_all("p")
        if len(outcomes) <= 3:
            outcomes_r = {}
            betTitle = str(bet.find("h2").get_text().strip())
            for outcome in outcomes:
                outcome_name = str(outcome.get_text().strip())
                odd_part = bet.find("div", {"title" :  outcome_name})
                odd = float(odd_part.find("span").get_text().strip().replace(",", "."))

                outcomes_r[outcome_name] = odd
        bets_r[betTitle] = outcomes_r
    
    #On obtients le nom des équipes
    nom_page = soup.find("meta",{"name" : "title"})
    nom_page = nom_page["content"].split(' ')
    for k in range(len(nom_page)):
        if nom_page[k] == 'sur':
            competitorName1 = nom_page[k+1]
            competitorName2 = nom_page[k+3]

    match = Match(competitorName1, competitorName2,bets_r)

    return match

def get_league_matches():
    matches = []
    links = MatchsLinksScrap(url_ligue1)
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
