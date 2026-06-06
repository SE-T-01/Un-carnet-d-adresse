import re
class Contact:
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    def __init__(self,nom,num_tel,email):
        assert isinstance(nom,str) and len(nom)>0, "Nom invalide"
        assert isinstance(num_tel,str) and num_tel.isdigit() and len(num_tel)>=10 and (num_tel.startswith("06") or num_tel.startswith("07")) ,"Numéro de téléphone invalide"
        assert isinstance(email,str) and re.match(Contact.pattern, email) ,"Email non valid"
        self.nom=nom
        self.num_tel=num_tel
        self.email=email
    def __str__(self):
        return " Le nom de contact :\t %s \n L'email de contact :\t %s \n Le numéro de téléphone de contacte :\t %s "%(self.nom,self.email,self.num_tel)