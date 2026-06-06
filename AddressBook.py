
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
                
