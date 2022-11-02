import unidecode
import pickle
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

    
def format_espace(str):
    new_str = ""
    for mot in str.split(" "):
        if mot != '':
            new_str += " " + mot
    return new_str

def format_name_g(str):
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
print("ImportantClass read")