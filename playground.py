import copy
from difflib import SequenceMatcher
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

s1 =SequenceMatcher(None, "Levadiakos", "Panathinaikos")
print(s1.ratio())