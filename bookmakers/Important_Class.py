######################################################## CLASSES ########################################################
   
class Match :
    def __init__(self,eq1:str,eq2:str,bets:dict) -> None:
        self.eq1 = eq1
        self.eq2 = eq2
        self.issues = bets
    
    def get_name(self):
        return self.eq1 + " / " + self.eq2

    
