import unidecode
import pickle
from difflib import SequenceMatcher
from f_annex import param



debug = param.debug
######################################################## CLASSES ########################################################

class Match :
    def __init__(self,eq1:str,eq2:str,bets:dict, url:str) -> None:
        self.home = eq1
        self.away = eq2
        self.bets = bets
        self.url = url
    
    def get_name(self):
        return self.home + " / " + self.away
    
    def show(self):
        print(f"Match : {self.home} vs {self.away} \n Url : {self.url} \n Bets : \n {self.bets}")
        return 
    

    def comparaison(match1, match2):
        s1 = SequenceMatcher(None, match1.home, match2.home)
        s2 = SequenceMatcher(None, match1.away, match2.away)
        if s1.ratio() > 0.7 and s2.ratio() > 0.5:
            return True
        else :
            return False 



 #Format des strings   
def format_espace(str):
    new_str = ""
    for mot in str.split(" "):
        if mot != '':
            new_str += " " + mot
    return new_str

def format_name_g(str):
    if str == None :
        return None 
    str = unidecode.unidecode(str)
    str = str.strip()
    str = str.lower()
    str = str.capitalize()
    return str

def format_replace(bookmaker, str, name_league):
    if bookmaker == "unibet" : 
        loaded_dict = trad_unibet
    elif bookmaker == "winamax" : 
        loaded_dict = trad_winamax
    elif bookmaker == "zebet" : 
        loaded_dict = trad_zebet
    elif bookmaker == "netbet" : 
        loaded_dict = trad_netbet
    elif bookmaker == "betclic" : 
        loaded_dict = trad_betclic

    if name_league not in loaded_dict.keys():
        loaded_dict[name_league] = {}

    for cle, valeur in loaded_dict[name_league].items():
        str = str.replace(cle, valeur)
    return str

def format_name(str, competitorName1, competitorName2, bookmaker, name_league):
    #Remplacement par bookmaker
    if bookmaker == "unibet" : 
        str  = format_replace("unibet", str, name_league)
    elif bookmaker == 'winamax':
        str  = format_replace("winamax", str, name_league)
    elif bookmaker == 'betclic' :
        str  = format_replace("betclic", str, name_league)
    elif bookmaker == 'zebet' :
        str  = format_replace("zebet", str, name_league)
    elif bookmaker == 'netbet' :
        str  = format_replace("netbet", str, name_league)
    
    #Home / Away
    str = str.replace(competitorName1, 'Home')
    str = str.replace(competitorName2, 'Away')
    str = str.replace(competitorName1.lower(), 'Home')
    str = str.replace(competitorName2.lower(), 'Away')

    return str

#Check des trads
def check_outcome(betTitle, competitorName1, competitorName2, outcome_name, outcome_name_old, trad_bets, bookmaker, name_league):
    boucle = True
    k = 0         
    while boucle and k < 3 :
        try :
            outcome_name = trad_bets[betTitle][outcome_name]
            boucle = False
        except KeyError : 
            print("-------------------------------------- KEY ERROR SPOTTED ---------------------------------------------")
            print(f"-------------------------------------- {bookmaker} ---------------------------------------------")
            print(f"pour le bet {betTitle}, \n Team en présence : {competitorName1} et {competitorName2} \n str rentré {outcome_name_old}, \n Transformé en {outcome_name}")
            s1 = SequenceMatcher(None, outcome_name_old, competitorName1)
            s2 = SequenceMatcher(None, outcome_name_old, competitorName2)
            if s2.ratio() > s1.ratio() :
                print(f"On rajoute la règle : {outcome_name_old} en {competitorName2}")
                with open(f'bookmakers\\trad_bookmakers\{bookmaker}.pkl', 'rb') as f:
                    loaded_dict = pickle.load(f)
                    f.close()
                with open(f'bookmakers\\trad_bookmakers\{bookmaker}.pkl', 'wb') as f:
                    if name_league not in loaded_dict.keys():
                        loaded_dict[name_league] = {}
                    loaded_dict[name_league][outcome_name_old] = competitorName2
                    pickle.dump(loaded_dict, f)
                    f.close()
            else :
                print(f"On rajoute la règle : {outcome_name_old} en {competitorName1}")
                with open(f'bookmakers\\trad_bookmakers\{bookmaker}.pkl', 'rb') as f:
                    loaded_dict = pickle.load(f)
                    f.close()
                with open(f'bookmakers\\trad_bookmakers\{bookmaker}.pkl', 'wb') as f:
                    if name_league not in loaded_dict.keys():
                        loaded_dict[name_league] = {}
                    loaded_dict[name_league][outcome_name_old] = competitorName1
                    pickle.dump(loaded_dict, f)
                    f.close()
            actualisation_trad(bookmaker)
            outcome_name = format_name(outcome_name, competitorName1, competitorName2, bookmaker, name_league)
            k+=1
        except :
            raise
    return outcome_name






def actualisation_trad(bookmaker):
    global trad_unibet, trad_winamax, trad_betclic, trad_netbet, trad_zebet

    if bookmaker == "unibet" or bookmaker == "all" :
        with open(r'bookmakers\trad_bookmakers\unibet.pkl', 'rb') as f:
            trad_unibet = pickle.load(f)
            f.close()
    if bookmaker == "winamax" or bookmaker == "all" :
        with open(r'bookmakers\trad_bookmakers\winamax.pkl', 'rb') as f:
            trad_winamax = pickle.load(f)
            f.close()
    if bookmaker == "betclic" or bookmaker == "all" :
        with open(r'bookmakers\trad_bookmakers\betclic.pkl', 'rb') as f:
            trad_betclic = pickle.load(f)
            f.close()
    if bookmaker == "netbet" or bookmaker == "all" :
        with open(r'bookmakers\trad_bookmakers\netbet.pkl', 'rb') as f:
            trad_netbet = pickle.load(f)
            f.close()
    if bookmaker == "zebet" or bookmaker == "all" :
        with open(r'bookmakers\trad_bookmakers\zebet.pkl', 'rb') as f:
            trad_zebet = pickle.load(f)
            f.close()
    

#Traduction
trad_unibet = {}
trad_winamax = {}
trad_betclic = {}
trad_netbet = {}
trad_zebet = {}

actualisation_trad("all")