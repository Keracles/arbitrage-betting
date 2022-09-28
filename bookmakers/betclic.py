from bs4 import BeautifulSoup
import requests
import json
from w3lib.html import replace_entities
from requests_html import HTMLSession
import re

url = "https://www.betclic.fr/football-s1/ligue-1-uber-eats-c4/rennes-nantes-m3001509981"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'}


def LinksScrap():
    session = HTMLSession()
    r = session.get(url)
    r.html.render(sleep=1, keep_page=True, scrolldown=1)
    #HTML Parser
    links = []
    motif = re.compile("m3")
    for str in r.html.links :
        test = motif.search(str)
        if test :
            links.append(str)
    session.close()
    return links


def get_page():
    session = HTMLSession()
    r = session.get(url)
    r.html.render(scrolldown=1)
    soup = BeautifulSoup(r.html.find('*')[0].html, 'html.parser')
    return soup

def get_games():
    soup = get_page()
    paris = soup.find_all("sports-markets-single-market")
    for parie in paris :
        outcomes_names = parie.find_all("p")
        if len(outcomes_names) <= 4:
            name_pari = str(parie.find("h2").get_text().strip())
            print(name_pari)
            for outcome_name in outcomes_names:
                name_outcome = str(outcome_name.get_text().strip())
                print(name_outcome)
                odd_part = parie.find("div", {"title" :  name_outcome})
                odd = float(odd_part.find("span").get_text().strip().replace(",", "."))
                print(odd)
    return


get_games()