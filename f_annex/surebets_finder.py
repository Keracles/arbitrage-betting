from bookmakers import Important_Class
import copy



def merge_dict(bet_bible):
    global pattern_bets
    bets_arrange = {}
    k = 0

    for bookmaker, bookmaker_dict in bet_bible.items():
        for name_league, matchs_league in bookmaker_dict.items():
            if name_league not in bets_arrange.keys():
                matchs_globaux = []
                for match_bookmaker in matchs_league:
                    match = crea_match_global(bookmaker, match_bookmaker)
                    matchs_globaux.append(match)
                bets_arrange[name_league] = matchs_globaux
            
            else :
                matchs_globaux = bets_arrange[name_league]
                matchs_ajout = []
                for match_bookmaker in matchs_league :
                    for match_global in matchs_globaux :
                        if match_bookmaker.comparaison(match_global):
                            for betTitle, outcomes in match_global.bets.items():
                                if betTitle in match_bookmaker.bets.keys():
                                    for outcome_name, outcome_odd in outcomes.items():
                                        if outcome_name in match_bookmaker.bets[betTitle].keys():
                                            match_global.bets[betTitle][outcome_name][bookmaker] = match_bookmaker.bets[betTitle][outcome_name]
                                        else :
                                            match_global.bets[betTitle][outcome_name][bookmaker] = None
                            else :
                                for outcome_name, outcome_odd in outcomes.items():
                                    match_global.bets[betTitle][outcome_name][bookmaker] = None
                            match_global.url.append(match_bookmaker.url)

                        else :
                            match = crea_match_global(bookmaker, match_bookmaker)
                            matchs_ajout.append(match)
                bets_arrange[name_league] + matchs_ajout

    return bets_arrange


def crea_match_global(bookmaker, match_bookmaker):
    global pattern_bets

    bets_match = copy.deepcopy(pattern_bets)
    for betTitle, outcomes in bets_match.items():
        if betTitle in match_bookmaker.bets.keys():
            for outcome_name, outcome_odd in outcomes.items():
                odds = {}
                if outcome_name in match_bookmaker.bets[betTitle].keys():
                    odds[bookmaker] = match_bookmaker.bets[betTitle][outcome_name]
                else :
                    odds[bookmaker] = None
                outcomes[outcome_name] = odds
        else :
            for outcome_name, outcome_odd in outcomes.items():
                odds = {}
                odds[bookmaker] = None
                outcomes[outcome_name] = odds
    match = Important_Class.Match(match_bookmaker.home, match_bookmaker.away, bets_match, [match_bookmaker.url])
    return match 



def finder(bets_arrange):
    findings = []

    for name_league, matchs_league in bets_arrange.items():
        for match in matchs_league :
            for betTitle, outcomes in match.bets.items():
                test_arbitrage = {}
                for outcome_name, odds in outcomes.items():
                    test_arbitrage[outcome_name] = best_odd(odds)
                
                ratio = calcul_arbitrage(test_arbitrage) 
                if ratio != None:
                    str =   [ratio,f"******************************************************* \n League {name_league} \n pour le match {match.get_name()} \n Coeff de {ratio}% \n pour le bet {betTitle} \n avec les odds {test_arbitrage} \n Viens parier idiots {match.url}"]
                    findings.append(str)
    
    findings = sorted(findings, key=getKey)
    findings_sort = []
    for ele in findings:
        findings_sort.append(ele[1])
    return findings_sort

def getKey(element):
    return element[0]

def best_odd(odds):
    best_odd = None
    best_bookmaker = None
    for bookmaker, odd in odds.items():
        if odd != None:
            if best_odd == None :
                best_odd = odd
                best_bookmaker = bookmaker
            elif odd > best_odd :
                best_odd = odd
                best_bookmaker = bookmaker
    return best_odd, best_bookmaker

def calcul_arbitrage(dict_best_odd):
    ratio = 0
    for outcome_name, (odd, bookmaker) in dict_best_odd.items():
        if odd == None :
            return None
        ratio += 1/float(odd)
    if ratio < 1 :
        coeff = round((1 - ratio)*100,2)
        return coeff

    else :
        return None
    



pattern_bets = {
    "1x2" : {
        "Home" : None,
        "Nul" : None,
        "Away" : None
    },


    "Draw No Bet" : {
        "Home" : None,
        "Away" : None
    },

    "Both Teams To Score" : {
        "Oui" : None,
        "Non" : None
    },

    "1st Half - 1x2" : {
        "Home" : None,
        "Nul" : None,
        "Away" : None
    },

    "1st Goal" : {
        "Home" : None,
        "No Goal" : None,
        "Away" : None
    },

    "Home To Win Both Halves" : {
        "Oui" : None,
        "Non" : None
    },

    "Away To Win Both Halves" : {
        "Oui" : None,
        "Non" : None
    },

    "Home To Win Either Half" : {
        "Oui" : None,
        "Non" : None
    },

    "Away To Win Either Half" : {
        "Oui" : None,
        "Non" : None
    },

    "Highest Scoring Half" : {
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


################################################################################################################################################################

