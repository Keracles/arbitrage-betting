from bs4 import BeautifulSoup
import requests
from w3lib.html import replace_entities
from requests_html import HTMLSession
import re
from Important_Class import Match


################################################################################################################################################################
                            #Globals variables#
url_zebet = 'https://www.zebet.fr'                    
pattern_ligue1 = "/fr/competition/96-ligue_1_uber_eats"
pattern_pl = '/fr/competition/94-premier_league'
url_match_test = 'https://www.zebet.fr/fr/event/m2ai2-lens_toulouse'
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
    r = session.get(url_zebet + pattern)
    r.html.render(sleep=1, keep_page=True, scrolldown=1)
    #HTML Parser
    links = []
    motif = re.compile("/fr/event/")
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
    soup =  soup.find('div', id='event')
    soup = soup.find('div', 'uk-grid uk-grid-small uk-grid-width-1-2 resp-1600')
    soup = soup.find_all('div', re.compile('uk-accordion-wrapper'))
  
    bets = {}
    #On va récupérer et traiter la soup
    for bet_boxe in soup:

        if bet_boxe.find_all('div', re.compile('grouped_questions')) != []:
            a=1
        elif bet_boxe.find_all('div', re.compile('content over_under_sameTP')) == []:
            bet_boxe = bet_boxe.find_all('div', re.compile('item-content'))
            for bet in bet_boxe :
                betTitle = bet.find("div", re.compile('bet-question')).contents[1].strip()
                bet = bet.find('div', re.compile('uk'))
                bet_outcomes = bet.find_all('div', re.compile('bet'))
                if len(bet_outcomes) <= nb_outcome:
                    outcomes = {}
                    for outcome in bet_outcomes:
                        outcome_name = outcome.find('span', re.compile('pmq-cote-acteur ')).contents[0].strip()
                        odd = float(outcome.find('span', 'pmq-cote').contents[0].strip().replace(',', '.'))
                        outcomes[outcome_name] = odd
                    bets[betTitle] = outcomes
        else :
            bet_boxe = bet_boxe.find_all('div', re.compile('content over_under_sameTP'))
            if len(bet_boxe) == 1:
                bet_boxe = bet_boxe[0]
                betTitle = bet_boxe.find("div", re.compile('bet-question')).contents[1].strip()
                bet_boxe = bet_boxe.find_all('div', re.compile('item-content'))
                for bet in bet_boxe :
                    bet = bet.find('div', re.compile('uk'))
                    if bet != None:
                        bet_outcomes = bet.find_all('div', re.compile('bet'))
                        if len(bet_outcomes) <= nb_outcome:
                            outcomes = {}
                            for outcome in bet_outcomes:
                                outcome_name = outcome.find('span', re.compile('pmq-cote-acteur ')).contents[0].strip()
                                odd = float(outcome.find('span', 'pmq-cote').contents[0].strip().replace(',', '.'))
                                outcomes[outcome_name] = odd
                            bets[betTitle] = outcomes
            else : 
                for bet in bet_boxe :
                    betTitle = bet.find("div", re.compile('bet-question')).contents[1].strip()
                    bet = bet.find('div', re.compile('uk'))
                    bet_outcomes = bet.find_all('div', re.compile('bet'))
                    if len(bet_outcomes) <= nb_outcome:
                        outcomes = {}
                        for outcome in bet_outcomes:
                            outcome_name = outcome.find('span', re.compile('pmq-cote-acteur ')).contents[0].strip()
                            odd = float(outcome.find('span', 'pmq-cote').contents[0].strip().replace(',', '.'))
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
    print(bets_replace)
    match = Match(competitorName1, competitorName2, bets_replace)
    return match


def get_league_matches(pattern):
    matches = []
    links = MatchsLinksScrap(pattern)
    d = len(links)
    n = 1
    for link in links :
        url_match = link
        match = build_match(url_zebet + url_match)
        matches.append(match)
        print(f"Zebet avancement : {100*n/d}%")
        n += 1
    return matches

################################################################################################################################################################
build_match(url_match_test)