from bs4 import BeautifulSoup
import requests
from w3lib.html import replace_entities
from requests_html import HTMLSession
import re
from Important_Class import Match


################################################################################################################################################################
                            #Globals variables#
url_netbet = 'https://www.netbet.fr'                    
pattern_ligue1 = "/football/france/ligue-1-uber-eats/"
pattern_pl = "/football/angleterre/premier-league/"
pattern_israel = '/football/israel/ligat-ha-al/'
url_match_test = 'https://www.netbet.fr/football/france/ligue-1-uber-eats/lens-toulouse'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'}
nb_outcome = 3
################################################################################################################################################################
                                #Fonctions utiles#

def get_page(url): #OKAY
    #Make request
    res = requests.get(url, headers=headers, timeout=5)
    res.close()
    return res.text

################################################################################################################################################################
                                #Fonctions pricipales#

def MatchsLinksScrap(pattern): #OKAY
    session = HTMLSession()
    r = session.get(url_netbet + pattern)
    r.html.render(sleep=1, keep_page=True, scrolldown=1)
    #HTML Parser
    links = []
    motif = re.compile(pattern)
    for str in r.html.links :
        test = motif.search(str)
        if test :
            links.append(str)
    session.close()
    r.close()
    return links


def build_match(url_match):
    #Get soup
    soup = BeautifulSoup(get_page(url_match), 'html.parser')
    soup =  soup.find(id='main')
    soup = soup.find_all('li', 'uk-open')

    bets = {}
    #On va récupérer et traiter la soup
    for bet_boxe in soup:
        bet_boxTitle = bet_boxe.find('div', 'title uk-accordion-title')
        bet_boxTitle = bet_boxe.find('span', 'label').contents[0]
        bet_boxe = bet_boxe.find("div", "uk-accordion-content")
        if len(bet_boxe.find_all("div", "nb-event_odds_wrapper")) <= 1:
            for bet in bet_boxe.find_all("div", "nb-event_odds_wrapper"):
                bet_outcomes = bet.find_all('a')
                if len(bet_outcomes) <= nb_outcome and len(bet_outcomes) > 1:
                    betTitle = bet_boxTitle
                    outcomes = {}
                    for outcome in bet_outcomes:
                        outcome_name = ''.join(outcome.find('div', 'nb-odds_choice').contents)
                        odd = outcome.find('div', 'nb-odds_amount').contents[0]
                        outcomes[outcome_name] = odd
                    bets[betTitle] = outcomes
        else :
            for bet in bet_boxe.find_all("div", "nb-event_odds_wrapper"):
                bet_outcomes = bet.find_all('a')
                if len(bet_outcomes) <= nb_outcome and len(bet_outcomes) > 1: 
                    betTitle =  bet_boxTitle + ' ' + bet.find('p').contents[0]
                    outcomes = {}
                    for outcome in bet_outcomes:
                        outcome_name = ''.join(outcome.find('div', 'nb-odds_choice').contents)
                        odd = float(outcome.find('div', 'nb-odds_amount').contents[0].replace(",", '.'))
                        outcomes[outcome_name] = odd
                    bets[betTitle] = outcomes
    competitorName1 = list(bets['Qui va gagner le match ?'].keys())[0]
    competitorName2 = list(bets['Qui va gagner le match ?'].keys())[-1]

    bets_replace = {}
    for i, (betTitle, outcomes) in enumerate(bets.items()):
        betTitle_replace = betTitle.replace(competitorName1, 'Home')
        betTitle_replace = betTitle_replace.replace(competitorName2, 'Away')
        outcomes_replace = {}
        for i, (outcome_name, odd) in enumerate(outcomes.items()):
            outcome_name_replace = outcome_name.replace(competitorName1, 'Home')
            outcome_name_replace = outcome_name_replace.replace(competitorName2, 'Away')
            outcomes_replace[outcome_name_replace] = odd
        bets_replace[betTitle_replace] = outcomes_replace

    match = Match(competitorName1, competitorName2, bets_replace)
    return match


def get_league_matches(pattern):
    matches = []
    links = MatchsLinksScrap(pattern)
    d = len(links)
    n = 1
    for link in links :
        url_match =link
        match = build_match(url_netbet + url_match)
        matches.append(match)
        print(f"Netbet avancement : {100*n/d}%")
        n += 1
    return matches

################################################################################################################################################################

build_match(url_match_test)