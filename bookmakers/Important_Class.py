import unidecode
import pickle
from difflib import SequenceMatcher
import os 
######################################################## CLASSES ########################################################

class Match :
    def __init__(self,eq1:str,eq2:str,bets:dict) -> None:
        self.eq1 = eq1
        self.eq2 = eq2
        self.bets = bets
    
    def get_name(self):
        return self.eq1 + " / " + self.eq2
    
    def show(self):
        print(f"Match : {self.eq1} vs {self.eq2} \n Bets : \n {self.bets}")
        return 

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

def format_replace(bookmaker, str):
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


    for cle, valeur in loaded_dict.items():
        str = str.replace(cle, valeur)
    return str

def format_name(str, competitorName1, competitorName2, bookmaker):
    #Remplacement par bookmaker
    if bookmaker == "unibet" : 
        str  = format_replace("unibet", str)
    if bookmaker == 'winamax':
        str  = format_replace("winamax", str)
    
    #Home / Away
    str = str.replace(competitorName1, 'Home')
    str = str.replace(competitorName2, 'Away')
    str = str.replace(competitorName1.lower(), 'Home')
    str = str.replace(competitorName2.lower(), 'Away')

    return str

#Check des trads
def check_outcome(betTitle, competitorName1, competitorName2, outcome_name, outcome_name_old, trad_bets, bookmaker):
    boucle = True
                        
    while boucle :
        try :
            outcome_name = trad_bets[betTitle][outcome_name]
            boucle = False
        except KeyError : 
            print("-------------------------------------- KEY ERROR SPOTTED ---------------------------------------------")
            print(f"pour le bet {betTitle}, \n Team en présence : {competitorName1} et {competitorName2} \n str rentré {outcome_name_old}, \n Transformé en {outcome_name}")
            s1 = SequenceMatcher(None, outcome_name_old, competitorName1)
            s2 = SequenceMatcher(None, outcome_name_old, competitorName2)
            if s2.ratio() > s1.ratio() :
                print(f"On rajoute la règle : {outcome_name_old} en {competitorName2}")
                with open(f'bookmakers\\trad_bookmakers\{bookmaker}.pkl', 'rb') as f:
                    loaded_dict = pickle.load(f)
                    f.close()
                with open(f'bookmakers\\trad_bookmakers\{bookmaker}.pkl', 'wb') as f:
                    loaded_dict[outcome_name_old] = competitorName2
                    pickle.dump(loaded_dict, f)
                    f.close()
            else :
                print(f"On rajoute la règle : {outcome_name_old} en {competitorName1}")
                with open(f'bookmakers\\trad_bookmakers\{bookmaker}.pkl', 'rb') as f:
                    loaded_dict = pickle.load(f)
                    f.close()
                with open(f'bookmakers\\trad_bookmakers\{bookmaker}.pkl', 'wb') as f:
                    loaded_dict[outcome_name_old] = competitorName1
                    pickle.dump(loaded_dict, f)
                    f.close()
            actualisation_trad(bookmaker)
            outcome_name = format_name(outcome_name, competitorName1, competitorName2, bookmaker)
        except :
            raise
    return outcome_name



#Traduction
trad_unibet = {}
trad_winamax = {}
trad_betclic = {}
trad_netbet = {}
trad_zebet = {}



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

actualisation_trad("all")