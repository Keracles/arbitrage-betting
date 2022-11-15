import copy
from difflib import SequenceMatcher
import requests

from bookmakers import unibet, Important_Class
import os 


print(os.path.abspath(r'bookmakers\trad_bookmakers\unibet.pkl'))

pattern_bets = {
    "1x2" : {
        "Home" : None,
        "Nul" : None,
        "Away" : None
    },


    "Draw no net" : {
        "Home" : None,
        "Away" : None
    },

    "Both teams to score" : {
        "Oui" : None,
        "Non" : None
    },

    "1st half - 1x2" : {
        "Home" : None,
        "Nul" : None,
        "Away" : None
    },

    "1st goal" : {
        "Home" : None,
        "No Goal" : None,
        "Away" : None
    },

    "Home To Win Both Halves" : {
        "Oui" : None,
        "Non" : None
    },

    "Away to win both halves" : {
        "Oui" : None,
        "Non" : None
    },

    "Home to win either half" : {
        "Oui" : None,
        "Non" : None
    },

    "Away to win either half" : {
        "Oui" : None,
        "Non" : None
    },

    "Highest scoring half" : {
        "1st" : None,
        "2e" : None,
        "Same" : None
    },

    "Home Highest Scoring Half" : {
        "1st" : None,
        "2e" : None,
        "Same" : None
    },

    "Away Highest Scoring Half" : {
        "1st" : None,
        "2e" : None,
        "Same" : None
    },

    "1st Half - Both Teams To Score" : {
        "Oui" : None,
        "Non" : None
    }
}

"""url = "https://www.enligne.parionssport.fdj.fr/paris-football/france/ligue-1-uber-eats/2926369/lorient-vs-paris-sg"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0 Win64 x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'}

r = requests.get(url, headers=headers)
print(r.text)"""
