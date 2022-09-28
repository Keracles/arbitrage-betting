from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import json
from Important_Class import Match
from w3lib.html import replace_entities




path_driver = r'C:\Users\kerac\Documents\Tools\drivers\geckodriver.exe'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'}
url = "https://www.winamax.fr/paris-sportifs/sports/1/7/4"
url_match = 'https://www.winamax.fr/paris-sportifs/match/34172157'

def pars_soup(html):
    #HTML Parser
    soup = BeautifulSoup(html, 'html.parser')
    return soup

def LinksScrap():
    driver = webdriver.Firefox(executable_path = path_driver)
    driver.get(url)
    html = driver.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
    soup = pars_soup(html)
    soup = soup.find_all("div", {"data-testid" : 'middleColumn'})[0]
    soup = soup.find_all("a")
    links = []
    for a in soup :
        if a.text :
            links.append(a['href'])
    return links
    

def get_page(url):
    #Make request
    res = requests.get(url, headers=headers)
    
    return res.text

def get_json():
    html = get_page(url_match)
    split1 = html.split("var PRELOADED_STATE =")[1]
    split2 = split1.split(";</script>")[0]
    return json.loads(split2)

def get_bets():
    bets = {}
    doublons = []
    json = get_json()
    outcomes = json["outcomes"]
    for id_bet, bet in json["bets"].items():
        bett = {}
        outcomes_one_bet = json["bets"][id_bet]["outcomes"]
        if len(outcomes_one_bet) < 4:
            for outcome in outcomes_one_bet :
                json_temp = outcomes[str(outcome)]
                name_issue = replace_entities(json_temp['label'])
                bett[name_issue]= json['odds'][str(outcome)]
        

            betTitle = json["bets"][id_bet]["betTitle"]
            if betTitle in bets.keys() :
                del bets[betTitle]
                doublons.append(betTitle)
            elif betTitle not in doublons :
                bets[betTitle] = bett
        

    return bets

print(LinksScrap())