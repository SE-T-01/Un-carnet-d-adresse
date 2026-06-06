# Version 1.0.0
"""
class AddressBook:
    def __init__(self):
        self.book=[]
    def AddContact(self,Cont):
        self.book.append(Cont)
    def RemoveContact(self,name):
        if len(self.book)==0:
            print("Le répértoire est vide")
        else:
            for i, contact in enumerate(self.book):
                if contact.nom.lower() == name.lower():
                    del self.book[i]
                    print(f"Contact '{name}' supprimé avec succès.")
                else :
                    print("Contact inexsiste")         
    def desplayContact(self,name):
         if len(self.book)==0:
            print("Le répértoire est vide")
         else:
            for contact in self.book:
                if contact.nom==name:
                    print(contact)
                else:
                     print("Contact inexsiste")
"""
#Version 2.0.0
import os
from contact import Contact
class AddressBook:
    def __init__(self,fich="Mescontacts.txt"):
        self.fich=fich
        self.book=[]
        if not os.path.exists(self.fich):#Si le fichier n'existe pas on va le crée
            open(self.fich,"w").close()
        else:#Charger les contacts existants (si fichier existe)
            self.charger()
    def charger(self):
        """Lit le fichier et remplit self.book"""
        with open(self.fich, 'r') as f:
            for ligne in f:
                ligne = ligne.strip()
                if ligne:
                    parties = ligne.split(';')
                    if len(parties) == 3:
                        nom, tel, email = parties
                        contact = Contact(nom, tel, email)
                        self.book.append(contact)
    def save(self):
        #Sauvegarde tous les contacts dans le fichier texte
        with open(self.fich, 'w') as fi:
            for contact in self.book:
                # Écrire une ligne: nom;email;telephone
                ligne = f"{contact.nom};{contact.num_tel};{contact.email}\n"
                fi.write(ligne)
    def AddContact(self,Cont):
         # Vérifier les doublons (même nom, insensible à la casse)
        for contact in self.book:
            if contact.nom.lower() == Cont.nom.lower():
                print(f"Le contact '{Cont.nom}' existe déjà.")
                return False 
            
        self.book.append(Cont)
        #Sauvegarder dans le fichier
        self.save()
        print(f"Contact '{Cont.nom}' ajouté avec succès.")
        return True
    def RemoveContact(self,name):
        if len(self.book)==0:
            print("Le répértoire est vide")
        else:
            for i, contact in enumerate(self.book):
                if contact.nom.lower() == name.lower():
                    del self.book[i]
                    self.save()
                    print(f"Contact '{name}' supprimé avec succès.")
                else :
                    print("Contact inexsiste")
    """
    def desplayContact(self,name):
        if len(self.book)==0:
            print("Le répértoire est vide")
        else:
            for contact in self.book:
                if contact.nom==name:
                    return contact
                    #print(contact)
                else:
                     #print("Contact inexsiste")
                    return None
    
    def desplayContact(self, name):
            if len(self.book) == 0:
                return None
            name_clean = name.strip().lower()  # Nettoyer et mettre en minuscules
            for contact in self.book:
                contact_name_clean = contact.nom.strip().lower()
                if contact_name_clean == name_clean:
                    return contact
            return None
    """
    def desplayContact(self, name):
        if not os.path.exists(self.fich):
            print("Fichier non trouvé")
            return
        name_clean = name.strip().lower()
        with open(self.fich, 'r', encoding='utf-8') as f:
            for ligne in f:
                ligne = ligne.strip()
                if not ligne:
                    continue
                # Découper la ligne : nom;téléphone;email
            parties = ligne.split(';')
            if len(parties) == 3:
                nom_fichier, tel, email = parties
                if nom_fichier.strip().lower() == name_clean:
                    print(f" Nom : {nom_fichier}")
                    print(f" Téléphone : {tel}")
                    print(f" Email : {email}")
                    return
    
                print(f"❌ Contact '{name}' non trouvé.")
    def afficher_fichier(self):
        if os.path.exists(self.fich):
            with open(self.fich, 'r') as fi:
                lignes = fi.readlines()
                if lignes:
                    for ligne in lignes:
                        ligne = ligne.strip()
                        if ligne:
                            # Remplacer ; par des espaces
                            ligne_formatee = ligne.replace(';', '   ')
                            print(ligne_formatee)   
                else:
                    print("Le fichier est vide.")   
        else:
            print("Fichier non trouvé")

                
